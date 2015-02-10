from django.core.exceptions import ObjectDoesNotExist
from elastimorphic.tests.base import BaseIndexableTestCase
from tests.utils import make_content

from bulbs.analytics.models import get_content_for_url, FacebookPage

from httmock import HTTMock, urlmatch


@urlmatch(path="/bad-redirect")
def bad_redirect(url, request):
    return {
        "status_code": 301,
        "headers": {
            "Location": "http://localhost/detail/123456/"
        }
    }


@urlmatch(path="/detail/123456/")
def content_404(url, request):
    return {
        "status_code": 404,
        "content": "Content not found!"
    }


@urlmatch(path="/fake-redirect")
def fake_redirect(url, request):
    return {
        "status_code": 301,
        "headers": {
            "Location": "http://localhost/detail/666/"
        }
    }


@urlmatch(path="/detail/666/")
def fake_content(url, request):
    return {
        "status_code": 200,
        "content": "Hello!"
    }


class URLResolutionTextCase(BaseIndexableTestCase):

    def test_url_resolution(self):
        test_content = make_content()

        test_url = "http://localhost{}".format(test_content.get_absolute_url())

        content = get_content_for_url(test_url)
        self.assertIsNotNone(content)
        self.assertEqual(test_content.id, content.id)

    def test_follow_redirects(self):
        test_content = make_content(id=666)

        with HTTMock(fake_redirect, fake_content):
            content = get_content_for_url("http://example.com/fake-redirect")
            self.assertIsNotNone(content)
            self.assertEqual(test_content.id, content.id)

    def test_url_nomatch(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_content_for_url("http://localhost/detail/1234567/")

        with self.assertRaises(ObjectDoesNotExist):
            with HTTMock(bad_redirect, content_404):
                get_content_for_url("http://example.com/bad-redirect")



