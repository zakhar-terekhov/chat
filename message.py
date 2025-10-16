import logging

import aioconsole


logger = logging.getLogger("message")


async def read_message(reader):
    raw = await reader.readline()
    message = raw.decode()
    logger.info(message)
    print(message)


async def submit_message(writer):
    message = await aioconsole.ainput()
    logger.info(message)
    writer.write(f"{message}\n\n".encode())
    await writer.drain()


async def submit_registration_message(writer, message):
    writer.write(f"{message}".encode())
    logger.info(message)
    await writer.drain()
