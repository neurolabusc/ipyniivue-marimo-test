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
    # Voxel statistics

    This Python script illustrates the ability to load a statistical map on top of an anatomical scan.
    """)
    return


@app.cell
def _(NiiVue, ShowRender, mo):
    nv = NiiVue(
        back_color=(1, 1, 1, 1),
        show_3d_crosshair=True,
        is_colorbar=True,
        multiplanar_show_render=ShowRender.ALWAYS,
    )
    nv.load_volumes([
            {'url': 'https://niivue.com/demos/images/mni152.nii.gz'},
            {'url': 'https://niivue.com/demos/images/spmMotor.nii.gz',
                 "colormap": "warm",
                "colormap_negative": "winter",
                "cal_min": 5,
                "cal_max": 7,
                "cal_min_neg": -7,
                "cal_max_neg": -5,
            }

        ])
    nv.volumes[0].colorbar_visible = False
    nv.opts.is_alpha_clip_dark = True
    nv.overlay_outline_width = 1
    nv.set_interpolation(True)

    ## User interface

    def on_neg_stat_change(values):
        """Set threshold for statistical overlay."""
        nv.volumes[1].cal_min_neg = -values[1]
        nv.volumes[1].cal_max_neg = -values[0]

    range_neg_stat = mo.ui.range_slider(
        start=1,
        stop=10,
        step=1,
        value=[5, 7],
        label="-Threshold",
        on_change=on_neg_stat_change,
    )

    def on_pos_stat_change(values):
        """Set threshold for statistical overlay."""
        nv.volumes[1].cal_min = values[0]
        nv.volumes[1].cal_max = values[1]

    range_pos_stat = mo.ui.range_slider(
        start=1,
        stop=10,
        step=1,
        value=[5, 7],
        label="+Threshold",
        on_change=on_pos_stat_change,
    )

    slider_outline = mo.ui.slider(
        start=0,
        stop=4,
        step=1,
        value=1,
        show_value=False,
        label="Outline",
        on_change=lambda v: setattr(nv, "overlay_outline_width", v),
    )

    mode_options = [
        "Restrict colorbar to range",
        "Colorbar from 0, transparent subthreshold",
        "Colorbar from 0, translucent subthreshold",
    ]

    def on_mode_change(value):
        """Handle alpha mode dropdown changes."""
        idx = mode_options.index(value)
        nv.volumes[1].colormap_type = idx

    drop_mode = mo.ui.dropdown(
        options=mode_options,
        value=mode_options[0],
        label="Mode",
        on_change=on_mode_change,
    )


    ## Display user interface and volumes

    mo.vstack([
        mo.hstack([range_neg_stat, range_pos_stat, slider_outline, drop_mode]),
        nv,
    ])
    return


if __name__ == "__main__":
    app.run()
