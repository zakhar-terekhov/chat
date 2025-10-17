import argparse
import asyncio

from environs import Env

from logger import setup_logger
from message import read_message, submit_registration_message

logger = setup_logger("registration")


async def register(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter, username: str
):
    """Регистрирует пользователя."""
    await read_message(reader)
    await submit_registration_message(writer, "\n")
    await read_message(reader)
    await submit_registration_message(writer, f"{username}\n")
    await read_message(reader)


async def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        description="""Регистрирует пользователя в чате.""",
    )

    parser.add_argument("-H", "--host", default=env.str("HOST"), help="Host")
    parser.add_argument(
        "-P",
        "--port",
        default=env.int("WRITE_PORT"),
        help="Port for sending messages to the chat",
    )
    parser.add_argument(
        "-U",
        "--username",
        default=env.str("USERNAME"),
        help="Username",
    )

    args = parser.parse_args()

    reader, writer = await asyncio.open_connection(args.host, args.port)

    await register(reader, writer, args.username)
    
    logger.info(f"Пользователь {args.username} зарегистрирован.")


if __name__ == "__main__":
    asyncio.run(main())
