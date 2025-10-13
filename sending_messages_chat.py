import argparse
import asyncio
import json
import logging

import aioconsole

from environs import Env

logger = logging.getLogger("sender")


async def authorize(token, reader, writer):
    writer.write(f"{token}\n\n".encode())
    await writer.drain()
    raw = await reader.readline()
    return raw.decode()


async def read_message(reader):
    raw = await reader.readline()
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
        Пользователь авторизуется по токену, предвариительно должен быть зарегистрирован.
        Запуск registration.py - регистрация нового пользователя.
        Запуск reading_messages.py - отображение чата.""",
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

    await read_message(reader)

    response = await authorize(token, reader, writer)

    if json.loads(response) is None:
        print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
        return

    while True:
        await read_message(reader)
        await write_message(writer)


if __name__ == "__main__":
    asyncio.run(main())
