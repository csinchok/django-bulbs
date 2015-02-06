import json

from django.conf import settings
from django.core.urlresolvers import resolve
from django.db import models

from django.http.request import validate_host, split_domain_port

import requests
from urlparse import urlparse

from bulbs.content.models import Content


def get_content_for_url(url, allow_redirects=True):

    parsed = urlparse(url)
    domain, port = split_domain_port(parsed.netloc)
    if validate_host(domain, settings.ALLOWED_HOSTS) is False:

        # Looks like the URL we were given isn't for this domain—let's try to resolve redirects
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            url = response.url
            parsed = urlparse(url)

            if validate_host(parsed.netloc, settings.ALLOWED_HOSTS) is False:
                # Looks like even after following the redirects, we're still fucked
                return

    match = resolve(parsed.path)
    if match:
        pk = match.kwargs.get('pk')
        if pk is None and len(match.args):
            pk = match.args[0]

        if pk:
            return Content.objects.get(pk=pk)
    return None


class SocialAccount(models.Model):

    last_checked = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def poll(self):
        """Polls Facebook, Twitter, etc for posts made since the last check"""
        raise NotImplemented("You must implement this")


class TwitterAccount(SocialAccount):
    handle = models.CharField(max_length=255)

    def __unicode__(self):
        return self.handle


class FacebookPage(SocialAccount):
    name = models.CharField(max_length=255)
    page_id = models.IntegerField()

    def __unicode__(self):
        return self.name

    def poll(self):
        response = requests.get("https://graph.facebook.com/{}/posts".format(self.page_id))

        for data in response.json()["data"]:
            post, created = FacebookPost.objects.get_or_create(
                post_id=data["id"],
                page=self,
                defaults={"data": json.dumps(data)})

            if created is False:
                # Looks like we've come this far before
                break

            post.data = json.dumps(data)
            post.content = get_content_for_url(data["link"])


class FacebookPost(models.Model):

    page = models.ForeignKey(FacebookPage)
    post_id = models.CharField(max_length=255)
    content = models.ForeignKey(Content, null=True, blank=True)
    data = models.TextField(null=True, blank=True)
