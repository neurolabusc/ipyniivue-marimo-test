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
    # Mesh Layers

    This Python script demonstrates showing meshes with overlays. Notice that the cortical mesh has a reduced opacity, allowing you to visualize the underlying subcortical mesh.

    The interactive controls allow you to explore different methods to observe meshes that might be obscured by other methods. One can use a shader like `outline` to hide parts of a mesh, adjust transparency, or use the `XRay` method.

    This script also highlights an important feature of ipyniivue: image and mesh loading occurs asynchronously. As a result, the load_meshes() function returns before the dataset is fully ready, meaning we can not set properties for a mesh before it is created. To correctly configure the mesh, an on_mesh_loaded() callback is used. This event triggers once the mesh has finished loading and is ready for use. Although this asynchronous behavior is uncommon in typical Python workflows, it ensures the web interface remains responsive during file loading.
    """)
    return


@app.cell
def _(mo):
    from ipyniivue import NiiVue, ShowRender
    import ipywidgets as widgets

    nv = NiiVue(
        show_3d_crosshair=True, back_color=(1, 1, 1, 1), is_colorbar=True
    )
    nv.opts.show_legend = False

    mesh_layer = {
        "url": "https://niivue.com/demos/images/BrainMesh_ICBM152.lh.motor.mz3",
        "cal_min": 0.5,
        "cal_max": 5.5,
        "use_negative_cmap": True,
    }

    nv.load_meshes(
        [
            {
               "url": "https://niivue.com/demos/images/BrainMesh_ICBM152.lh.mz3",
               "layers": [mesh_layer],
            },
            {
                "url": "https://niivue.com/demos/images/CIT168.mz3",
            },

        ]
    )

    @nv.on_mesh_loaded
    def on_mesh_loaded(volume):
        nv.meshes[1].colorbar_visible = False

    ## User interface
    slider_opacity = mo.ui.slider(
        start=1,
        stop=10,
        step=1,
        value=10,
        show_value=False,
        label="Opacity",
        on_change=lambda v: nv.set_mesh_layer_property(nv.meshes[0].id, 0, "opacity", v * 0.1),
    )

    slider_xray = mo.ui.slider(
        start=0,
        stop=30,
        step=1,
        value=0,
        show_value=False,
        label="XRay",
        on_change=lambda v: setattr(nv.opts, "mesh_xray", v * 0.01),
    )

    drop_shader = mo.ui.dropdown(
        options=nv.mesh_shader_names(),
        value="Phong",
        label="Shader",
        on_change=lambda v: nv.set_mesh_shader(nv.meshes[0].id, v),
    )

    def on_alpha_change(value):
        idx = 0
        if value == "Opaque":
            nv.meshes[idx].opacity = 1.0
        elif value == "Translucent":
            nv.meshes[idx].opacity = 0.2
        elif value == "Transparent":
            nv.meshes[idx].opacity = 0.0
        nv.draw_scene()


    drop_alpha = mo.ui.dropdown(
        options=["Opaque", "Translucent", "Transparent"],
        value="Opaque",
        label="Opacity",
        on_change=on_alpha_change,   # ← no parentheses!
    )
    ## Display user interface and meshes

    mo.vstack([
        mo.hstack([slider_opacity, slider_xray, drop_shader, drop_alpha]),
        nv,
    ])
    return NiiVue, ShowRender

@app.cell
def _(mo):
    mo.md("""
    # Voxel statistics

    This Python script illustrates the ability to load a statistical map on top of an anatomical scan.
    """)
    return

@app.cell
def _(NiiVue, ShowRender, mo):
    nv2 = NiiVue(
        back_color=(1, 1, 1, 1),
        show_3d_crosshair=True,
        is_colorbar=True,
        multiplanar_show_render=ShowRender.ALWAYS,
    )
    nv2.load_volumes([
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
    nv2.volumes[0].colorbar_visible = False
    nv2.opts.is_alpha_clip_dark = True
    nv2.overlay_outline_width = 1
    nv2.set_interpolation(True)

    ## User interface

    def on_neg_stat_change(values):
        """Set threshold for statistical overlay."""
        nv2.volumes[1].cal_min_neg = -values[1]
        nv2.volumes[1].cal_max_neg = -values[0]

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
        nv2.volumes[1].cal_min = values[0]
        nv2.volumes[1].cal_max = values[1]

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
        on_change=lambda v: setattr(nv2, "overlay_outline_width", v),
    )

    mode_options = [
        "Restrict colorbar to range",
        "Colorbar from 0, transparent subthreshold",
        "Colorbar from 0, translucent subthreshold",
    ]

    def on_mode_change(value):
        """Handle alpha mode dropdown changes."""
        idx = mode_options.index(value)
        nv2.volumes[1].colormap_type = idx

    drop_mode = mo.ui.dropdown(
        options=mode_options,
        value=mode_options[0],
        label="Mode",
        on_change=on_mode_change,
    )


    ## Display user interface and volumes

    mo.vstack([
        mo.hstack([range_neg_stat, range_pos_stat, slider_outline, drop_mode]),
        nv2,
    ])
    return


if __name__ == "__main__":
    app.run()
