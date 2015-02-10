import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import resolve, Resolver404
from django.db import models
from django.http.request import validate_host, split_domain_port
from django.utils import timezone

import requests
from urlparse import urlparse

from bulbs.content.models import Content


def get_content_for_url(url, allowed_hosts=["*"]):

    parsed = urlparse(url)
    domain, port = split_domain_port(parsed.netloc)

    if validate_host(domain, allowed_hosts) is False:

        # Looks like the URL we were given isn't for this domain--let's try to resolve redirects
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            url = response.url
            parsed = urlparse(url)

            if validate_host(parsed.netloc, allowed_hosts) is False:
                # Looks like even after following the redirects, we're still fucked
                return

    try:
        match = resolve(parsed.path)
    except Resolver404:
        raise ObjectDoesNotExist
    if match:
        pk = match.kwargs.get('pk')
        if pk is None and len(match.args):
            pk = match.args[0]

        if pk:
            return Content.objects.get(pk=pk)

    # If we get here, something fucked up
    raise ObjectDoesNotExist


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
    access_token = models.CharField(max_length=510)
    allowed_hosts = models.CharField(null=True, blank=True, max_length=255)
    last_updated = models.IntegerField(null=True, blank=True)

    FACEBOOK_FIELDS = [
        "type", "created_time", "link", "name", "picture",
        "id", "description", "message", "caption", "status_type"
    ]

    def __unicode__(self):
        return self.name

    def poll(self):
        graph_url = "https://graph.facebook.com/{}/posts".format(self.page_id)
        params = {
            "access_token": self.access_token,
            "fields": ",".join(self.FACEBOOK_FIELDS)
        }
        response = requests.get(graph_url, params=params)
        response.raise_for_status()

        for data in response.json()["data"]:
            post, created = FacebookPost.objects.get_or_create(
                post_id=data["id"],
                page=self,
                defaults={"data": json.dumps(data)})

            if created is False:
                # Looks like we've come this far before
                break

            if "link" in data and post.content is None:
                post.content = get_content_for_url(data["link"], allowed_hosts=self.allowed_hosts)
                post.save()


class FacebookPost(models.Model):

    page = models.ForeignKey(FacebookPage, related_name="posts")
    post_id = models.CharField(max_length=255)
    content = models.ForeignKey(Content, null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    insights = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField()

    def update_insights(self):
        graph_url = "https://graph.facebook.com/{}/insights".format(self.post_id)
        params = {"access_token": self.page.access_token}
        response = requests.get(graph_url, params=params)
        response.raise_for_status()

        self.insights = json.dumps(response.json()["data"])
        self.last_updated = timezone.now()
        self.save()
