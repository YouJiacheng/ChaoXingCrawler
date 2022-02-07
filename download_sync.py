# coding:utf-8
from pathlib import Path

import requests

# will be blocked by antispider
# need global proxy

def download_book_sync(download_dir: str, template_url: str, page_range: range):
    task_iter = (
        (
            str(Path(download_dir) / f'{page}.pdf'),
            template_url.format(page)
        ) 
        for page in page_range
    )
    ok = True
    while True:
        try:
            if ok:
                path, url = next(task_iter)
            if Path(path).exists():  # 已下载，跳过
                continue
            print(path)
            resp = requests.get(url=url, timeout=30)
            print(resp.status_code)
            if resp.status_code == 200:
                with open(path, mode='wb') as f:
                    f.write(resp.content)
                    ok = True
            else:
                ok = False
        except requests.exceptions.Timeout:
            print('timeout')
            ok = False
        except StopIteration:
            break

def download_book(download_dir: str, template_url: str, page_range: range):
    Path(download_dir).mkdir(exist_ok=True)
    download_book_sync(download_dir, template_url, page_range)


if __name__ == '__main__':
    download_book(download_dir='./test2',
                  template_url='https://ssj-sslibrary-com-s.qh.yitlink.com:8444/download/getFile?fileMark=13534500&userMark=&pages=589&time=1630847861896&enc=e66c6586ed8aa05220a5e39064c6f62c&code=721094ac2e7f448d4ca57dbf5e9f8dfd&cpage={}',
                  page_range=range(589, 590)
    )