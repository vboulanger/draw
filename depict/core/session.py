from bokeh.io import output_notebook, reset_output


class Session:
    def __init__(self, width, height, save_path, file_exists_mode,
                 description, title, jupyter_notebook,
                 background_color, palette_name, grid_visible, show_plot,
                 width_total_as_session, automatic_color_mapping):
        self.width = width
        self.height = height
        self.save_path = save_path
        self.file_exists_mode = file_exists_mode
        self.description = description
        self.title = title
        if jupyter_notebook:
            output_notebook()
        else:
            reset_output()
        self.background_color = background_color
        self.palette_name = palette_name
        self.grid_visible = grid_visible
        self.show_plot = show_plot
        self.width_total_as_session = width_total_as_session
        self.automatic_color_mapping = automatic_color_mapping
