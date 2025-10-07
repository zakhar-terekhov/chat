import asyncio


async def main():
    reader, _ = await asyncio.open_connection("minechat.dvmn.org", 5000)

    while True:
        data = await reader.read(100)
        print(
            data.decode(
                encoding="utf-8",
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
