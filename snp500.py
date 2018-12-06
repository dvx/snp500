import requests
import os, time, json, sys
from bottle import route, run, template, error, response, request
import redis
import pandas as pd
import const

r = redis.Redis(decode_responses=True).from_url(url=const.REDIS_URL)

@error(404)
def error404(error):
    response.set_header('Content-Type', 'application/json')
    return json.dumps('The barking of a dog does not disturb the man on a camel -- Egyptian Proverb')

@route('/')
def api():
    t = time.time()
    cache_hit = True
    wiki_req = requests.get(const.WIKIPEDIA_API_REV.format(const.SNP500_COMPANIES_PAGE))
    rev_dict = wiki_req.json()['query']['pages']
    wiki_rev = rev_dict[next(iter(rev_dict))]['revisions'][0]['revid']
    cached_rev = r.get('cached_rev')
    out = { }
    try:
        # do we have a cache miss?
        if cached_rev is not None and wiki_rev != int(cached_rev):
            cache_hit = False
            wiki_req = requests.get(const.WIKIPEDIA_API_PARSE.format(const.SNP500_COMPANIES_PAGE))
            wiki_html = wiki_req.json()['parse']['text']['*']
            tables = pd.read_html(wiki_html)
            sp500_table = tables[0]
            symbols = sp500_table[0].get_values()[1:]
            r.set('cached_rev', wiki_req.json()['parse']['revid'])
            r.set('cached_symbols', json.dumps(symbols.tolist()))
        symbols = json.loads(r.get('cached_symbols'))
        num_symbols = len(symbols)
        out['symbols'] = json.loads(r.get('cached_symbols'))
        out['rev'] = int(r.get('cached_rev'))
        out['num_symbols'] = num_symbols
        out['sane'] = num_symbols == const.EXPECTED_SYMBOLS
        out['cache_hit'] = cache_hit
        out['t'] = time.time() - t
    except Exception as e:
        print(e, file=sys.stderr)
    response.set_header('Content-Type', 'application/json')
    return out

run(host='0.0.0.0', port=int(const.PORT))
