# ipyniivue marimo demo

This notebook illustrates how [ipyniivue](https://github.com/niivue/ipyniivue) can be embedded into [marimo](https://docs.marimo.io/) notebooks. Documentation for [ipyniivue](https://niivue.github.io/ipyniivue/) and [marimo widgets](https://docs.marimo.io/api/inputs/) can help extend this notebook.

## Marimo Online Playground

You can also insert ipyniivue into the [marimo playground](https://docs.marimo.io/guides/publishing/playground/).

```javascript
import marimo as mo
from ipyniivue import NiiVue
nv = NiiVue()
nv.load_volumes([{"url": "https://niivue.com/demos/images/mni152.nii.gz"}])
nv
```

## Live Demo

You can run fork and run this live demo using a Github or Google log in.

[![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_UrcD1cE8mC6Pk9Au987RmA)

# Local Development

Open notebook in edit mode:

```sh
git clone https://github.com/neurolabusc/ipyniivue-marimo-test.git
cd ipyniivue-marimo-test
pip install uv
uv run marimo edit marimo.vox.py
# alternatively, for mesh-based example
# uv run marimo edit marimo.mesh.py
```

Export single notebook as WASM+HTML website:


```sh
uv run marimo export html-wasm marimo.vox.py -o dist/index.html
```

Export all `marimo.*.py` notebooks as web pages with an index page and a navigation bar:

```
python ./build_all.py
```