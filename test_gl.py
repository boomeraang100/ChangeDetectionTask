import pyglet

print("pyglet:", pyglet.version)

window = pyglet.window.Window(
    width=800,
    height=600,
    visible=True,
)

print("WINDOW CREATED")

pyglet.app.run()