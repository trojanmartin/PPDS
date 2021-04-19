import aiohttp
import asyncio

class Shared:
    def __init__(self):        
        self.finished = False


async def Progress(shared):
    while(not shared.finished):
        await asyncio.sleep(0.01)
        print("In progress")


async def download(shared):
    print("Starting dowloading")
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.google.com') as resp:
            shared.finished = True
            print("Downloading finished")
                

async def main():
    share = Shared()
    await asyncio.gather(Progress(share),download(share))        


if __name__ == "__main__":
    asyncio.run(main())
