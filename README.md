# ipyniivue marimo demo

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
