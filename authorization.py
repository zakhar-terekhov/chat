import argparse
import asyncio
import json

from environs import Env

from logger import setup_logger
from message import read_message, submit_message

logger = setup_logger("authorization")


async def authorize(
    token: str, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> str:
    """Авторизует пользователя по токену."""
    writer.write(f"{token}\n\n".encode())
    await writer.drain()

    raw = await reader.readline()
    return raw.decode()


async def main():
    env = Env()
    env.read_env()

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
    parser.add_argument(
        "-T",
        "--token",
        default=env.str("TOKEN"),
        help="Token for authorization",
    )
    args = parser.parse_args()

    reader, writer = await asyncio.open_connection(args.host, args.port)

    await read_message(reader)

    authorization = await authorize(args.token, reader, writer)

    response = json.loads(authorization)

    if response is None:
        logger.info(
            f"Неизвестный токен {args.token}. Проверьте его или зарегистрируйте заново."
        )
        print("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
        return

    logger.info(
        f"Успешная авторизация пользователя {response['nickname']} по токену {args.token}."
    )

    while True:
        await read_message(reader)
        await submit_message(writer)


if __name__ == "__main__":
    asyncio.run(main())
