#!/usr/bin/env python
import csv
import json
import bisect
from collections import OrderedDict
from itertools import combinations
import argparse
import yaml
import requests


def parse_google_sheet(key, gid=None):
    url = 'https://docs.google.com/spreadsheets/d/{}/export?format=csv{}'.format(key, '' if gid is None else '&gid={}'.format(gid))
    return list(csv.reader(requests.get(url).text.splitlines()))


def prepare_data_from_table():
    raw_data = parse_google_sheet('1OhcJ0p6Wa2_Xl4mO2_JwEG06wBXbdGlD0hCfVQomOyY', '1785255735')

    nodes = OrderedDict()
    links = {}
    last_node = this_node = None
    for set_id, row in enumerate(raw_data[1:]):
        for i, node in enumerate(row):
            if node.lower() not in nodes:
                max_rank = max((v['index'] for v in nodes.values() if v['category'] == i), default=-1)
                nodes[node.lower()] = {'label': node, 'category': i, 'index': max_rank+1}
            this_node = list(nodes.keys()).index(node.lower())
            if i:
                this_link = (last_node, this_node)
                if this_link not in links:
                    links[this_link] = {'left': last_node, 'right': this_node, 'paths':[]}
                links[this_link]['paths'].append(set_id)
            last_node = this_node

    return {
        'categories': [{'label': c} for c in raw_data[0]],
        'nodes': list(nodes.values()),
        'links': list(links.values()),
    }


def prepare_data_from_matrix():
    raw_data = parse_google_sheet('1OhcJ0p6Wa2_Xl4mO2_JwEG06wBXbdGlD0hCfVQomOyY', '681738291')

    nodes = []
    nodes_map_y = {}

    cat_indices_x = [i for i, c in enumerate(raw_data[0]) if c and i >= 2]
    assert cat_indices_x[0] == 2
    cat_indices_x_max = len(raw_data[1])
    for i, node in enumerate(raw_data[1]):
        if i < 2:
            continue
        if not node:
            cat_indices_x_max = i
            break
        cat_i = bisect.bisect(cat_indices_x, i) - 1
        if i == cat_indices_x[cat_i]:
            index_this = 0
        nodes.append((cat_i+1, index_this, node))
        index_this += 1

    cat_indices_y = [i for i, row in enumerate(raw_data) if row[0] and i >= 2]
    assert cat_indices_y[0] == 2
    for i, row in enumerate(raw_data):
        if i < 2:
            continue
        node = row[1]
        if not node:
            break
        cat_i = bisect.bisect(cat_indices_y, i) - 1
        if i == cat_indices_y[cat_i]:
            index_this = 0
        this = (cat_i, index_this, node)
        if cat_i:
            assert this in nodes, '{} does not match in both axes'.format(this)
        else:
            nodes.append(this)
        nodes_map_y[i] = nodes.index(this)
        if cat_i:
            assert nodes_map_y[i] == i - cat_indices_y[1], '{} does not match in both axes'.format(this)
        index_this += 1

    links = []

    for y, row in enumerate(raw_data):
        if y < 2:
            continue
        for x, content in enumerate(row):
            if x < 2:
                continue
            if x >= cat_indices_x_max:
                break
            if not content:
                continue

            cat_x = bisect.bisect(cat_indices_x, x)
            cat_y = bisect.bisect(cat_indices_y, y) - 1
            if cat_y+1 == cat_x:
                this = (nodes_map_y[y], x-2)
                if this not in links:
                    links.append(this)

    categories = [raw_data[2][0]] + [raw_data[0][i] for i in cat_indices_x]

    return {
        'categories': [{'label': c} for c in categories],
        'nodes': [dict(zip(('category', 'index', 'label'), n)) for n in nodes],
        'links': [dict(zip(('left', 'right'), l)) for l in links],
    }


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


def main(output, yaml_file, use_table, use_matrix):
    if use_table:
        data = prepare_data_from_table()
    elif use_matrix:
        data = prepare_data_from_matrix()
    else:
        data = prepare_data_from_yaml(yaml_file)
    with open(output, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', metavar='OUTPUT', dest='output', default='data.json')
    parser.add_argument('-y','--yaml-file', default='data.yaml')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', dest='use_table', action='store_true')
    group.add_argument('-m', dest='use_matrix', action='store_true')
    main(**vars(parser.parse_args()))
