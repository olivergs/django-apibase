# -*- coding: utf-8 -*-
"""
Utility functions for API base application
==========================================

.. module:: apibase.utils
    :platform: Django
    :synopsis: Utility functions for API base application
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports
import json, base64
import rsa

# PyEVO imports
from pyevo.http import nvp_request

def get_rsa_key(key):
	"""
	Gets an RSA key from its unicode pkcs1 representation

    :param key: Key contents
    :type key: :class:`unicode`
    :returns: :class:`rsa.PrivateKey` or :class:`rsa.PublicKey`

    .. note::
    	The return key type is defined by the "BEGIN RSA X KEY" that begins
    	key contents where X is PRIVATE or PUBLIC
	"""
	if not isinstance(key,(rsa.PrivateKey,rsa.PublicKey)):
		if 'BEGIN RSA PRIVATE KEY' in key:
			key=rsa.PrivateKey.load_pkcs1(key)
		else:
			key=rsa.PublicKey.load_pkcs1(key)
	return key

def json_signed_post_data(apikey,privkey,data):
	"""
	Prepares a signed request post data

    :param apikey: API key
    :type apikey: :class:`unicode`
    :param pubkey: Private key for data signing
    :type pubkey: :class:`unicode` or :class:`rsa.PrivateKey`
    :param data: Data that will be signed and sent
    :type data: :class:`dict`, :class:`list` -- Any JSON serializable
	:returns: :class:`dict` with POST data

    .. note::
    	Data will be converted to JSON to be signed
	"""
	key=get_rsa_key(privkey)
	# Convert data to JSON
	jsondata=json.dumps(data)
	# Generate signature
	signature=rsa.sign(jsondata,key,'SHA-1')
	# Encode signature in BASE64
	b64signature=base64.b64encode(signature)
	# Prepare data
	return {
		'key': apikey,
		'data': jsondata,
		'signature': b64signature,
	}

def json_encrypted_post_data(apikey,pubkey,data):
	"""
	Prepares an encrypted request post data

    :param apikey: API key
    :type apikey: :class:`unicode`
    :param pubkey: Private key for data encryption
    :type pubkey: :class:`unicode` or :class:`rsa.PrivateKey`
    :param data: Data that will be encrypted and sent
    :type data: :class:`dict`, :class:`list` -- Any JSON serializable
    :returns: :class:`dict` with POST data

    .. note::
    	Data will be converted to JSON to be encrypted
	"""
	key=get_rsa_key(pubkey)
	# Convert data to JSON
	jsondata=json.dumps(data)
	# Encrypt data
	encrypted=rsa.encrypt(jsondata,key)
	# Encode encrypted data in BASE64
	b64encrypted=base64.b64encode(encrypted)
	return {
		'key': apikey,
		'data': b64encrypted,
	}

def json_signed_request(url,apikey,privkey,data,*args,**kwargs):
	"""
	Send a signed request

    :param url: URL for the API request
    :type url: :class:`unicode`
    :param apikey: API key
    :type apikey: :class:`unicode`
    :param pubkey: Private key for data signing
    :type pubkey: :class:`unicode` or :class:`rsa.PrivateKey`
    :param data: Data that will be signed and sent
    :type data: :class:`dict`, :class:`list` -- Any JSON serializable
	:returns: server response contents

    .. note::
    	Data will be converted to JSON to be signed and sent to server
	"""
	# Prepare data
	postdata=json_signed_post_data(apikey,privkey,data)
	# Send request
	return nvp_request(url,postdata,method='POST',*args,**kwargs)

def json_encrypted_request(url,apikey,pubkey,data,json=True):
	"""
	Send an encrypted request

    :param url: URL for the API request
    :type url: :class:`unicode`
    :param apikey: API key
    :type apikey: :class:`unicode`
    :param pubkey: Private key for data encryption
    :type pubkey: :class:`unicode` or :class:`rsa.PrivateKey`
    :param data: Data that will be encrypted and sent
    :type data: :class:`dict`, :class:`list` -- Any JSON serializable
    :returns: server response contents

    .. note::
    	Data will be converted to JSON to be encrypted and sent to server
	"""
	postdata=json_encrypted_post_data(apikey,pubkey,data)
	# Send request
	return nvp_request(url,postdata,method='POST',json=True)
