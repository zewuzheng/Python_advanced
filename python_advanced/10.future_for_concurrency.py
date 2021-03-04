# %%
from concurrent import futures
import os
import time
import sys

import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR').split()

BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flag(cc):
    url = f'{BASE_URL}/{cc}/{cc}.gif'
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end='')
    sys.stdout.flush()


MAX_WORKER = 20


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower + '.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKER, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))

# executor eturn results in the same order as input sequence

def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    print(f'{count} flags downloaded in {elapsed:.2f}s')


if __name__ == '__main__':
    main(download_many)

# %%
# concurrent.futures.Future and asyncio.Future:
# they all represents jobs that have or have yet been done.
# for concurrent.futures.ThreadPoolExecutor, it returns an iter, and iter have 'next' method that get the results of each futures.
# strictly speaking, the concurrent downloads we defined above is not parallel download,
# because it the constrained by Galbal Interpreter Lock. So it is ran in serveral threads.

# GIL: because CPython Interpreter is not save in threads, so a python process cannot use multiple cpu cores simutaneously.

#%%
from tqdm import tqdm
import time
for i in tqdm(range(100)):
    time.sleep(0.1)
    