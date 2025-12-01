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
def _(mo):
    mo.md("""
    ## Loading Brain Volume

    Downloading MRI scan from HBN dataset...
    """)
    return


@app.cell
def _(NiiVue, mo):
    import httpx
    from pathlib import Path
    import tempfile

    # URL to the brain scan
    url = "https://fcp-indi.s3.amazonaws.com/data/Projects/HBN/MRI/Site-CBIC/sub-NDARAA396TWZ/anat/sub-NDARAA396TWZ_acq-HCP_T1w.nii.gz"

    # Create temporary file
    temp_dir = Path(tempfile.mkdtemp())
    temp_file = temp_dir / "brain.nii.gz"

    # Download the file with progress indication
    with mo.status.spinner(title="Downloading brain scan...") as _spinner:
        response = httpx.get(url, follow_redirects=True, timeout=60.0)
        temp_file.write_bytes(response.content)

    # Create NiiVue instance and load the file
    nv = NiiVue()
    nv.load_volumes([{"path": str(temp_file)}])

    nv
    return


if __name__ == "__main__":
    app.run()
