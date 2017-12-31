# Dark Matter Graph

➡️ [Click here to see the network diagram](https://lsstdarkmatter.github.io/dark-matter-graph/)

➡️ [Click here to see the adjacency matrix](https://lsstdarkmatter.github.io/dark-matter-graph/matrix.html)

![](data/network_graph.png =200x200)
![](data/adjacency_matrix.png =200x200)


This repo hosts a web application that uses [D3.js](https://d3js.org/) to implement the "dark matter graph", as proposed in
[LSSTDESC/LSSTDarkMatter](https://github.com/LSSTDESC/LSSTDarkMatter) (see [#9](https://github.com/LSSTDESC/LSSTDarkMatter/issues/9),
[#10](https://github.com/LSSTDESC/LSSTDarkMatter/issues/10),
[#11](https://github.com/LSSTDESC/LSSTDarkMatter/issues/11), and
[#13](https://github.com/LSSTDESC/LSSTDarkMatter/issues/13)).

This idea mostly comes from [@kadrlica](https://github.com/kadrlica), [@aimalz](https://github.com/aimalz), [@yymao](https://github.com/yymao).
The web app is made by [@yymao](https://yymao.github.io/).

## Usage

1. Clone this repo:
   ```
   git clone https://github.com/lsstdarkmatter/dark-matter-graph.git
   cd dark-matter-graph
   ```
   or update it if you already have a local clone:
   ```
   cd dark-matter-graph
   git pull
   ```

2. Prepare data from the spreadsheet:
   ```
   data/prepare_data.py --yaml-file data/data.yaml -o data/data.json
   ```

3. Start a http server:
   ```
   python -m http.server
   ```
   Or, if using Python2:
   ```
   python2 -m SimpleHTTPServer
   ```

4. Direct your browser to the URL the above command returns, or if it returns `Serving HTTP on X.X.X.X port YYYY`,
   direct your browser to http://X.X.X.X:YYYY/ (usually it would be http://0.0.0.0:8000/).

   _Note: if you get an `OSError: [Errno 98] Address already in use`, add some 4- or 5-digit numbers after the command, e.g., `python -m http.server 12345`_.

## Format of `data.json`

- `data.json` should be a json object with four attributes `categories`, `nodes`, `links`, and `path`. Each of them should be an array of objects.
- Objects in the `categories` array should have the `label` attribute.
- Objects in the `nodes` array should have (1) the `label` attribute, (2) the `category` attribute that indicates the category this node belongs to, using the corresponding index as in the `categories` array, and (3) the `index` attribute that indicates the index of this node within its category.
- Objects in the `links` array should have the `left` and `right` attributes, indicating the two nodes it links together. Both `left` and `right` should use the corresponding indices as in the `nodes` array.
- Each "path" is a collection of "links". Specification on `path` object TBD.

Here's a minimal example:
```json
{
  "categories":
  [
    {"label": "Model"},
    {"label": "Probe"}
  ],

  "nodes":
  [
    {"category": 0, "index": 0, "label": "SIDM"},
    {"category": 1, "index": 0, "label": "Halo Density Profile"}
  ],

  "links": [
    {"left": 0, "right": 1, "paths": [0]}
  ],

  "paths": [
    {"path": [0, 1]}
  ]
}
```
