#!/usr/bin/env python3
"""Import this project's pilot-reading-v0.1 records; never claim a fresh PDF reading."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys
import literature as lit

FIELD_MAP = {'type': 'research_type', 'problem': 'research_question', 'data': 'data',
             'construction': 'construction', 'evidence': 'benchmark_evidence',
             'evaluation_sample': 'evaluation_sample', 'settings': 'settings',
             'metrics': 'metrics', 'results': 'findings', 'limits': 'author_limitations',
             'resources': 'resources'}


def migrate(library, source):
    path = Path(source).expanduser().resolve()
    source_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    pilot = lit.read_json(path)
    lit.require(pilot.get('schema_version') == 'pilot-reading-v0.1', 'Unsupported pilot format')
    conn = lit.connect(library, create=True)
    results = []
    try:
        conn.execute('BEGIN IMMEDIATE')
        for old in pilot['papers']:
            _, actual_sha = lit.file_info(old['source_path'])
            lit.require(actual_sha == old['sha256'], 'Original PDF changed: ' + old['paper_id'])
            lang = old.get('language', {})
            meta = {'title': old['title'], 'year': old['year_as_printed'],
                    'version': old['venue_or_version_as_printed'], 'page_count': old['page_count'],
                    'paper_language': lang.get('paper_main_text', ''), 'data_language': lang.get('benchmark_data_language', ''),
                    'title_zh': lang.get('translated_title_zh', ''),
                    'metadata_source': str(path) + '; inherited pilot; translation is an AI draft'}
            imported = lit.add(conn, old['source_path'], meta, old['paper_id'])
            r = lit.get(conn, imported['paper_id'])
            if r['coverage'].get('pilot_sha256') == source_sha:
                results.append({'paper_id': r['paper_id'], 'skipped': True})
                continue
            lit.require(not r['fields'] and not r['notes'] and not r['experiments'], 'Refusing to replace an existing reading: ' + r['paper_id'])
            before = copy.deepcopy(r)
            scope_notes = []
            for key, val in old['fields'].items():
                lit.require(key in FIELD_MAP, 'Unknown pilot field: ' + key)
                citations = []
                for item in val['evidence']:
                    citations.append({'pdf_page': item['pdf_page'], 'locator': item.get('locator', ''),
                                      'quote': item['quote'], 'check': 'unverified',
                                      'inherited_verification': item.get('verification'),
                                      'inherited_visual_check': item.get('page_visually_checked', False)})
                status = 'conflicting' if val['content_status'] == 'needs_reconciliation' else val['content_status']
                generated = {'label': val['label'], 'value': {'zh': val['value'], 'en': None},
                             'origin': 'author' if val['origin'] == 'paper_reported' else 'ai_inference',
                             'status': status, 'evidence': citations}
                r['fields'][FIELD_MAP[key]] = {'generated': generated, 'review': 'pending', 'review_note': '继承试读初稿，未在本次迁移重新核验原文'}
                if val.get('assistant_scope_note'):
                    scope_notes.append({'field': FIELD_MAP[key], 'note': val['assistant_scope_note']})
            if scope_notes:
                r['fields']['ai_appraisal'] = {'generated': {'value': scope_notes, 'origin': 'ai_inference', 'status': 'extracted', 'evidence': []}, 'review': 'pending', 'review_note': '继承试读的范围判断'}
            r['issues'] = copy.deepcopy(old.get('issues', []))
            r['coverage'] = {'mode': 'metadata_only', 'pages_read': [], 'import_method': 'pilot_migration',
                             'pilot_path': str(path), 'pilot_sha256': source_sha,
                             'inherited_reading_note': pilot.get('extraction_validation'),
                             'note': '仅迁移既有读书记录并核对文件哈希；本次未重新阅读PDF。'}
            r['tags'] = ['财报问答', '基准论文', '继承试读待核验']
            lit.save(conn, r, before)
            results.append({'paper_id': r['paper_id'], 'revision': r['revision'], 'fields': len(r['fields']), 'skipped': False})
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--library', required=True)
    p.add_argument('--input', required=True)
    a = p.parse_args()
    try:
        results = migrate(a.library, a.input)
        print(json.dumps({'ok': True, 'papers': results}, ensure_ascii=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, lit.sqlite3.Error) as exc:
        print(json.dumps({'ok': False, 'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    sys.exit(main())
