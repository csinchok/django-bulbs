from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.utils.http import urlencode

from bulbs.utils.test import BaseAPITestCase

from bulbs.ads.models import TargetingOverride


# TODO: factor out the user+permission stuff from ContentAPITestCase
class TestTargetingView(BaseAPITestCase):

    def test_get_fail(self):
        client = Client()
        nothing = client.get(reverse("targeting"))
        # you don't even get nothing without permission
        self.assertEqual(nothing.status_code, 403)
        # ok, have nothing, if that's your thing.
        client.login(username="admin", password="secret")
        self.give_permissions()
        nothing = client.get(reverse("targeting"))
        self.assertEqual(nothing.status_code, 404)

        param = urlencode({"url": "some/bull/shit"})
        url = "{0}?{1}".format(reverse("targeting"), param)
        also_nothing = client.get(url)
        self.assertEqual(also_nothing.status_code, 404)

    def test_get_success(self):
        TargetingOverride.objects.create(
            url="/content_list_two.html",
            targeting={"dfp_iscool": False}
        )

        client = Client()
        client.login(username="admin", password="secret")
        self.give_permissions()
        param = urlencode({"url": "/content_list_two.html"})
        url = "{0}?{1}".format(reverse("targeting"), param)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"dfp_iscool": false}')

    def test_post(self):
        client = Client()
        client.login(username="admin", password="secret")
        self.give_permissions()
        param = urlencode({"url": "/content_list_two.html"})
        url = "{0}?{1}".format(reverse("targeting"), param)
        response = client.post(
            url,
            content_type="application/json", data='{"dfp_iscool": false}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"dfp_iscool": false}')

        override = TargetingOverride.objects.get(url="/content_list_two.html")
        self.assertEqual(override.targeting, {"dfp_iscool": False})

    def test_bad_json(self):
        client = Client()
        client.login(username="admin", password="secret")
        self.give_permissions()

        param = urlencode({"url": "/content_list_two.html"})
        url = "{0}?{1}".format(reverse("targeting"), param)
        response = client.post(
            url, data="{'butts': 'poop'}", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def give_permissions(self):
        target_perm = Permission.objects.get(codename="change_targetingoverride")
        self.admin.user_permissions.add(target_perm)
