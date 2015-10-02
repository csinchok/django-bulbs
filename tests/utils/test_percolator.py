from bulbs.content.models import Content
from bulbs.sections.models import Section
from bulbs.special_coverage.models import SpecialCoverage
from bulbs.utils.percolator import (
    clean_deprecated_percolators, delete_percolator, get_query_id_list, object_exists
)
from bulbs.utils.test import BaseIndexableTestCase


class SectionPercolatorTests(BaseIndexableTestCase):
    def setUp(self):
        super(SectionPercolatorTests, self).setUp()
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
        for i in range(5):
            query = self.base_query
            query['groups'][0]['conditions'][0]['values'][0] = {
                'name': 's-{}'.format(i),
                'value': 's-{}'.format(i)
            }

            s = Section.objects.create(name='section.{}'.format(i), query=query)
            s.save()
        Section.search_objects.refresh()

    def test_query_id_list(self):
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = [
            'section.1', 'section.2', 'section.3', 'section.4', 'section.5', 'section.None',
            'section.1000'
        ]
        self.assertItemsEqual(expected_list, id_list)

    def test_section_object_exists_by_es_id(self):
        self.assertTrue(object_exists(Section, 'section.1'))
        self.assertTrue(object_exists(Section, 'section.2'))
        self.assertTrue(object_exists(Section, 'section.3'))
        self.assertTrue(object_exists(Section, 'section.4'))
        self.assertTrue(object_exists(Section, 'section.5'))
        self.assertFalse(object_exists(Section, 'section.None'))
        self.assertFalse(object_exists(Section, 'section.1000'))

    def test_section_object_exists_by_id(self):
        self.assertTrue(object_exists(Section, 1))
        self.assertTrue(object_exists(Section, 2))
        self.assertTrue(object_exists(Section, 3))
        self.assertTrue(object_exists(Section, 4))
        self.assertTrue(object_exists(Section, 5))
        self.assertFalse(object_exists(Section, None))
        self.assertFalse(object_exists(Section, 1000))

    def test_delete_percolator(self):
        delete_percolator(self.es, self.index, self.doc_type, 'section.None')
        Section.search_objects.refresh()
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = [
            'section.1', 'section.2', 'section.3', 'section.4', 'section.5', 'section.1000'
        ]
        self.assertItemsEqual(expected_list, id_list)

    def test_clean_deprecated_percolators_sections(self):
        clean_deprecated_percolators(Section)
        Section.search_objects.refresh()
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = ['section.1', 'section.2', 'section.3', 'section.4', 'section.5']
        self.assertItemsEqual(expected_list, id_list)


class SpecialCoveragePercolatorTests(BaseIndexableTestCase):
    def setUp(self):
        super(SpecialCoveragePercolatorTests, self).setUp()
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
        for i in range(5):
            query = self.base_query
            query['groups'][0]['conditions'][0]['values'][0] = {
                'name': 'special-{}'.format(i),
                'value': 'special-{}'.format(i)
            }

            s = SpecialCoverage.objects.create(
                name='special.{}'.format(i), active=True, query=query
            )
            s.save()
        Content.search_objects.refresh()

    def test_query_id_list(self):
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = [
            'specialcoverage.1', 'specialcoverage.2', 'specialcoverage.3', 'specialcoverage.4',
            'specialcoverage.5', 'specialcoverage.None', 'specialcoverage.1000'
        ]
        self.assertItemsEqual(expected_list, id_list)

    def test_specialcoverage_object_exists_by_es_id(self):
        self.assertTrue(object_exists(SpecialCoverage, 'specialcovearge.1'))
        self.assertTrue(object_exists(SpecialCoverage, 'specialcovearge.2'))
        self.assertTrue(object_exists(SpecialCoverage, 'specialcovearge.3'))
        self.assertTrue(object_exists(SpecialCoverage, 'specialcovearge.4'))
        self.assertTrue(object_exists(SpecialCoverage, 'specialcovearge.5'))
        self.assertFalse(object_exists(SpecialCoverage, 'specialcovearge.None'))
        self.assertFalse(object_exists(SpecialCoverage, 'specialcovearge.1000'))

    def test_specialcoverage_object_exists_by_id(self):
        self.assertTrue(object_exists(SpecialCoverage, 1))
        self.assertTrue(object_exists(SpecialCoverage, 2))
        self.assertTrue(object_exists(SpecialCoverage, 3))
        self.assertTrue(object_exists(SpecialCoverage, 4))
        self.assertTrue(object_exists(SpecialCoverage, 5))
        self.assertFalse(object_exists(SpecialCoverage, None))
        self.assertFalse(object_exists(SpecialCoverage, 1000))

    def test_delete_percolator(self):
        delete_percolator(self.es, self.index, self.doc_type, 'specialcoverage.None')
        Content.search_objects.refresh()
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = [
            'specialcoverage.1', 'specialcoverage.2', 'specialcoverage.3', 'specialcoverage.4',
            'specialcoverage.5', 'specialcoverage.1000'
        ]
        self.assertItemsEqual(expected_list, id_list)

    def test_clean_deprecated_percolators_special_coverage(self):
        clean_deprecated_percolators(SpecialCoverage)
        Content.search_objects.refresh()
        id_list = get_query_id_list(self.es, self.index, self.doc_type)
        expected_list = [
            'specialcoverage.1', 'specialcoverage.2', 'specialcoverage.3',
            'specialcoverage.4', 'specialcoverage.5'
        ]
        self.assertItemsEqual(expected_list, id_list)
