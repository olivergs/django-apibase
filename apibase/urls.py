# -*- coding: utf-8 -*-
"""

===============================================

.. module:: 
    :platform: django
    :synopsis: 
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django.conf.urls import url
from django.conf import settings

# Base URL patterns
urlpatterns=[]

# Debug URL patterns
if settings.TEST:
	debug_urlpatterns=[
		url(r'^jsonsignedtest/$', 'apibase.views.signed_request_test', name='signed_request_test'),
		url(r'^jsonencryptedtest/$', 'apibase.views.encrypted_request_test', name='encrypted_request_test'),
	]
	urlpatterns=debug_urlpatterns+urlpatterns
	
