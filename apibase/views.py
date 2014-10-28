# -*- coding: utf-8 -*-
"""
API base application views module
===============================================

.. module:: apibase.views
    :platform: Django
    :synopsis: API base application views module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports
import json

# Django imports
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.test.client import Client

# Application imports
from apibase.models import APICredential
from apibase.decorators import json_signed_view, json_encrypted_view
from apibase.utils import json_signed_post_data, json_encrypted_post_data
from apibase.tests import TEST_DATA

@csrf_exempt
@json_signed_view()
def signed_request_test(request):
    """
    Signed request test view

    :param request: Django HTTP request 
    :type request: :class:`django.http.HttpRequest`
    :returns: JSON signed data

    **POST Parameters**:
        **key**: API key
        **data**: JSON data
        **signature**: JSON data signature
    """
    if request.method == 'POST':
        # Decorators check data signing so data is verified
        return HttpResponse(json.dumps(request.json_data), content_type="text/plain")
    elif request.method =='GET':
        try:
            # Get credentials
            key=request.GET.get('key',None)
            credentials=APICredential.objects.get(key=key)
            client=Client()
            response=client.post(reverse('signed_request_test'),json_signed_post_data(key,credentials.private,TEST_DATA)).content
        except Exception, e:
            response='ERROR: %s' % e
        return HttpResponse(response,content_type="text/plain")
    else:
        return HttpResponseBadRequest()

@csrf_exempt
@json_encrypted_view()
def encrypted_request_test(request):
    """
    Encrypted request test view

    :param request: Django HTTP request 
    :type request: :class:`django.http.HttpRequest`
    :returns: JSON decrypted data

    **POST Parameters**:
        **key**: API key
        **data**: JSON data
    """
    if request.method == 'POST':
        # Decorators check data signing so data is verified
        return HttpResponse(json.dumps(request.json_data), content_type="text/plain")
    elif request.method =='GET':
        try:
            key=request.GET.get('key',None)
            credentials=APICredential.objects.get(key=key)
            client=Client()
            print "SENDING"
            response=client.post(reverse('encrypted_request_test'),json_encrypted_post_data(key,credentials.private,TEST_DATA)).content
            print response
        except Exception, e:
            print 'ERROR: %s' % e
            response='ERROR: %s' % e
        return HttpResponse(response,content_type="text/plain")
    else:
        return HttpResponseBadRequest()

