# coding:utf-8
import asyncio
from pathlib import Path

import aiohttp
import aiofiles

# will be blocked by antispider
# need global proxy

async def download_worker(session: aiohttp.ClientSession, task_queue: asyncio.Queue):
    while True:
        path, url = await task_queue.get()
        if Path(path).exists():  # 已下载，跳过
            task_queue.task_done()
            continue
        async with session.get(url=url) as resp:
            if resp.status != 200:
                print(resp.status)
                raise RuntimeError
            data = await resp.read()
            print(path)
            async with aiofiles.open(path, mode='wb') as f:
                await f.write(data)
                task_queue.task_done()


async def download_book_async(download_dir: str, template_url: str, page_range: range):
    async with aiohttp.ClientSession() as session:
        task_queue = asyncio.Queue(maxsize=10)
        workers_num = 4
        # 创建并运行worker
        workers = [asyncio.create_task(download_worker(session, task_queue)) for _ in range(workers_num)]
        for page in page_range:
            await task_queue.put(
                (
                    str(Path(download_dir) / f'{page}.pdf'),
                    template_url.format(page)
                )
            )

        # 等待尚未完成的下载
        await task_queue.join()

        # 销毁worker
        for worker in workers:
            worker.cancel()
        await asyncio.gather(*workers, return_exceptions=True)


def download_book(download_dir: str, template_url: str, page_range: range):
    Path(download_dir).mkdir(exist_ok=True)
    asyncio.run(download_book_async(download_dir, template_url, page_range))


if __name__ == '__main__':
    download_book(download_dir='./download',
                  template_url='https://ssj-sslibrary-com-s.qh.yitlink.com:8444/download/getFile?fileMark=13531247&userMark=&pages=368&time=1630855832279&enc=504affcec1c8e0971a1da313c3d35682&code=8e8e18359d4fbf5118dff042e74d825f&cpage={}',
                  page_range=range(200, 369)
    )
