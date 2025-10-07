import asyncio
import datetime

import aiofiles


async def write_message_to_file(message: str):
    async with aiofiles.open("chat_file.txt", "a") as f:
        await f.write(message)


async def main():
    while True:
        reader, _ = await asyncio.open_connection("minechat.dvmn.org", 5000)

        current_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        raw = await reader.read(200)
        message = f"[{current_datetime}] {raw.decode()}"

        await write_message_to_file(message)
        print(message)


if __name__ == "__main__":
    asyncio.run(main())
