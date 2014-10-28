# -*- coding: utf-8 -*-
"""
apibase tests module
================================

.. module:: apibase.tests
    :platform: Django
    :synopsis: apibase tests module
.. moduleauthor:: (C) 2014
"""

# Python imports
import json

# Django imports
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client

# Application imports
from apibase.models import APICredential

TEST_DATA=[u'test1',u'test2',1,2,3,True,False]

TEST_KEY='KZmfXWLZL4slzcjQlDui'

TEST_PUBKEY="""-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAgyrAlVlHKQbUShLoC2UVH8hmSwEQlJM+TXph5GNmyueJNw7bzkc+
LC+NZfUR9L2IEQK3tVTaDntqluTqQaQQ/Nh8kLNk8/YdE6YwWO9UBV2D643MXIxf
8YT8lrlzHrbRWc4daWYiaNTR3oX4hO6ysld3rM5PC+OHJR7y3Rl4LHUa+TA8pWgp
4otluShz+DPj6mJhjdmA+8OMiQzW0CQZiTlkEjYfJ0tvhXh1g8g4vdkEw2QlLt7N
SSWm7fHuoDsCzcB0EvDuOrI4lrC8CUEdgrI3sJU2QE7JyQ7Yl9fAzBPM7vgGXWqg
gdxUxKchPpj2gbWviT+9y2/kv/91Jpf1IQIDAQAB
-----END RSA PUBLIC KEY-----"""

TEST_PRIVKEY="""-----BEGIN RSA PRIVATE KEY-----
MIIEqQIBAAKCAQEAgyrAlVlHKQbUShLoC2UVH8hmSwEQlJM+TXph5GNmyueJNw7b
zkc+LC+NZfUR9L2IEQK3tVTaDntqluTqQaQQ/Nh8kLNk8/YdE6YwWO9UBV2D643M
XIxf8YT8lrlzHrbRWc4daWYiaNTR3oX4hO6ysld3rM5PC+OHJR7y3Rl4LHUa+TA8
pWgp4otluShz+DPj6mJhjdmA+8OMiQzW0CQZiTlkEjYfJ0tvhXh1g8g4vdkEw2Ql
Lt7NSSWm7fHuoDsCzcB0EvDuOrI4lrC8CUEdgrI3sJU2QE7JyQ7Yl9fAzBPM7vgG
XWqggdxUxKchPpj2gbWviT+9y2/kv/91Jpf1IQIDAQABAoIBAA1p29PqE1rgtej1
UgGITsa3Sa615yoqfJ6Tu1sNxz9Muj2FKXlI09TU8BLTIwjyMO38ZykGCl6cxGO1
+TbJPmt9ABAUKGjCbGrL/fm6T89Upt7520JDoLQkM2h+goVLkNEsQNm8dhxeVy/4
Z1fAyUlvpG9pka/Xjq6qVcanJYbbD1LcDFirl0dfyTwvq/mSgZWrze6DE35Uyy39
NWZ1EtDU44NEuostX2x7HAF0ZQoykC5UeUedw19OyTrqjCfxLouPLi5GTbOEe54s
FBCye5RTPJ7QNm6xn/x4yckejMexufA4CWjGAzZGrZnPY3H55/H/ltgkgV3FLwY5
M5lyIAECgYkA1Xp0ApMB1moFbtxiqdcXW6nIis1gS09aYCsNW12KQM4d6g8f0cGE
Yh/Z9Z1SnxpjiA+7cmZigCMCIPaiHQVwJB/Z6WSKn3FzwIA9EYd3a9IZTKbzceCd
8p2rC2n7QIPkMH+aqwJgJt5elHvzCGfQp6fBZ9rW4xJPr5heHjQCYXESvz8nOpEH
oQJ5AJ1LIkAt+/F68RE5EJpK3Sw54Oe8gcQ+S40wQ9rPvoL+7pFtRO7/A2/J6kpi
mS5uI8tWilQhNw2btH1+YR3Vd+5J0Pas+6msmuWu3kfUv3c33qkhR86omadZpwiU
j8fpbwb48weGbagKD8h8vpINrlkWx/siqFn9gQKBiB0Bw4uqAADrbQuQRJPBVzos
SsSZfXEeOjCBCRKWFjgSCbyJC5DL07oli8807koSIt4VDSpRQScaGqrx+DsrRv6R
mWF+ONvLZagNhL7CAncTGD7zHHcnxy51QA2P/ATbJwF0BUchToFZi85vPSmyOYbe
Y4hCExrNnShF8tv1wzEMVTjJUwJBPKECeAiVKPFHkQ/EHZNLAdTpcNgQ8Gy0pIAI
xiaWE53E6ChNsMbOp4xC7fUTl20npCQcbmeR+UpN5asga+DNHI98LmcaMATFu5Wu
jWUq/YX93dSrf8LKxhhIqtmu0qZtNMs7uYsv2lL2ytT4d5QA+oUNqg3CaHcTlQwU
AQKBiQCl1X9bSgJhv4uonYbc1TxREzGhA3JZalFhRxTSuGBBmbzNZJGdF/VcH6fz
lfXQ97Ts51Uh5g1o9qeMsWLcYV/FCz3IHZ40MMW7n1ZBDmXD9Vlm/zSsrihRwTLi
0ZSrdgIjLlF0RlOaXAIOLmPLV99kv3+r0Gaznbg4zDmuY52Wmi6rogzAipKl
-----END RSA PRIVATE KEY-----"""

class APIBaseTestCase(TestCase):
	"""
	Test case for template rendering API
	"""
	TEMPLATE_CONTENT='{% for num in nums %}{{ num }},{% endfor %}{{ eight }}'
	
	client=Client()

	def setUp(self):
		"""
		Test case setup
		"""
		# Setup an API key
		self.api=APICredential(key=TEST_KEY,public=TEST_PUBKEY,private=TEST_PRIVKEY)
		self.api.save()

	def test_signed_request(self):
		"""
		Test signed request
		"""
		# Get signed request test view
		response=self.client.get(reverse('signed_request_test') + '?key=%s' % self.api.key)
		# Check response
		self.assertEqual(json.loads(response.content),TEST_DATA)

	def test_encrypted_request(self):
		"""
		Test signed request
		"""
		# Get signed request test view
		response=self.client.get(reverse('signed_request_test') + '?key=%s' % self.api.key)
		# Check response
		self.assertEqual(json.loads(response.content),TEST_DATA)