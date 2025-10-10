import argparse
import asyncio

import aioconsole

from environs import Env


async def authorized(reader, writer):
    writer.write(f"fd97791e-a5d6-11f0-a5a4-0242ac110003\n\n".encode())
    await writer.drain()
    await read_message(reader)


async def read_message(reader):
    message = await reader.read(200)
    print(message.decode())


async def write_message(writer):
    message = await aioconsole.ainput()
    writer.write(f"{message}\n\n".encode())
    await writer.drain()


async def main():
    env = Env()
    env.read_env()

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

    await authorized(reader, writer)

    while True:
        await read_message(reader)
        await write_message(writer)


if __name__ == "__main__":
    asyncio.run(main())
