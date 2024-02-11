from threading import Thread
from uagents import Agent, Bureau, Context, Model
from uagents.setup import fund_agent_if_low

from discord.ext import commands
import discord
import asyncio

import json


def place_order(item, address):
    try:
        with open('order.json', "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
    data.update({
        item: address
    })
    with open('order.json', "w") as json_file:
        json.dump(data, json_file, indent=4)


def add_data(price, name, file_path='test.json'):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
    data.update({
        name[:1] + str(price): {
            'price': price,
            'name': name
        }
    })
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("Data has been added successfully.")


def remove_data(key_to_remove, file_path='test.json'):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("File not found.")
        return
    if key_to_remove in data:
        del data[key_to_remove]
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Key '{key_to_remove}' has been removed successfully.")
    else:
        print(f"Key '{key_to_remove}' not found in the data.")


def retrieve_data(file_path='test.json'):
    try:
        with open(file_path, "r") as json_file:
            catalog = 'Catalog:\n\n'
            data = json.load(json_file)
            for key in sorted(data.keys()):
                name = data[key]['name']
                price = data[key]['price']
                catalog += f"{key.ljust(10)} =>    {name.ljust(20)} -      ${price}\n"

        return catalog

    except FileNotFoundError:
        print("File not found.")
        return None
    
def order_info(id, file_path='test.json'):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return data[id]['price']
    except FileNotFoundError:
        print("File not found.")
        return None


order = []

intents = discord.Intents.all()
intents.members = True

dbot = commands.Bot(command_prefix='$', intents=intents)


def read_token():
    with open("token.txt", "r") as file:
        return file.read().strip()


allowed_channel_name = "test"


@dbot.command(name='addItem')
async def addItem(ctx):
    if ctx.channel.name != allowed_channel_name:
        await ctx.send("This command can only be used in a specific channel.")
        return

    admin_role = discord.utils.get(ctx.guild.roles, name='Admin')
    if not admin_role in ctx.author.roles:
        # await ctx.send("You don't have permission to use this command.")
        return

    await ctx.send("Enter item name")

    def check_author(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        item = await dbot.wait_for('message', timeout=30.0, check=check_author)
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you took too long to respond.")
    else:
        item = item.content
        await ctx.send("Enter item price")
        try:
            price = await dbot.wait_for('message', timeout=30.0, check=check_author)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long to respond.")
        else:
            price = price.content
            add_data(price, item)


@dbot.command(name='catalog')
async def catalog(ctx):
    if ctx.channel.name != allowed_channel_name:
        # await ctx.send("This command can only be used in a specific channel.")
        return

    data = retrieve_data()
    if data is None:
        await ctx.send("No data found.")

    await ctx.send(data)


@dbot.command(name='buy')
async def buy(ctx):
    if ctx.channel.name != allowed_channel_name:
        # await ctx.send("This command can only be used in a specific channel.")
        return

    def check_author(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send("Enter the Item Id.")

    try:
        item = await dbot.wait_for('message', timeout=30.0, check=check_author)
    except asyncio.TimeoutError:
        await ctx.send("Sorry, you took too long to respond.")
    else:
        item = item.content
        await ctx.send("Enter the Agentverse Address.")
        try:
            padr = await dbot.wait_for('message', timeout=30.0, check=check_author)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long to respond.")
        else:
            padr = padr.content
            await ctx.send("Enter the Delivery Address.")
            try:
                dadr = await dbot.wait_for('message', timeout=30.0, check=check_author)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you took too long to respond.")
            else:
                dadr = dadr.content
                order.append((item, padr, dadr))


class PaymentInitialization(Model):
    address: str
    amount: int
    denom: str
    info: tuple


class TransactionRcpt(Model):
    tx_hash: str
    status: str
    info: tuple


bot = Agent(
    name="bot",
    port=8000,
    seed="bot secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(bot.wallet.address())


@bot.on_interval(period=1)
async def request_funds(ctx: Context):
    if len(order) > 0:
        ctx.logger.info(f"Received payment request of amount {int(order_info(order[0][0]))}: {order[0][1]}")
        await ctx.send(
            'agent1qdp9j2ev86k3h5acaayjm8tpx36zv4mjxn05pa2kwesspstzj697xy5vk2a',
            PaymentInitialization(
                address=order[0][1], amount=int(order_info(order[0][0])), denom='atestfet', info=(order[0][0], order[0][2])
            ),
        )
        order.pop(0)


@bot.on_message(model=TransactionRcpt)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionRcpt):
    if msg.status == "success":
        ctx.logger.info("Transaction successful")
        place_order(msg.info[0], msg.info[1])
    else:
        ctx.logger.error("Transaction failed")


def run_bot():
    dbot.run(read_token())


if __name__ == "__main__":
    thread = Thread(target=run_bot)
    thread.start()
    print(bot.address)
    bot.run()
