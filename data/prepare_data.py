#!/usr/bin/env python
import csv
import json
import bisect
from collections import OrderedDict, Counter
import argparse
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
                nodes[node.lower()] = {'name': node, 'category': i, 'index': max_rank+1}
            this_node = list(nodes.keys()).index(node.lower())
            if i:
                this_link = (last_node, this_node)
                if this_link not in links:
                    links[this_link] = {'left': last_node, 'right': this_node, 'entries':[]}
                links[this_link]['entries'].append(set_id)
            last_node = this_node

    return {
        'categories': [{'name': c} for c in raw_data[0]],
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
        'categories': [{'name': c} for c in categories],
        'nodes': [dict(zip(('category', 'index', 'name'), n)) for n in nodes],
        'links': [dict(zip(('left', 'right'), l)) for l in links],
    }


def main(use_table, output):
    prepare_data_this = prepare_data_from_table if use_table else prepare_data_from_matrix
    with open(output, 'w') as f:
        json.dump(prepare_data_this(), f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', metavar='OUTPUT', dest='output', default='data.json')
    parser.add_argument('-t', dest='use_table', action='store_true')
    main(**vars(parser.parse_args()))
