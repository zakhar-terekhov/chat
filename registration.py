import argparse
import asyncio
import logging

from environs import Env

from sending_messages_chat import submit_message, read_message

logger = logging.getLogger("registration")


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

    args = parser.parse_args()

    reader, writer = await asyncio.open_connection(args.host, args.port)

    await read_message(reader)

    for _ in range(2):
        await submit_message(writer, "\n")
        await read_message(reader)

if __name__ == "__main__":
    asyncio.run(main())
