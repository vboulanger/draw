import depict
import pytest


def test_sesstion_creation_basic():
    depict.session()

@pytest.mark.parametrize("width", [1000])
@pytest.mark.parametrize("height", [1000])
@pytest.mark.parametrize("save_path", [None, 'test_path'])
@pytest.mark.parametrize("file_exists_mode", ['append', 'overwrite'])
@pytest.mark.parametrize("description", ['', 'Blablabla'])
@pytest.mark.parametrize("title", ['', 'Blablabla'])
@pytest.mark.parametrize("jupyter_notebook", [False])
@pytest.mark.parametrize("background_color", ['blue', (204, 101, 156)])
@pytest.mark.parametrize("palette_name", ['categories_10', 'categories_256',
                                          'linear_purple', 'linear_blue_red',
                                          'linear_blue'])
@pytest.mark.parametrize("grid_visible", [False, True])
@pytest.mark.parametrize("show_plot", [False, True])
@pytest.mark.parametrize("width_total_as_session", [False, True])
@pytest.mark.parametrize("automatic_color_mapping", [False, True])
def test_params_valid_session(width, height, save_path, file_exists_mode,
                              description, title, jupyter_notebook,
                              background_color, palette_name, grid_visible,
                              show_plot, width_total_as_session,
                              automatic_color_mapping):
    depict.session(width=width, height=height, save_path=save_path,
                   file_exists_mode=file_exists_mode, description=description,
                   title=title, jupyter_notebook=jupyter_notebook,
                   background_color=background_color,
                   palette_name=palette_name, grid_visible=grid_visible,
                   show_plot=show_plot,
                   width_total_as_session=width_total_as_session,
                   automatic_color_mapping=automatic_color_mapping)
