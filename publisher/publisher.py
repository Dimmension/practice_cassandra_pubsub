import asyncio
from rabbit import aio_pika, channel_pool

async def send_message(
    channel_pool: aio_pika.pool.Pool,
    message: str
) -> None:
    async with channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange("new_exchange", type=aio_pika.ExchangeType.DIRECT,
            durable=True
        )
        queue = await channel.declare_queue("new_queue", durable=True)
        await queue.bind(exchange, routing_key="new_queue")
        
        await exchange.publish(
            aio_pika.Message(body=message.encode(), delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
            routing_key="new_queue"
        )


async def main() -> None:
    with open("input.txt", "r") as f:
        for l in f:
            line = l.strip()
            await send_message(channel_pool, line)
            print(f"Sent: {line}")

if __name__ == "__main__":
    asyncio.run(main())

