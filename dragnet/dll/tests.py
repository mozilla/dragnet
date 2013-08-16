from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from nose.tools import eq_, ok_
from django.core.urlresolvers import reverse

from dragnet.dll.models import File


class DllTest(TestCase):

    def test_unauthenticated_user_redirected_from_create(self):
        url = reverse('dll.create')
        response = self.client.get(url)
        self.assertRedirects(
            response,
            '%s?%s=%s' % (
                reverse('users.login'),
                REDIRECT_FIELD_NAME,
                url,
            )
        )

    def test_unauthenticated_user_redirected_from_edit(self):
        sys_user, __ = User.objects.get_or_create(
            username='system',
            first_name='System',
        )

        myfile = File.objects.create(
            created_by=sys_user,
            modified_by=sys_user,
            file_name='abc.dll'
        )

        url = reverse('dll.edit', args=[myfile.pk])
        response = self.client.get(url)
        # when the user is unauthenticated, they are redirected from edit to
        # a read-only view.
        self.assertRedirects(response, reverse('dll.view', args=[myfile.pk]))
