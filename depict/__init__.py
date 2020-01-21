from .core.histogram import histogram_base as _histogram_base
from .core.histogram import _update_histogram_default_args
from .core.line import line_base as _line_base
from .core.line import _update_line_default_args

from .core.point import point_base as _point_base
from .core.point import _update_point_default_args

from .core.tools import save_base as _save_base
from .core.tools import _update_save_default_args

from .core.tools import show_base as _show_base
from .core.tools import _update_show_default_args

from .core.session import Session as _Session


__all__ = ['session', 'line', 'point', 'histogram', 'show', 'save']


def session(width=900, height=400, save_path=None, file_exists_mode='append',
            description='', title='', jupyter_notebook=False,
            background_color='aliceblue', palette_name='categories_10',
            grid_visible=True, show_plot=True, width_total_as_session=True,
            automatic_color_mapping=True):
    global _SESSION, histogram, line, point, save, show
    _SESSION = _Session(width=width, height=height, save_path=save_path,
                        file_exists_mode=file_exists_mode,
                        description=description, title=title,
                        jupyter_notebook=jupyter_notebook,
                        background_color=background_color,
                        palette_name=palette_name,
                        grid_visible=grid_visible, show_plot=show_plot,
                        width_total_as_session=width_total_as_session,
                        automatic_color_mapping=automatic_color_mapping)

    save = _update_save_default_args(save_base=_save_base, session=_SESSION)
    histogram = _update_histogram_default_args(histogram_base=_histogram_base,
                                               session=_SESSION)
    line = _update_line_default_args(line=_line_base, session=_SESSION)
    point = _update_point_default_args(point=_point_base, session=_SESSION)
    show = _update_show_default_args(show_base=_show_base, session=_SESSION)


session()
