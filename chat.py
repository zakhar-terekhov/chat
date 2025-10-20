import argparse
import asyncio
import datetime

from environs import Env

from saving_history import write_message_to_file


async def display_chat(reader: asyncio.StreamReader, history_path: str):
    """Отображает чат."""
    while True:
        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        raw = await reader.read(200)
        message = f"[{current_datetime}] {raw.decode()}"

        await write_message_to_file(message, history_path)
        print(message)


async def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        description="""Отображает чат с сервера по заданному хосту и порту.
                    Чат выводится в консоль и записывается в файл.""",
    )

    parser.add_argument("-H", "--host", default=env.str("HOST"), help="Host")
    parser.add_argument(
        "-P", "--port", default=env.int("READ_PORT"), help="Read port for reading chat"
    )
    parser.add_argument(
        "-F", "--history", default=env.str("HISTORY"), help="Path to chat history"
    )

    args = parser.parse_args()

    history_path = args.history

    reader, writer = await asyncio.open_connection(args.host, args.port)

    try:
        await display_chat(reader, history_path)
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
