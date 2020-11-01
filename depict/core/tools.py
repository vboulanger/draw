from .plot import Plot

from bokeh.embed import file_html
from bokeh.layouts import column, row
from bokeh.models.widgets import Div
from bokeh.plotting import show as show_bokeh
from bokeh.resources import CDN
import numpy as np


def _make_plot(plot, width_total_as_session, share_x, share_y):
    # TODO: Check the shape first, the types etc
    def build_plot(plot, width=None, x_range=None, y_range=None):
        fig = plot.make_figure()
        if share_x:
            if x_range is None:
                x_range = fig.x_range
            else:
                fig.x_range = x_range
        if share_y:
            if y_range is None:
                y_range = fig.y_range
            else:
                fig.y_range = y_range
        if width:
            fig.width = width
        if not plot.grid_visible:
            fig.xgrid.visible = False
            fig.ygrid.visible = False
        for step in plot.steps:
            step(fig)
        if width:
            div = Div(text=plot.description, width=width, height=None)
        else:
            div = Div(text=plot.description, width=plot.width, height=None)
        return [column(fig, div), x_range, y_range]

    if isinstance(plot, Plot):
        if width_total_as_session:
            return build_plot(plot=plot, width=plot.width_session)[0]
        else:
            return build_plot(plot)[0]
    elif isinstance(plot, (list, np.ndarray)):
        x_range = None
        y_range = None
        row_all = []
        for p_1 in plot:
            if isinstance(p_1, Plot):
                width = p_1.width_session if width_total_as_session else None
                if x_range is None:
                    if y_range is None:
                        f_r, xr, yr = build_plot(p_1, width=width)
                        x_range = xr
                        y_range = yr
                    else:
                        f_r, xr, yr = build_plot(p_1, width=width,
                                                 y_range=y_range)
                        x_range = xr
                else:
                    if y_range is None:
                        f_r, xr, yr = build_plot(p_1, width=width,
                                                 x_range=x_range)
                        y_range = yr
                    else:
                        f_r = build_plot(p_1, width=width, x_range=x_range,
                                         y_range=y_range)[0]
                row_all.append(f_r)
            elif isinstance(p_1, (list, np.ndarray)):
                fig_width = int(p_1[0].width_session / len(p_1))
                width = fig_width if width_total_as_session else None
                row_i = []
                for pp in p_1:
                    if x_range is None:
                        if y_range is None:
                            f_r, xr, yr = build_plot(pp, width=width)
                            x_range = xr
                            y_range = yr
                        else:
                            f_r, xr, yr = build_plot(pp, width=width,
                                                     y_range=y_range)
                            x_range = xr
                    else:
                        if y_range is None:
                            f_r, xr, yr = build_plot(pp, width=width,
                                                     x_range=x_range)
                            y_range = yr
                        else:
                            f_r, xr, yr = build_plot(pp, width=width,
                                                     x_range=x_range,
                                                     y_range=y_range)
                    row_i.append(f_r)
                row_all.append(row(row_i))
        return column(row_all)


def show_base(plot, width_total_as_session=False, share_x=False,
              share_y=False):
    show_bokeh(_make_plot(plot=plot,
                          width_total_as_session=width_total_as_session,
                          share_x=share_x, share_y=share_y))


def _update_show_default_args(show_base, session):
    def show_updated(plot,
                     width_total_as_session=session.width_total_as_session,
                     share_x=False, share_y=False):
        show_base(plot=plot, width_total_as_session=width_total_as_session,
                  share_x=share_x, share_y=share_y)
    return show_updated


def _update_save_default_args(save_base, session):
    def save_updated(plot, save_path=session.save_path,
                     file_exists_mode=session.file_exists_mode,
                     width_total_as_session=session.width_total_as_session,
                     share_x=False, share_y=False):
        save_base(plot=plot, save_path=save_path,
                  file_exists_mode=file_exists_mode,
                  width_total_as_session=width_total_as_session,
                  share_x=share_x, share_y=share_y)
    return save_updated


def save_base(plot, save_path, file_exists_mode, width_total_as_session,
              share_x, share_y):
    if not save_path:
        # TODO: Add warning
        return None

    plot_made = _make_plot(plot, width_total_as_session=width_total_as_session,
                           share_x=share_x, share_y=share_y)
    html = file_html(plot_made, CDN)

    if not save_path.endswith('.html'):
        save_path += '.html'
    if file_exists_mode.lower() == 'append':
        with open(file=save_path, mode='a',) as f:
            f.write(html)
    elif file_exists_mode.lower() == 'overwrite':
        with open(file=save_path, mode='w',) as f:
            f.write(html)


def is_color(c):
    if isinstance(c, str):
        return True
    if isinstance(c, (list, np.ndarray, tuple)) and (
            len(c) == 3) and isinstance(c[0], (float, int)):
        return True
    return False


def from_rgb_to_hex(col):
    return '#' + hex(col[0])[2:].upper().zfill(2) + hex(col[1])[
                                                    2:].upper().zfill(2) + hex(
        col[2])[2:].upper().zfill(2)


def format_color(col):
    if isinstance(col, (list, np.ndarray, tuple)) and all(
            [isinstance(c_i, (float, int)) for c_i in col]) and (
            len(col) == 3):
        if 0 <= np.min(col) <= np.max(col) <= 1:
            rgb = (int(255 * col[0]), int(255 * col[1]), int(255 * col[2]))
        else:
            rgb = (int(col[0]), int(col[1]), int(col[2]))
        return from_rgb_to_hex(rgb)
    else:
        return col


def is_iterable(obj):
    ''' Check if an object is iterable
    Cf https://stackoverflow.com/questions/1952464/in-python-how-do-i- \
    determine-if-an-object-is-iterable

    Args:
        obj (Any object)

    Returns
        is_iterable (bool)
    '''
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True
