import argparse
import asyncio
import logging

from environs import Env

from message import read_message, submit_registration_message


logger = logging.getLogger("registration")


async def register(reader, writer, username):
    await read_message(reader)
    await submit_registration_message(writer, "\n")
    await read_message(reader)
    await submit_registration_message(writer, f"{username}\n")
    await read_message(reader)


async def main():
    env = Env()
    env.read_env()

    logging.basicConfig(
        level=logging.INFO,
        filename="history.log",
        format="%(levelname)s:%(name)s:%(message)s",
    )

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


if __name__ == "__main__":
    asyncio.run(main())
