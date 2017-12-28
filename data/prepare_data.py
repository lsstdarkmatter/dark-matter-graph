#!/usr/bin/env python

import csv
import json
from collections import OrderedDict, Counter
import requests

if __name__ == '__main__':
    url = 'https://docs.google.com/spreadsheets/d/1OhcJ0p6Wa2_Xl4mO2_JwEG06wBXbdGlD0hCfVQomOyY/export?gid=1785255735&format=csv'
    raw_data = list(csv.reader(requests.get(url).text.splitlines()))

    nodes = OrderedDict()
    links = {}
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

    counts = Counter((v['category'] for v in nodes.values()))

    data = {
        'categories': [{'name': c, 'count': counts[i]} for i, c in enumerate(raw_data[0])],
        'nodes': list(nodes.values()),
        'links': list(links.values()),
    }

    with open('data.json', 'w') as f:
        json.dump(data, f)
