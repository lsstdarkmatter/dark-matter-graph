# Dark Matter Graph

**[Click here to see the "Dark Matter Graph"](https://lsstdarkmatter.github.io/dark-matter-graph/)**

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

2. Pull data from the spreadsheet:
   ```
   data/prepare_data.py -o data/data.json
   ```

3. Start a http server:
   ```
   python -m http.server
   ```
   Or, if using Python2:
   ```
   python2 -m SimpleHTTPServer
   ```

4. Direct your browser to the URL the above command returns (usually it is http://0.0.0.0:8000/).

   _Note: if you get an `OSError: [Errno 98] Address already in use`, add some 4- or 5-digit numbers after the command, e.g., `python -m http.server 12345`_.

## Format of `data.json`

- `data.json` should be a json object with three attributes `categories`, `nodes`, and `links`. Each of them should be an array of objects.
- Objects in the `categories` array should have the `name` attribute.
- Objects in the `nodes` array should have (1) the `name` attribute, (2) the `category` attribute that indicates the category this node belongs to, using the corresponding index as in the `categories` array, and (3) the `index` attribute that indicates the index of this node within its category.
- Objects in the `links` array should have the `left` and `right` attributes, indicating the two nodes it links together. Both `left` and `right` should use the corresponding indices as in the `nodes` array.

Here's a minimal example:
```json
{
  "categories":
  [
    {"name": "Model"},
    {"name": "Probe"}
  ],

  "nodes":
  [
    {"category": 0, "index": 0, "name": "SIDM"},
    {"category": 1, "index": 0, "name": "Halo Density Profile"}
  ],

  "links": [
    {"left": 0, "right": 1},
  ]
}
```
