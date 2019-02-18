import unittest
from src import validate, urldecode

class TestValidation(unittest.TestCase):

	def test_decode(self):
		self.assertEqual(urldecode('FIRST%20LAST'), 'FIRST LAST')
		self.assertEqual(urldecode('V%C4IN%D6%20M%C4KI'), 'VÄINÖ MÄKI')		

	def test_simple(self):
		url = 'http://someserver.com/?B02K_VERS=0003&B02K_TIMESTMP=50020181017141433899056&B02K_IDNBR=2512408990&B02K_STAMP=20010125140015123456&B02K_CUSTNAME=FIRST%20LAST&B02K_KEYVERS=0001&B02K_ALG=03&B02K_CUSTID=9984&B02K_CUSTTYPE=02&B02K_MAC=EBA959A76B87AE8996849E7C0C08D4AC44B053183BE12C0DAC2AD0C86F9F2542'
		excpected_result = 'http://someserver.com/?firstname=First&lastname=Last&hash=4f6536ca2a23592d9037a4707bb44980b9bd2d4250fc1c833812068ccb000712'
		self.assertEqual(validate(url), excpected_result)

	def test_vaino(self):
		url = 'http://someserver.com/?B02K_VERS=0003&B02K_TIMESTMP=50020181017141433899056&B02K_IDNBR=2512408990&B02K_STAMP=20010125140015123456&B02K_CUSTNAME=V%C4IN%D6%20M%C4KI&B02K_KEYVERS=0001&B02K_ALG=03&B02K_CUSTID=9984&B02K_CUSTTYPE=02&B02K_MAC=D097F084296A5504BF8AEFA839B5BEC4453F5EFAD67FCB543C0EE554824151EF'
		print(validate(url))

	def test_invalid_url(self):
		fakeurl = 'foobar'
		excpected_result = 'foobar?error=Malformed%20URL'
		self.assertEqual(validate(fakeurl), excpected_result)

	def test_missing_parameter(self):
		url = 'http://someserver.com/?B02K_TIMESTMP=50020181017141433899056&B02K_IDNBR=2512408990&B02K_STAMP=20010125140015123456&B02K_CUSTNAME=FIRST%20LAST&B02K_KEYVERS=0001&B02K_ALG=03&B02K_CUSTID=9984&B02K_CUSTTYPE=02&B02K_MAC=EBA959A76B87AE8996849E7C0C08D4AC44B053183BE12C0DAC2AD0C86F9F2542'
		excpected_result = 'http://someserver.com/?error=Missing%20parameter%3A%20%27B02K_VERS%27'
		self.assertEqual(validate(url), excpected_result)

	def test_invalid_signature(self):
		url = 'http://someserver.com/?B02K_VERS=0003&B02K_TIMESTMP=50020181017141433899056&B02K_IDNBR=2512408990&B02K_STAMP=20010125140015123456&B02K_CUSTNAME=FIRST%20LAST&B02K_KEYVERS=0001&B02K_ALG=03&B02K_CUSTID=9984&B02K_CUSTTYPE=02&B02K_MAC=EBA959A76B87AE8996849E7C0C08D4AC44B053183BE12C0DAC2AD0C86F9F2543'
		excpected_result = 'http://someserver.com/?error=Incorrect%20signature'
		self.assertEqual(validate(url), excpected_result)


if __name__ == '__main__':
	unittest.main()