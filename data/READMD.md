
## Format of `data.json`

- `data.json` should be a json object with four attributes `categories`, `nodes`, `links`, and `path`. Each of them should be an array of objects.
- Objects in the `categories` array should have the `label` attribute.
- Objects in the `nodes` array should have (1) the `label` attribute, (2) the `category` attribute that indicates the category this node belongs to, using the corresponding index as in the `categories` array, (3) the `index` attribute that indicates the index of this node within its category, and (4) the `paths` attribute that contains a list of path indices.
- Objects in the `links` array should have the `left` and `right` attributes, indicating the two nodes it links together. Both `left` and `right` should use the corresponding indices as in the `nodes` array.  It should also have the `paths` attribute that contains a list of path indices.
- Conceptually, each "path" is a collection of "links". It should also have the `path` attribute that contains a list of node indices.

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
    {"category": 0, "index": 0, "label": "SIDM", "paths": [0]},
    {"category": 1, "index": 0, "label": "Halo Density Profile", "paths": [0]}
  ],

  "links": [
    {"left": 0, "right": 1, "paths": [0]}
  ],

  "paths": [
    {"path": [0, 1]}
  ]
}
```
