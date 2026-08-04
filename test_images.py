import requests
queries = ['technology', 'cybersecurity', 'programming', 'server', 'network', 'ai', 'computer', 'coding', 'internet', 'data']
for q in queries:
    try:
        r = requests.get('https://source.unsplash.com/featured/800x600/?' + q, allow_redirects=True, timeout=5)
        status = str(r.status_code)
        url = (r.url[:70] if 'unsplash' in r.url else 'redirected')
        print(q + ': ' + status + ' -> ' + url)
    except Exception as e:
        print(q + ': FAILED - ' + str(e)[:50])
