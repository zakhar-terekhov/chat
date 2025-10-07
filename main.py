import argparse
import asyncio
import datetime

import aiofiles
from environs import Env


async def write_message_to_file(message: str, history_path: str):
    async with aiofiles.open(history_path, "a") as f:
        await f.write(message)


async def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(
        prog="Чат",
        description="""Отображает чат с сервера по заданному хосту и порту.
                    Чат выводится в консоль и записывается в файл.""",
    )

    parser.add_argument("-H", "--host", default=env.str("HOST"), help="Host")
    parser.add_argument("-P", "--port", default=env.int("PORT"), help="Port")
    parser.add_argument("-F", "--history", default=env.str("HISTORY"), help="Path to chat history")

    args = parser.parse_args()

    history_path = args.history

    while True:
        reader, _ = await asyncio.open_connection(args.host, args.port)

        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        raw = await reader.read(200)
        message = f"[{current_datetime}] {raw.decode()}"

        await write_message_to_file(message, history_path)
        print(message)


if __name__ == "__main__":
    asyncio.run(main())
