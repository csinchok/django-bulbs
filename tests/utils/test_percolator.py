from django.core.management import call_command
from django.utils.six import StringIO

from bulbs.content.models import Content
from bulbs.sections.models import Section
from bulbs.special_coverage.models import SpecialCoverage
from bulbs.utils.percolator import (
    clean_deprecated_class_percolators, delete_percolator, get_deprecated_queries,
    get_percolator_class, get_query_id_list
)
from bulbs.utils.test import BaseIndexableTestCase


class PercolatorTests(BaseIndexableTestCase):
    def setUp(self):
        super(PercolatorTests, self).setUp()
        self.index = Content.search_objects.mapping.index
        self.doc_type = '.percolator',
        self.base_query = {
            'excluded_ids': [],
            'groups': [{
                'conditions': [{
                    'field': 'tag',
                    'type': 'any',
                    'values': [{
                        'name': '',
                        'value': ''
                    }]
                }],
            }],
            'included_ids': [],
            'pinned_ids': []
        }
        # Add bad data to be cleared out.
        query = self.base_query
        query['groups'][0]['conditions'][0]['values'][0] = {
            'name': 's-None',
            'value': 's-None'
        }
        Section(name='none section', query=query)._save_percolator()
        query = self.base_query
        query['groups'][0]['conditions'][0]['values'][0] = {
            'name': 's-1000',
            'value': 's-1000'
        }
        Section(name='1000 section', id=1000, query=query)._save_percolator()
        # Add bad data to be cleared out.
        query = self.base_query
        query['groups'][0]['conditions'][0]['values'][0] = {
            'name': 'special-None',
            'value': 'special-None'
        }
        SpecialCoverage(name='none special', query=query)._save_percolator()
        query = self.base_query
        query['groups'][0]['conditions'][0]['values'][0] = {
            'name': 'special-1000',
            'value': 'special-1000'
        }
        SpecialCoverage(name='1000 special', id=1000, query=query)._save_percolator()
        for i in range(2):
            query = self.base_query
            query['groups'][0]['conditions'][0]['values'][0] = {
                'name': 's-{}'.format(i),
                'value': 's-{}'.format(i)
            }

            section = Section.objects.create(name='section.{}'.format(i), query=query)
            section.save()
            special = SpecialCoverage.objects.create(
                name='special.{}'.format(i), query=query, active=True
            )
            special.save()

        q = {
            'query': {
                'filtered': {
                    'filter': {
                        'nested': {
                            'filter': {
                                'terms': {
                                    'tags.slug': ['recent']
                                }
                            },
                            'path': 'tags'
                        }
                    },
                    'query': {
                        'match_all': {}
                    }
                }
            }
        }
        self.es.index(index=self.index, doc_type=self.doc_type, body=q, id='recent')
        self.es.index(index=self.index, doc_type=self.doc_type, body=q, id='popular')
        Content.search_objects.refresh()

    def test_query_id_list(self):
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = [
            'section.1', 'section.2', 'section.1000', 'section.None', 'specialcoverage.1',
            'specialcoverage.2', 'specialcoverage.1000', 'specialcoverage.None', 'recent',
            'popular'
        ]
        self.assertItemsEqual(expected_list, id_list)

    def test_delete_percolator(self):
        delete_percolator(self.es, self.index, self.doc_type, 'section.None')
        Section.search_objects.refresh()
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = [
            'section.1', 'section.2', 'section.1000', 'specialcoverage.1', 'specialcoverage.2',
            'specialcoverage.1000', 'specialcoverage.None', 'recent', 'popular'
        ]
        self.assertItemsEqual(expected_list, id_list)

    def test_get_percolator_class(self):
        cls = get_percolator_class('section.1')
        self.assertEqual(cls, Section)
        cls = get_percolator_class('section.None')
        self.assertEqual(cls, Section)
        cls = get_percolator_class('section.')
        self.assertIsNone(cls)
        cls = get_percolator_class('specialcoverage.1')
        self.assertEqual(cls, SpecialCoverage)
        cls = get_percolator_class('specialcoverage.None')
        self.assertEqual(cls, SpecialCoverage)
        cls = get_percolator_class('specialcoverage.')
        self.assertIsNone(cls)
        cls = get_percolator_class('popular')
        self.assertIsNone(cls)
        cls = get_percolator_class('recent')
        self.assertIsNone(cls)

    def test_get_deprecated_queries(self):
        queries = get_deprecated_queries()
        expected_list = [
            'section.1000', 'section.None', 'specialcoverage.1000', 'specialcoverage.None'
        ]
        self.assertItemsEqual(expected_list, queries)

    def test_clean_deprecated_class_percolators_sections(self):
        clean_deprecated_class_percolators()
        Content.search_objects.refresh()
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = [
            'section.1', 'section.2', 'specialcoverage.1', 'specialcoverage.2', 'recent', 'popular'
        ]
        self.assertItemsEqual(expected_list, id_list)

    def test_call_clean_percolator_command(self):
        call_command('clean_percolator')
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = [
            'section.1', 'section.2', 'specialcoverage.1', 'specialcoverage.2', 'recent', 'popular'
        ]
        self.assertItemsEqual(expected_list, id_list)

    def test_call_clean_percolator_command_check(self):
        out = StringIO()
        call_command('clean_percolator', '--check', stdout=out)
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = [
            'section.1', 'section.2', 'section.1000', 'section.None', 'specialcoverage.1',
            'specialcoverage.2', 'specialcoverage.1000', 'specialcoverage.None', 'recent',
            'popular'
        ]
        self.assertItemsEqual(expected_list, id_list)
        output = out.getvalue()
        bad_queries = output.split('\n')
        expected_list = [
            'section.1000', 'section.None', 'specialcoverage.1000', 'specialcoverage.None'
        ]
        self.assertItemsEqual(expected_list, bad_queries[:-1])
