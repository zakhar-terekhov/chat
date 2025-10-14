import argparse
import asyncio
import json
import logging

from environs import Env

from message import read_message, submit_message


logger = logging.getLogger("authorization")


async def authorize(token, reader, writer):
    writer.write(f"{token}\n\n".encode())
    await writer.drain()
    raw = await reader.readline()
    return raw.decode()


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
        description="""Пользователь авторизуется по токену, предвариительно должен быть зарегистрирован.
        После успешной авторизации, скрипт позволяет отправлять сообщения в чат.
        Запуск registration.py - регистрация нового пользователя.
        Запуск chat.py - отображение чата.""",
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
        await submit_message(writer)


if __name__ == "__main__":
    asyncio.run(main())
