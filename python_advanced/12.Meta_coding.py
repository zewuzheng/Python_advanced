#%%
# hasattr

a = {'c':1, 'd':2}
print(a)
print(hasattr(a, 'items'))
print(hasattr(a, 'e'))

#%%
from urllib.request import urlopen
import warnings
import os
import json

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'data/osconfeed.json'

def load():
    if not os.path.exists(JSON):
        msg = f'downloading {URL} to {JSON}'
        warnings.warn(msg)
        with urlopen(URL) as remote, open(JSON, 'wb') as local:
            local.write(remote.read())

    with open(JSON) as fp:
        return json.load(fp)

feed = load()
