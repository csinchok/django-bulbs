from elastimorphic.tests.base import BaseIndexableTestCase
from tests.utils import make_content


class URLResolutionTextCase(BaseIndexableTestCase):

    def test_url_resolution(self):
        test_content = make_content()

        test_content = content.get_absolute_url()
