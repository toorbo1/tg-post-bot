import random, time
from duckduckgo_search import DDGS

# Try DDGS with delay and random query suffix to avoid cache/rate-limit
query = "IT technology computer " + str(random.randint(1, 9999))
time.sleep(random.uniform(1.5, 3.0))
try:
    with DDGS() as ddgs:
        results = list(ddgs.images(query, max_results=3))
        for r in results:
            url = r.get('image', '')
            if url.startswith('http') and not url.endswith('.svg'):
                print('OK: ' + url[:90])
                break
        else:
            print('No valid results')
except Exception as e:
    print('FAIL: ' + str(e)[:100])
