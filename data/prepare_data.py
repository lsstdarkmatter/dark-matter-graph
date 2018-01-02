#!/usr/bin/env python
import os
import json
from collections import OrderedDict
from itertools import combinations
import argparse
import yaml
import requests
try:
    from html import escape
except ImportError:
    from cgi import escape

__all__ = ['prepare_data_from_yaml', 'main']

_ads_url = 'http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?bibcode={}&data_type=Custom&format=%251m%20(%25y)%3A%3A%3A%25r&nocookieset=1'

def format_reference(bibcodes, use_ads=True):
    if use_ads:
        results = requests.get(_ads_url.format(requests.utils.quote(','.join(bibcodes)))).text.strip().split('\n\n')
        assert results[0] == 'Query Results from the ADS Database', 'something went wrong when querying ADS about {}'.format(bibcodes)
        assert len(results) == len(bibcodes) + 2, 'something went wrong when querying ADS about {}'.format(bibcodes)
        results = {u: t for t, _, u in (r.strip().partition(':::') for r in results[2:])}
    else:
        results = {}
    return [{'text': escape(results.get(u, u)), 'ads': escape(requests.utils.quote(u))} for u in bibcodes]


def prepare_data_from_yaml(yaml_file, use_ads):
    with open(yaml_file) as f:
        d = yaml.load(f)

    nodes = OrderedDict()
    for i, category_obj in enumerate(d['Categories']):
        category_key = category_obj['key']
        del category_obj['key']
        if 'title' not in category_obj:
            category_obj['title'] = category_key

        for j, node_obj in enumerate(d[category_key]):
            node_key = node_obj['key']
            del node_obj['key']
            if node_key in nodes:
                raise ValueError('{} repeatedly defined!'.format(node_key))
            if 'label' not in node_obj:
                node_obj['label'] = node_key
            node_obj['category'] = i
            node_obj['index'] = j
            node_obj['paths'] = []
            if 'references' in node_obj:
                node_obj['references'] = format_reference(node_obj['references'], use_ads)
            nodes[node_key] = node_obj

    nodes_keys = list(nodes.keys())
    category_indices = tuple(range(len(d['Categories'])))

    links = {}
    for i, path_obj in enumerate(d['Paths']):
        path = path_obj['path']

        assert tuple((nodes.get(k, {}).get('category') for k in path)) == category_indices, '{} is not valid'.format(path)
        for k in path:
            nodes[k]['paths'].append(i)

        path = [nodes_keys.index(k) for k in path]
        for comb in combinations(enumerate(path), 2):
            cat, link_key = zip(*comb)
            if link_key not in links:
                links[link_key] = {'left': link_key[0], 'right': link_key[1], 'direct':(cat[1] == cat[0]+1), 'paths':[]}
            links[link_key]['paths'].append(i)
        path_obj['path'] = path

    return {
        'categories': d['Categories'],
        'nodes': list(nodes.values()),
        'links': list(links.values()),
        'paths': d['Paths'],
    }


def main(output, yaml_file, use_ads, **kwargs):
    with open(output, 'w') as f:
        json.dump(prepare_data_from_yaml(yaml_file, use_ads), f)


if __name__ == '__main__':
    this_dir = os.path.dirname(__file__)
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', metavar='OUTPUT_FILE', default=os.path.join(this_dir, 'data.json'))
    parser.add_argument('-y', '--yaml-file', metavar='YAML_FILE', default=os.path.join(this_dir, 'data.yaml'))
    parser.add_argument('--no-ads', dest='use_ads', action='store_false')
    main(**vars(parser.parse_args()))
