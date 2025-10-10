import aiofiles


async def write_message_to_file(message: str, history_path: str):
    async with aiofiles.open(history_path, "a") as f:
        await f.write(message)
