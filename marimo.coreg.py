import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from ipyniivue import NiiVue, ShowRender
    import ipywidgets as widgets
    return NiiVue, ShowRender, mo


@app.cell
def _(mo):
    mo.md("""
    # Coregistration Images

    We often need to verify that two images have been successfully warped into a common anatomical space. In this example, we load a background T1-weighted template representing the average brain shape of 152 healthy young adults (displayed in grayscale). On top of this, we overlay a T2-weighted scan from a stroke patient that has been aligned to the template using ANTs, shown with the [Navia](https://www.fabiocrameri.ch/colourpalettes/) colormap (initially transparent). Finally, we add a red [Difference of Gaussian](https://pubmed.ncbi.nlm.nih.gov/38508496/) outline of the spatially normalized T2w image. The sliders allow you to adjust the opacity of each layer.
    """)
    return


@app.cell
def _(NiiVue, ShowRender, mo):
    nv = NiiVue(
        back_color=(0, 0, 0, 0),
        show_3d_crosshair=True,
        multiplanar_show_render=ShowRender.ALWAYS,
    )
    nv.load_volumes([
            {'url': 'https://niivue.github.io/niivue-demo-images/mni152.nii.gz'},
            {'url': 'https://niivue.github.io/niivue-demo-images/M2208_T2w.nii.gz', 'colormap': 'navia', 'opacity': 0.0},
            {'url': 'https://niivue.github.io/niivue-demo-images/M2208_dog.nii.gz', 'colormap': 'actc'}
        ])

    ## User interface

    slider_template = mo.ui.slider(
        start=0,
        stop=1,
        step=0.1,
        value=1.0,
        show_value=False,
        label="Template",
        on_change=lambda v: setattr(nv.volumes[0], "opacity", v),
    )

    slider_coreg = mo.ui.slider(
        start=0,
        stop=1,
        step=0.1,
        value=0.0,
        show_value=False,
        label="Coreg",
        on_change=lambda v: setattr(nv.volumes[1], "opacity", v),
    )

    slider_outline = mo.ui.slider(
        start=0,
        stop=1,
        step=0.1,
        value=1.0,
        show_value=False,
        label="Outline",
        on_change=lambda v: setattr(nv.volumes[2], "opacity", v),
    )


    ## Display user interface and volumes

    mo.vstack([
        mo.hstack([slider_template, slider_coreg, slider_outline]),
        nv,
    ])
    return


if __name__ == "__main__":
    app.run()
