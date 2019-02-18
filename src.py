import hashlib
import urllib.parse

INPUT_SECRET = 'inputsecret' #very scret
OUTPUT_SECRET = 'outputsecret'

def get_params(url):
	qstring = url.split('?')[1]
	params = [param.split('=') for param in qstring.split('&')]
	return {param[0]: param[1] for param in params}

def urldecode(string):
	return urllib.parse.unquote(string, encoding='windows-1252')

def urlencode(string):
	return urllib.parse.quote(string, encoding='windows-1252')

def make_querystring(params):
	attr_names = ['B02K_VERS', 'B02K_TIMESTMP', 'B02K_IDNBR', 'B02K_STAMP', 'B02K_CUSTNAME', 'B02K_KEYVERS', 'B02K_ALG', 'B02K_CUSTID', 'B02K_CUSTTYPE']
	parts = [urldecode(params[attr]) for attr in attr_names]
	return f"{'&'.join(parts)}&{INPUT_SECRET}&"

def make_error(server, err):
	return f"{server}?error={urlencode(err)}"

def make_output(server, cust_name):
	name = [part.title() for part in cust_name.split('%20')]
	hash_source = f'firstname={name[0]}&lastname={name[1]}#{OUTPUT_SECRET}'
	hashed = hashlib.sha256(hash_source.encode('utf-8')).hexdigest()
	return f"{server}?{hash_source.split('#')[0]}&hash={hashed}"

def validate(url):
	try:
		server = url.split('?')[0]
		params = get_params(url)
	except:
		return make_error(server, 'Malformed URL')
	try:
		querystring = make_querystring(params)
	except KeyError as err:
		return make_error(server, f"Missing parameter: {err}")
	signature = hashlib.sha256(querystring.encode('utf-8')).hexdigest()
	if not params['B02K_MAC'] or signature.upper() != params['B02K_MAC']:
		return make_error(server, 'Incorrect signature')
	else:
		return make_output(server, params['B02K_CUSTNAME'])
