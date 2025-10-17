import asyncio

import aioconsole

from logger import setup_logger


async def read_message(reader: asyncio.StreamReader):
    logger = setup_logger("read_message")

    raw = await reader.readline()
    message = raw.decode()

    logger.info(message)
    print(message)


async def submit_message(writer: asyncio.StreamWriter):
    logger = setup_logger("submit_message")

    message = await aioconsole.ainput()

    logger.info(message)

    writer.write(f"{message}\n\n".encode())
    await writer.drain()


async def submit_registration_message(writer: asyncio.StreamWriter, message: str):
    logger = setup_logger("submit_registration_message")
    logger.info(message)

    writer.write(f"{message}".encode())
    await writer.drain()
