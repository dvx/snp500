import requests
from bottle import route, run, template, error, response, request
import os, time, json
import redis
import pandas as pd
import const

pool = redis.ConnectionPool(decode_responses=True).from_url(url=const.REDIS_URL)
r = redis.Redis(connection_pool=pool)

@error(404)
def error404(error):
	response.set_header('Content-Type', 'application/json')
	return json.dumps('The barking of a dog does not disturb the man on a camel -- Egyptian Proverb')

@route('/')
def home():
	r = redis.Redis(connection_pool=pool)
	response.set_header('Content-Type', 'application/json')
	wiki_req = requests.get(const.WIKIPEDIA_API_REV.format(const.SP500_COMPANIES_PAGE))
	rev_dict = wiki_req.json()['query']['pages']
	wiki_rev = rev_dict[next(iter(rev_dict))]['revisions'][0]['revid']
	
	# do we have a cache miss?
	if wiki_rev != r.get('cached_rev'):
		print('cache miss')
		wiki_req = requests.get(const.WIKIPEDIA_API_PARSE.format(const.SP500_COMPANIES_PAGE))
		wiki_html = wiki_req.json()['parse']['text']['*']
		tables = pd.read_html(wiki_html)
		sp500_table = tables[0]
		symbols = sp500_table[0].get_values()[1:]
		r.set('cached_rev', wiki_req.json()['parse']['revid'])
		r.set('cached_symbols', symbols.tolist())
		r.set('cached_symbols_len', len(symbols))

	return {
			'symbols': list(r.get('cached_symbols')),
			'rev': r.get('cached_rev'),
			'num_symbols': r.get('cached_symbols_len'),
			'sanity': r.get('cached_symbols_len') == const.EXPECTED_SYMBOLS
			}

run(host='0.0.0.0', port=int(const.PORT))
