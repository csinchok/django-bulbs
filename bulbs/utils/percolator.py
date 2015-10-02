import re

from elasticsearch_dsl.connections import connections

from bulbs.content.models import Content
# from bulbs.sections.models import Section


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


def object_exists(cls, id):
    if not str(id).isdigit():
        pattern = '(\w+)\.(\d+)'
        if re.match(pattern, str(id)):
            id = int(id.split('.')[-1])
            return object_exists(cls, id)
        return False
    return cls.objects.filter(id=int(id)).exists()


def clean_deprecated_percolators(cls):
    index = Content.search_objects.mapping.index
    doc_type = '.percolator'

    if not hasattr(cls, 'es_id'):
        raise TypeError('The provided class does not store a query in the Percolator.')

    es = connections.get_connection('default')
    _ids = get_query_id_list(es, index, doc_type)
    for _id in _ids:
        if not object_exists(cls, _id):
            delete_percolator(es, index, doc_type, _id)
