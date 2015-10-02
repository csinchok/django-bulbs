import re

from elasticsearch_dsl.connections import connections

from bulbs.content.models import Content
from bulbs.sections.models import Section
from bulbs.special_coverage.models import SpecialCoverage


PERCOLATOR_PATTERNS = {
    'section.(\w+)': Section,
    'specialcoverage.(\w+)': SpecialCoverage
}


def get_query_id_list(es, index, doc_type):
    """Searches an elasticsearch index for all results of a given doc_type"""

    results = es.search(index=index, doc_type=doc_type)
    results_hits = results.get('hits', None)

    if results_hits is None:
        raise KeyError('No queries matched in the index {}'.format(index))

    hits = results_hits.get('hits', None)
    if hits is None:
        raise KeyError('No queries matched in the index {}'.format(index))

    _ids = [hit.get('_id') for hit in hits if hit.get('_id', None)]
    return _ids


def delete_percolator(es, index, doc_type, es_id):
    es.delete(index=index, doc_type='.percolator', id=es_id, refresh=True, ignore=404)


def get_percolator_class(es_id):
    for pattern, model in PERCOLATOR_PATTERNS.items():
        if re.match(pattern, es_id):
            return model
    return None


def class_percolator_is_valid(cls, es_id):
    id = es_id.split('.')[-1]
    if not str(id).isdigit():
        return False
    return cls.objects.filter(id=int(id)).exists()


def get_deprecated_queries():
    bad_queries = list()
    index = Content.search_objects.mapping.index
    doc_type = '.percolator'
    es = connections.get_connection('default')
    es_ids = get_query_id_list(es, index, doc_type)
    for es_id in es_ids:
        cls = get_percolator_class(es_id)
        if cls and not class_percolator_is_valid(cls, es_id):
            bad_queries.append(es_id)
    return bad_queries


def clean_deprecated_class_percolators():
    index = Content.search_objects.mapping.index
    doc_type = '.percolator'
    es = connections.get_connection('default')
    bad_queries = get_deprecated_queries()
    for es_id in bad_queries:
        delete_percolator(es, index, doc_type, es_id)
