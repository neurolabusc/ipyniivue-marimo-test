# ipyniivue marimo demo

This notebook illustrates how [ipyniivue](https://github.com/niivue/ipyniivue) can be embedded into [marimo](https://docs.marimo.io/) notebooks. Documentation for [ipyniivue](https://niivue.github.io/ipyniivue/) and [marimo widgets](https://docs.marimo.io/api/inputs/) can help extend this notebook.

## Live Demo
[![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_UrcD1cE8mC6Pk9Au987RmA)

# Local Development

Open notebook in edit mode:

```sh
git clone git@github.com:neurolabusc/ipyniivue-marimo-test.git
cd ipyniivue-marimo-test
uv run marimo edit niivue_demo.py
```

Export WASM+HTML website:


```sh
uv run marimo export html-wasm niivue_demo.py -o dist/index.html
```
