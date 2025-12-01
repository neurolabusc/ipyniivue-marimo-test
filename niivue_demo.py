import marimo

__generated_with = "0.18.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # NiiVue Interactive Brain Viewer

    This demo showcases the **ipyniivue** widget with a real brain scan from the
    Healthy Brain Network dataset, dynamically loaded from S3.
    """)
    return


@app.cell
def _():
    from ipyniivue import NiiVue
    return (NiiVue,)


@app.cell
def _(NiiVue):
    url = "https://fcp-indi.s3.amazonaws.com/data/Projects/HBN/MRI/Site-CBIC/sub-NDARAA396TWZ/anat/sub-NDARAA396TWZ_acq-HCP_T1w.nii.gz"

    nv = NiiVue()
    nv.load_volumes([{"url": url}])

    nv
    return


if __name__ == "__main__":
    app.run()
