import logging

import aioconsole


logger = logging.getLogger("authorization")


async def read_message(reader):
    raw = await reader.readline()
    message = raw.decode()
    logger.info(message)
    print(message)


async def submit_message(writer, line_break="\n\n"):
    message = await aioconsole.ainput()
    logger.info(message)
    writer.write(f"{message}{line_break}".encode())
    await writer.drain()
