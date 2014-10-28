# -*- coding: utf-8 -*-
"""
API base view decorators module
===============================================

.. module:: apibase.decorators
    :platform: Django
    :synopsis: API base view decorators module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports
import base64, json
from functools import wraps

# Django imports
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.decorators import available_attrs

# Application imports
from sitetools.utils import get_client_ip
from apibase.models import APICredential

def apibase_view(view_func):
    """
    Decorator for views that checks that the request is an AJAX request, showing a
    404 error page if it is not.

    # TODO: Sources checking
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.method=='POST':
            key=request.POST.get('key',None)
            try:
                request.credentials=APICredential.objects.get(key=key)
            except:
                return HttpResponse(status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def json_signed_view(errorcode=403,redirect_url=None):
    """
    Decorator to verify JSON signed requests.

    :param errorcode: Error code to use if data can not be decrypted
    :type errorcode: HTTP error code
    :param redirect_url: URL to redirect if data can not be decrypted
    :type redirect_url: An absolute or relative URL
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        @apibase_view
        def _wrapped_view(request, *args, **kwargs):
            if request.method=='POST':
                # Get signature parameter
                b64signature=request.POST.get('signature',None)
                # Get signed data
                data=request.POST.get('data',None)
                # Check signature
                if not b64signature or not data:
                    return HttpResponse(status=400)
                try:
                    # Decode signature
                    signature=base64.b64decode(b64signature)
                    # Verify data
                    request.credentials.verify(data,signature)
                    request.json_data=json.loads(data)
                except:
                    if redirect_url is not None:
                        return HttpResponseRedirect(redirect_url)
                    else:
                        return HttpResponse(status=errorcode)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def json_encrypted_view(errorcode=403,redirect_url=None):
    """
    Decorator to decrypt JSON encrypted requests.
    
    :param errorcode: Error code to use if data can not be verified
    :type errorcode: HTTP error code
    :param redirect_url: URL to redirect if data can not be verified
    :type redirect_url: An absolute or relative URL
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        @apibase_view
        def _wrapped_view(request, *args, **kwargs):
            if request.method=='POST':
                # Get encrypted data
                b64data=request.POST.get('data',None)
                # Check data
                if not b64data:
                    return HttpResponse(status=400)
                try:
                    # Decode data
                    data=base64.b64decode(b64data)
                    # Decrypt data
                    request.json_data=json.loads(request.credentials.decrypt(data))
                except:
                    if redirect_url is not None:
                        return HttpResponseRedirect(redirect_url)
                    else:
                        return HttpResponse(status=errorcode)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
