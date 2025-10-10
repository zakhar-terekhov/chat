import argparse
import asyncio
import logging

import aioconsole

from environs import Env

logger = logging.getLogger("sender")


async def authorized(token, reader, writer):
    writer.write(f"{token}\n\n".encode())
    await writer.drain()
    await read_message(reader)


async def read_message(reader):
    raw = await reader.read(200)
    message = raw.decode()
    logger.info(message)
    print(message)


async def write_message(writer):
    message = await aioconsole.ainput()
    logger.info(message)
    writer.write(f"{message}\n\n".encode())
    await writer.drain()


async def main():
    env = Env()
    env.read_env()

    token = env.str("TOKEN")

    logging.basicConfig(
        level=logging.INFO,
        filename="history.log",
        format="%(levelname)s:%(name)s:%(message)s",
    )

    parser = argparse.ArgumentParser(
        description="""Позволяет отправлять сообщения в чат.
        После запуска данного скрипта можно создать нового пользователя или авторизоваться по токену.
        Для того, что увидеть отправленное сообщение в общем чате, необходимо запустить скрипт reading_messages.py.""",
    )

    parser.add_argument("-H", "--host", default=env.str("HOST"), help="Host")
    parser.add_argument(
        "-P",
        "--port",
        default=env.int("WRITE_PORT"),
        help="Port for sending messages to the chat",
    )

    args = parser.parse_args()

    reader, writer = await asyncio.open_connection(args.host, args.port)

    await authorized(token, reader, writer)

    while True:
        await read_message(reader)
        await write_message(writer)


if __name__ == "__main__":
    asyncio.run(main())
