import time, sys
from duckduckgo_search import DDGS
query = 'IT technology computer'
time.sleep(1)
try:
    with DDGS() as ddgs:
        results = list(ddgs.images(query, max_results=5))
        for r in results:
            url = r.get('image','')
            if url.startswith('http'):
                print('OK: ' + url[:80])
except Exception as e:
    print('FAIL: ' + str(e)[:100])
