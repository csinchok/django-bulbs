# django-bulbs Change Log

## Version 0.7.13

- Add Glance JSON feed for content ingestion: `/feeds/glance.json`

## Version 0.7.12

- Reduce RSS view caching from 10 to 5 min (per social squad)

## Version 0.7.11

- Remove redundant ES_URLS setting, just use ES_CONNECTIONS. Eventually all client projects can stop using ES_URLS too. 
- Example app checks ELASTICSEARCH_HOST env variable (useful for using docker-based ES served inside VM)

## Version 0.7.10

- Added `special_coverage` object to SpecialCoverageView context

## Version 0.7.9

- Added SpecialCoverageView to /bulbs/special_coverage/views for Special Coverage reuse

## Version 0.7.8

- Hotfix for contribution csv & api discrepencies with publish filters.

## Version 0.7.6

- Add `Content.evergreen` boolean column to indicate "always fresh" content

## Version 0.7.5

- Improved special coverage percolator retrieval logging

## Version 0.7.3

- Fix special coverage migration to grab model directly so that custom `SpecialCoverage.save()` method is called and triggers `_save_percolator`
- Campaign.save() triggers `SpecialCoverage._save_percolator()` via Celery task
- Install: Celery is now a regular (non-dev) requirement
- Bump min DJES dependency to reflect latest requirements

## Version 0.7.1

- Fix `Content.percoloate_special_coverage()` to ignore non-special-coverage results (ex: Sections)
- Fix `Content.percoloate_special_coverage()` to filter out entries without `start_date` fields (prevents search failure if one entry in shard was missing field)

## Version 0.7.0

- Added `Content.percolate_special_coverage()` containing new Special Coverage ordering rules to be shared by all client sites
- Fixed `SpecialCoverage._save_percolator()` to *always* save to percolator. This fixes regression in **0.6.49** with switch from `active` boolean flag to `is_active` property based on start/end dates, which would cause inclusion in percolator based on when SpecialCoverage was last saved. This fix requires percolator retrieval to filter active Special Coverage by start/end dates, and is the reason for the breaking minor version change. Easiest to just use the new `Content.percolate_special_coverage()` method instead of site-specific queries.

## Version 0.6.43

- Added `instant_article` flag to content model to set whether or not content eligible for Instant Articles RSS Feed
