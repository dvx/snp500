import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

SP500_COMPANIES_PAGE = 'List_of_S%26P_500_companies'
WIKIPEDIA_API_PARSE = 'https://en.wikipedia.org/w/api.php?action=parse&page={}&format=json'
WIKIPEDIA_API_REV = 'https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles={}&rvprop=ids&format=json'
PORT = os.getenv('PORT', default=80)
REDIS_URL = os.getenv('REDIS_URL')
EXPECTED_SYMBOLS = 505

print("environment variables loaded...")