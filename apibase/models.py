# -*- coding: utf-8 -*-
"""
API base application models module
===============================================

.. module:: apibase.models
    :platform: Django
    :synopsis: API base application models module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Python imports
import string
import rsa

# Django imports
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext,ugettext_lazy as _
from django.conf import settings

class APICredential(models.Model):
    """
    API credentials model class
    """

    class Meta:
        """
        Metadata for this model
        """
        verbose_name=_('API credential')
        verbose_name_plural=_('API credentials')

    # Fields
    key=models.CharField(_('Key'),max_length=50,unique=True,editable=False,
        help_text=_('API key'))
    public=models.TextField(_('Public key'),blank=True,null=True,editable=False,
        help_text=_('RSA public key'))
    private=models.TextField(_('Private key'),blank=True,null=True,editable=False,
        help_text=_('RSA private key'))    
    sources=models.TextField(_('Sources'),editable=False,
        help_text=_('Comma separated source IP addresses allowed to use this credentials'))
    description=models.CharField(_('Description'),max_length=50,blank=True,null=True,
        help_text=_('API key description'))
    user=models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_('User'),blank=True,null=True,
        help_text=_('User this key is bound'))

    def remove_begin_end_key(self,key):
        """
        Removes egin and end key markers from given key
        """

        return key.replace

    @property
    def private_key(self):
        """
        Returns an RSA private key object from PEM private key
        """
        return rsa.PrivateKey.load_pkcs1(self.private)

    @property
    def public_key(self):
        """
        Returns an RSA private key object from PEM private key
        """
        return rsa.PublicKey.load_pkcs1(self.public)

    @staticmethod
    def generate_keys():
        """
        Generate key for this api credentials
        """
        chars=string.digits + string.ascii_letters
        key=get_random_string(20,chars)
        pubkey, privkey = rsa.newkeys(settings.APIBASE_RSA_KEY_SIZE)
        pubkeypem=pubkey.save_pkcs1(format='PEM')
        privkeypem=privkey.save_pkcs1(format='PEM')
        return (key,pubkeypem,privkeypem)

    def sign(self,data):
        """
        Signs data with public key and returns data signature
        """
        return rsa.sign(data,self.private_key,'SHA-1')

    def verify(self,data,signature):
        """
        Verify signed data using private key
        """
        return rsa.verify(data,signature,self.public_key)

    def encrypt(self,data):
        """
        Encrypts data using public key
        """
        return rsa.encrypt(data, self.public_key)

    def decrypt(self,data):
        """
        Decrypts data using private key
        """
        return rsa.decrypt(data, self.private_key)

    def save(self,*args,**kwargs):
        """
        Save method overload
        """
        if not self.key:
            self.key,self.public,self.private=APICredential.generate_keys()
        # Call parent method
        super(APICredential,self).save(*args,**kwargs)

    # Methods
    def __unicode__(self):
        """
        Return model unicode representation
        """
        return self.key
