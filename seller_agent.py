from uagents import Agent, Context, Model, Protocol
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low


class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str
    info: tuple


class PaymentInitialization(Model):
    address: str
    amount: int
    denom: str
    info: tuple

class TransactionInfo(Model):
    tx_hash: str
    amount: int
    info: tuple

class TransactionRcpt(Model):
    tx_hash: str
    status: str
    info: tuple


alice = Agent(
    name="alice",
    port=8001,
    seed="alice secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

fund_agent_if_low(alice.wallet.address())



@alice.on_message(model=PaymentInitialization, replies=PaymentRequest)
async def request_funds(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(f"Received payment request from {sender}: {msg.address} {msg.amount}")
    await ctx.send(
        msg.address,
        PaymentRequest(
            wallet_address=str(ctx.wallet.address()), amount=msg.amount, denom="atestfet", info=msg.info
        ),
    )


@alice.on_message(model=TransactionInfo, replies=TransactionRcpt)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)

    coin_received = tx_resp.events["coin_received"]
    print(coin_received["receiver"], str(ctx.wallet.address()))
    if (
        coin_received["receiver"] == str(ctx.wallet.address())
        and coin_received["amount"] == f"{msg.amount}atestfet"
    ):
        ctx.logger.info(f"Transaction {msg.tx_hash} success")
        await ctx.send('agent1qggfh6rfj0c6upfugetfq2yn78kmjhrlr3nndmpsssqedvlpjtjlvrt00rp',
                 TransactionRcpt(tx_hash=msg.tx_hash, status="success", info=msg.info))
    else:
        ctx.logger.error(f"Transaction {msg.tx_hash} failed")
        await ctx.send('agent1qggfh6rfj0c6upfugetfq2yn78kmjhrlr3nndmpsssqedvlpjtjlvrt00rp', TransactionRcpt(tx_hash=msg.tx_hash, status="failed"))

print(alice.address)
print(alice.wallet.address())
alice.run()