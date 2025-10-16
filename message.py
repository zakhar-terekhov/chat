import aioconsole

from logger import setup_logger


async def read_message(reader):
    logger = setup_logger("read_message")
    raw = await reader.readline()
    message = raw.decode()
    logger.info(message)
    print(message)


async def submit_message(writer):
    logger = setup_logger("submit_message")
    message = await aioconsole.ainput()
    logger.info(message)
    writer.write(f"{message}\n\n".encode())
    await writer.drain()


async def submit_registration_message(writer, message):
    logger = setup_logger("submit_registration_message")
    logger.info(message)
    writer.write(f"{message}".encode())
    await writer.drain()
