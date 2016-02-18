"""Custom search function to assist in customizing our special coverage searches."""
import six

from elasticsearch_dsl import filter as es_filter

from bulbs.content.custom_search import get_condition_filter
from bulbs.content.models import Content


class SearchParty(object):
    """Wrapper that searches for content from a group of SpecialCoverage objects."""

    def __init__(self, special_coverages, *args, **kwargs):
        """Store list of special_coverages class level."""
        self._special_coverages = special_coverages
        self._query = {}

    def search(self):
        """Return a search using the combined query of all associated special coverage objects."""
        es_query = Content.search_objects.search()
        # Get SpecialCoverage group filters.
        group_filter = self.get_group_filters()
        if group_filter:
            es_query = es_query.filter(es_filter.Bool(must=[group_filter]))
        # search_filter |= es_filter.Terms(pk=self.query.get("included_ids", []))
        # # # We don't care to pin things here since it shoudl be random ordering.
        # search_filter |= es_filter.Terms(pk=self.query.get("pinned_ids", []))
        # search_filter |= ~es_filter.Terms(pk=self.query.get("excluded_ids", []))
        return es_query

    def get_group_filters(self):
        """Return es OR filters to include all special coverage group conditions."""
        should_filters = []
        field_map = {
            "feature-type": "feature_type.slug",
            "tag": "tags.slug",
            "content-type": "_type"
        }
        for group_set in self.query.get("groups", []):
            for group in group_set:
                group_filter = es_filter.MatchAll()
                for condition in group.get("conditions", []):
                    group_filter &= get_condition_filter(condition, field_map=field_map)
                should_filters.append(group_filter)
        return es_filter.Bool(should=should_filters)

    @property
    def query(self):
        """Group the self.special_coverages queries and memoize them."""
        if not self._query:
            self._query.update({
                "excluded_ids": [],
                "included_ids": [],
                "pinned_ids": [],
                "groups": [],
            })
            for special_coverage in self._special_coverages:
                # Access query at dict level.
                query = getattr(special_coverage, "query", {})
                if "query" in query:
                    query = query.get("query")

                self._query.update({

                })
                self._query["excluded_ids"] += query.get("excluded_ids", [])
                self._query["included_ids"] += query.get("included_ids", [])
                self._query["pinned_ids"] += query.get("pinned_ids", [])
                self._query["groups"] += [query.get("groups", [])]
        return self._query


def second_slot_query_generator(query1, query2):
    """Returns the result of a different query at the 1st index of iteration.

    :param query1: Primary search that will be the default result set.
    :type  query1: Any iterable object; intended for djes.search.LazySearch and django.Querysets.
    :param query2: Secondard search that will return at the 1st index of iteration.
    :type  query2: Any iterable object; intended for djes.search.LazySearch and django.Querysets.
    """
    index = 0
    while True:
        result = None
        if index == 1:
            try:
                result = six.next(query2)
            except IndexError:
                pass
        if result is None:
            try:
                result = six.next(query1)
            except IndexError:
                break
        yield result
        index += 1
