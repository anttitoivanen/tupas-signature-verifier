import hashlib
import urllib.parse

class Validator:

	def __init__(self):
		pass

	def get_params(self, url):
		qstring = url.split('?')[1]
		params = [param.split('=') for param in qstring.split('&')]
		return {param[0]: param[1] for param in params}

	def urldecode(self, string):
		return urllib.parse.unquote(string, encoding='windows-1252')

	def urlencode(self, string):
		return urllib.parse.quote(string, encoding='windows-1252')

	def make_querystring(self, params, secret):
		attr_names = ['B02K_VERS', 
									'B02K_TIMESTMP', 
									'B02K_IDNBR', 
									'B02K_STAMP', 
									'B02K_CUSTNAME', 
									'B02K_KEYVERS', 
									'B02K_ALG', 
									'B02K_CUSTID', 
									'B02K_CUSTTYPE']
		parts = [self.urldecode(params[attr]) for attr in attr_names]
		return f"{'&'.join(parts)}&{secret}&"

	def make_error(self, server, err):
		return f"{server}?error={self.urlencode(err)}"

	def make_output(self, server, cust_name, secret):
		name = [part.capitalize() for part in cust_name.split('%20')]
		hash_source = f'firstname={name[0]}&lastname={name[1]}#{secret}'
		hashed = hashlib.sha256(hash_source.encode('utf-8')).hexdigest()
		return f"{server}?firstname={name[0]}&lastname={name[1]}&hash={hashed}"

	def validate(self, url, input_secret, output_secret):
		try:
			server = url.split('?')[0]
			params = self.get_params(url)
		except:
			return self.make_error(server, 'Malformed URL')
		try:
			querystring = self.make_querystring(params, input_secret)
		except KeyError as err:
			return self.make_error(server, f"Missing parameter: {err}")
		signature = hashlib.sha256(querystring.encode('utf-8')).hexdigest()
		if not params['B02K_MAC'] or signature.upper() != params['B02K_MAC']:
			return self.make_error(server, 'Incorrect signature')
		else:
			return self.make_output(server, params['B02K_CUSTNAME'], output_secret)
