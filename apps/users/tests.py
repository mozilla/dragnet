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

import re
from urlparse import urlparse
import datetime
from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from nose.tools import eq_, ok_

try:
    import ldap
    from users.auth.backends import MozillaLDAPBackend
except ImportError:
    MozillaLDAPBackend = None


class UsersTest(TestCase):

    def test_login(self):
        url = reverse('users.login')
        response = self.client.get(url)
        eq_(response.status_code, 200)

        mortal = User.objects.create(
          username='mortal',
          first_name='Mortal',
          last_name='Joe'
        )
        mortal.set_password('secret')
        mortal.save()

        response = self.client.post(url, {'username': 'mortal',
                                          'password': 'wrong'})
        eq_(response.status_code, 200)
        ok_('errorlist' in response.content)

        response = self.client.post(url, {'username': 'mortal',
                                          'password': 'secret'})
        eq_(response.status_code, 302)
        path = urlparse(response['location']).path
        eq_(path, settings.LOGIN_REDIRECT_URL)

        response = self.client.get('/')
        eq_(response.status_code, 200)
        ok_('Mortal' in response.content)

        url = reverse('users.logout')
        response = self.client.get(url)
        eq_(response.status_code, 302)
        path = urlparse(response['location']).path
        eq_(path, settings.LOGOUT_REDIRECT_URL)

        response = self.client.get('/')
        eq_(response.status_code, 200)
        ok_('Mortal' not in response.content)

    def _get_all_inputs(self, html):
        _input_regex = re.compile('<input (.*?)>', re.M | re.DOTALL)
        _attrs_regex = re.compile('(\w+)="([^"]+)"')
        all_attrs = {}
        for input in _input_regex.findall(html):
            attrs = dict(_attrs_regex.findall(input))
            all_attrs[attrs.get('name', attrs.get('id', ''))] = attrs
        return all_attrs

    def test_login_next_redirect(self):
        url = reverse('users.login')
        response = self.client.get(url, {'next': '/foo/bar'})
        eq_(response.status_code, 200)
        attrs = self._get_all_inputs(response.content)
        ok_(attrs[REDIRECT_FIELD_NAME])
        eq_(attrs[REDIRECT_FIELD_NAME]['value'], '/foo/bar')

        mortal = User.objects.create_user(
          'mortal', 'mortal', password='secret'
        )
        mortal.set_password('secret')
        mortal.save()

        response = self.client.post(url, {'username': 'mortal',
                                          'password': 'secret',
                                          'next': '/foo/bar'})
        eq_(response.status_code, 302)
        path = urlparse(response['location']).path
        eq_(path, '/foo/bar')

    def test_login_failure(self):
        url = reverse('users.login')
        mortal = User.objects.create(
          username='mortal',
          first_name='Mortal',
          last_name='Joe',
          email='mortal@mozilla.com',
        )
        mortal.set_password('secret')
        mortal.save()

        response = self.client.post(url, {'username': 'mortal',
                                          'password': 'xxx'})
        eq_(response.status_code, 200)
        ok_('errorlist' in response.content)

        response = self.client.post(url, {'username': 'xxx',
                                          'password': 'secret'})
        eq_(response.status_code, 200)
        ok_('errorlist' in response.content)

    def test_login_rememberme(self):
        url = reverse('users.login')
        mortal = User.objects.create(
          username='mortal',
          first_name='Mortal',
          last_name='Joe'
        )
        mortal.set_password('secret')
        mortal.save()

        response = self.client.post(url, {'username': 'mortal',
                                          'password': 'secret',
                                          'rememberme': 'yes'})
        eq_(response.status_code, 302)
        expires = self.client.cookies['sessionid']['expires']
        date = expires.split()[1]
        then = datetime.datetime.strptime(date, '%d-%b-%Y')
        today = datetime.datetime.today()
        days = settings.SESSION_COOKIE_AGE / 24 / 3600
        eq_((then - today).days + 1, days)

    def test_login_by_email(self):
        url = reverse('users.login')

        mortal = User.objects.create(
          username='mortal',
          email='mortal@hotmail.com',
          first_name='Mortal',
          last_name='Joe'
        )
        mortal.set_password('secret')
        mortal.save()

        response = self.client.post(url, {'username': 'Mortal@hotmail.com',
                                          'password': 'secret'})
        eq_(response.status_code, 302)

        response = self.client.get('/')
        eq_(response.status_code, 200)
        ok_('Mortal' in response.content)

    def test_changing_your_username(self):
        url = reverse('users.settings')
        response = self.client.get(url)
        eq_(response.status_code, 302)
        path = urlparse(response['location']).path
        eq_(path, settings.LOGIN_URL)

        mortal = User.objects.create(
          username='mortal',
          email='mortal@hotmail.com',
          first_name='Mortal',
          last_name='Joe'
        )
        mortal.set_password('secret')
        mortal.save()
        assert self.client.login(username='mortal', password='secret')

        url = reverse('users.settings')
        response = self.client.get(url)
        eq_(response.status_code, 200)

        ok_('value="%s"' % mortal.username in response.content)

        User.objects.create_user(
          'maxpower',
          'maxpower@mozilla.com',
          password='secret',
        )

        response = self.client.post(url, {'username':' Maxpower '})
        eq_(response.status_code, 200)
        ok_('errorlist' in response.content)

        response = self.client.post(url, {'username':'homer   '})
        eq_(response.status_code, 302)

        ok_(User.objects.get(username='homer'))
        ok_(not User.objects.filter(username='mortal').exists())

        # stupid but I should be able to save my own username twice
        response = self.client.post(url, {'username':'homer'})
        ok_(User.objects.get(username='homer'))

        response = self.client.post(url, {'username':'Homer'})
        ok_(User.objects.get(username='Homer'))

    def test_mozilla_ldap_backend_basic(self):
        if MozillaLDAPBackend is None:
            return
        back = MozillaLDAPBackend()
        class LDAPUser:
            def __init__(self, attrs):
                self.attrs = attrs
        ldap_user = LDAPUser({'mail':['mail@peterbe.com']})
        user, created = back.get_or_create_user('peter', ldap_user)
        ok_(created)
        ok_(user)
        eq_(user.username, 'peter')

        peppe = User.objects.create_user(
          'peppe',
          'mail@peterbe.com',
        )
        user, created = back.get_or_create_user('peter', ldap_user)
        ok_(not created)
        eq_(user, peppe)

        username = back.ldap_to_django_username('mail@peterbe.com')
        eq_(username, 'peppe')
        username = back.ldap_to_django_username('lois@peterbe.com')
        eq_(username, 'lois')

    def test_login_username_form_field(self):
        url = reverse('users.login')
        response = self.client.get(url)
        eq_(response.status_code, 200)
        html = response.content.split('<form')[1].split('</form')[0]
        inputs = self._get_all_inputs(html)
        input = inputs['username']
        eq_(input['autocorrect'], 'off')
        eq_(input['spellcheck'], 'false')
        eq_(input['autocapitalize'], 'off')
        eq_(input['type'], 'email')
