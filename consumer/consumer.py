import asyncio
import os
from cassandra.cluster import Cluster
from rabbit import channel_pool
import aio_pika
from consts import *

cluster = Cluster(contact_points=CASSANDRA_HOSTS, port=CASSANDRA_PORT)
session = cluster.connect()
session.execute(CREATE_KEYSPACE)
session.set_keyspace("my_keyspace")
session.execute(CREATE_TABLE)
insert_stmt = session.prepare(INSERT_KEYSPACE)

async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            session.execute(insert_stmt, (message.body.decode(),))
            print(f"Message saved: {message.body.decode()}")
        except Exception as e:
            print(f"Error during saving: {e}")
            raise

async def main():
    async with channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange("new_exchange", type=aio_pika.ExchangeType.FANOUT, durable=True)
        queue = await channel.declare_queue("new_queue", durable=True)
        await queue.bind(exchange, routing_key="new_queue")
        await queue.consume(process_message)

if __name__ == "__main__":
    asyncio.run(main())