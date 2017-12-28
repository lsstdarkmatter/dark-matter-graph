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

1. Clone this repo
   ```
   git clone https://github.com/lsstdarkmatter/dark-matter-graph.git
   cd dark-matter-graph
   ```
   or update it if you already have a local clone
   ```
   cd dark-matter-graph
   git pull
   ```

2. Pull data from the spreadsheet:
   ```
   data/prepare_data.py -o data/data.json
   ```

3. Start a http server
   ```
   python -m http.server
   ```
   Or, if using Python2:
   ```
   python2 -m SimpleHTTPServer
   ```
