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
    # Mesh Layers

    This Python script demonstrates showing meshes with overlays. Notice that the cortical mesh has a reduced opacity, allowing you to visualize the underlying subcortical mesh.

    The interactive controls allow you to explore different methods to observe meshes that might be obscured by other methods. One can use a shader like `outline` to hide parts of a mesh, adjust transparency, or use the `XRay` method.

    This script also highlights an important feature of ipyniivue: image and mesh loading occurs asynchronously. As a result, the load_meshes() function returns before the dataset is fully ready, meaning we can not set properties for a mesh before it is created. To correctly configure the mesh, an on_mesh_loaded() callback is used. This event triggers once the mesh has finished loading and is ready for use. Although this asynchronous behavior is uncommon in typical Python workflows, it ensures the web interface remains responsive during file loading.
    """)
    return


@app.cell
def _(mo):

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
    return

if __name__ == "__main__":
    app.run()
