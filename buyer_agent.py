from uagents import Agent, Context, Model, Protocol
from uagents.setup import fund_agent_if_low


class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str
    info: tuple


class TransactionInfo(Model):
    tx_hash: str
    amount: int
    info: tuple


bob = Agent(
    name="bob",
    port=8002,
    seed="bob secret phrase",
    endpoint=["http://127.0.0.1:8002/submit"],
)

fund_agent_if_low(bob.wallet.address())


@bob.on_message(model=PaymentRequest, replies=TransactionInfo)
async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(f"Received payment request from {sender}: {msg}")

    # send the payment
    transaction = ctx.ledger.send_tokens(
        msg.wallet_address, msg.amount, "atestfet", ctx.wallet
    )

    ctx.logger.info(f"Processed payment request from {sender}")

    # send the tx hash so alice can confirm
    await ctx.send(sender, TransactionInfo(tx_hash=transaction.tx_hash, amount=msg.amount, info=msg.info))

print(bob.address)
bob.run()