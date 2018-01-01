#!/usr/bin/env python
import os
import json
from collections import OrderedDict
from itertools import combinations
import argparse
import yaml

__all__ = ['prepare_data_from_yaml', 'main']

def prepare_data_from_yaml(yaml_file):
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


def main(output, yaml_file, **kwargs):
    with open(output, 'w') as f:
        json.dump(prepare_data_from_yaml(yaml_file), f)


if __name__ == '__main__':
    this_dir = os.path.dirname(__file__)
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', metavar='OUTPUT_FILE', default=os.path.join(this_dir, 'data.json'))
    parser.add_argument('-y', '--yaml-file', metavar='YAML_FILE', default=os.path.join(this_dir, 'data.yaml'))
    main(**vars(parser.parse_args()))
