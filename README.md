# LSST Dark Matter Graphic

This repo hosts a web application that uses [D3.js](https://d3js.org/) to implement the LSST "dark matter graphic", as proposed in [LSSTDESC/LSSTDarkMatter](https://github.com/LSSTDESC/LSSTDarkMatter)
(see [#9](https://github.com/LSSTDESC/LSSTDarkMatter/issues/9),
[#10](https://github.com/LSSTDESC/LSSTDarkMatter/issues/10),
[#11](https://github.com/LSSTDESC/LSSTDarkMatter/issues/11), and
[#13](https://github.com/LSSTDESC/LSSTDarkMatter/issues/13)).

This design concept comes largely from coversations between [@kadrlica](https://github.com/kadrlica), [@aimalz](https://github.com/aimalz), [@yymao](https://github.com/yymao).
Web app development is led by [@yymao](https://yymao.github.io/) with content curated by [@kadrlica](https://github.com/kadrlica).

| [Click to see the network diagram](https://lsstdarkmatter.github.io/dark-matter-graph/network.html) | [Click to see the adjacency matrix](https://lsstdarkmatter.github.io/dark-matter-graph/matrix.html) |
|:--:|:--:|
| <a href="https://lsstdarkmatter.github.io/dark-matter-graph/network.html"><img src="static/thumbnail_network.png" width="250"/></a> | <a href="https://lsstdarkmatter.github.io/dark-matter-graph/matrix.html"><img src="static/thumbnail_matrix.png" width="250"/></a> |

## Local Installation

Below are local installation instructions for developers.

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

2. Edit `data/data.yaml`, and then convert it to the json file by running:
   ```
   data/prepare_data.py
   ```
   ([See this readme](data/README.md) to learn more the format of `data.yaml` and `data.json`.)

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

