# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
# 
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
# 
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
# 
# The Original Code is Mozilla Sheriff Duty.
# 
# The Initial Developer of the Original Code is Mozilla Corporation.
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
# 
# Contributor(s):
# 
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
# 
# ***** END LICENSE BLOCK *****

import logging
from django.contrib.auth.models import User
from django_auth_ldap.backend import LDAPBackend

logger = logging.getLogger("authentication")

class MozillaLDAPBackend(LDAPBackend):
    """Overriding this class so that I can transform emails to usernames.

    At Mozilla we use email addresses as the username but in django I want,
    for example:
        INPUT:
            username -> pbengtsson@mozilla.com
        OUTPUT:
            username -> pbengtsson
            email -> pbengtsson@mozilla.com

    I can map (in settings.AUTH_LDAP_USER_ATTR_MAP):
        'username' -> 'uid'
        and
        'email -> 'mail

    But that means that the second time a user logs in, it's not going to
    find a username that is 'pbengtsson@mozilla.com' so it'll go ahead and
    create it again and you'll end up with duplicates once the attribute
    conversion is done.

    The other thing that this backend accomplishes is to change username
    entirely. Suppose, for example, that your mozilla LDAP email is
    'pbengtsson@mozilla.com' but you prefer your own custom alias of
    'peterbe'. What it does then, is looking at existing users that match
    the *email address* and returns the username for that one.
    """

    def get_or_create_user(self, username, ldap_user):
        """
        This must return a (User, created) 2-tuple for the given LDAP user.
        username is the Django-friendly username of the user. ldap_user.dn is
        the user's DN and ldap_user.attrs contains all of their LDAP attributes.
        """
        # users on this site can't change their email but they can change their
        # username
        
        logger.info("Attempting LDAP auth of %s", username)
        
        if ldap_user.attrs.get('mail'):
            for user in (User.objects
              .filter(email__iexact=ldap_user.attrs.get('mail')[0])):
                return (user, False)
                
        # use the default from django-auth-ldap
        return User.objects.get_or_create(
           username__iexact=username,
           defaults={'username': username.lower()}
        )


    def ldap_to_django_username(self, username):
        """Allow users to use a different username"""
        try:
            return User.objects.get(email=username).username
        except User.DoesNotExist:
            return username.split('@')[0]
