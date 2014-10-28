# -*- coding: utf-8 -*-
"""
API base application administration module
==========================================

.. module:: apibase.admin
    :platform: Django
    :synopsis: API base application administration module
.. moduleauthor:: (C) 2014 Oliver Gutiérrez
"""

# Django imports
from django.contrib import admin
from django.utils.translation import ugettext,ugettext_lazy as _

# Application imports
from sitetools.admin import BaseModelAdmin
from apibase.models import APICredential

class APICredentialAdmin(BaseModelAdmin):
	"""
	API credential administration class
	"""
	list_display = ('key','description','user','admin_public_key','admin_private_key',)
	list_filter = ('user',)
	search_fields = ('key','user__username','user__firstname','user__lastname','user__email')
	raw_id_fields = ('user',)
	actions = ('action_regenerate_keys',)

	def action_regenerate_keys(self, request, queryset):
		"""
		Key regeneration administration action
		"""
		for obj in queryset:
			key,obj.public,obj.private=APICredential.generate_keys()
			obj.save()
	action_regenerate_keys.short_description=_('Regenerate API public and private keys')

	def admin_public_key(self,obj):
		"""
		Administration site public key representation
		"""
		return """
			<button type="button" onclick="django.jQuery('#pubkey%s').show();django.jQuery(this).remove()">%s</button>
			<div id="pubkey%s" style="display: none;"><pre>%s</pre></div>
		""" % (obj.id,ugettext('Show key'),obj.id,obj.public)
	admin_public_key.allow_tags=True
	admin_public_key.short_description=_('Public key')

	def admin_private_key(self,obj):
		"""
		Administration site public key representation
		"""
		return """
			<button type="button" onclick="django.jQuery('#privkey%s').show();django.jQuery(this).remove()">%s</button>
			<div id="privkey%s" style="display: none;"><pre>%s</pre></div>
		""" % (obj.id,ugettext('Show key'),obj.id,obj.private)
	admin_private_key.allow_tags=True
	admin_private_key.short_description=_('Private key')

# Model registration
admin.site.register(APICredential,APICredentialAdmin)