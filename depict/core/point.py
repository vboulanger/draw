from .plot import Plot
from .tools import show_base, save_base, is_color, format_color
from ..tools.color_palettes import palette_from_name_to_function

import numbers

from bokeh.plotting import figure
from bokeh.models import ColorBar, LinearColorMapper
import numpy as np
import pandas as pd


def point_base(x, y, source_dataframe, width, height, description, title,
               x_label, y_label, show_plot, color, colorbar_type, legend, size,
               alpha, x_axis_type, y_axis_type, grid_visible, session,
               save_path):
    """ Scatter plot

    Args:
        x (array-like): X-axis data
        y (array-like): y-axis data
    """
    # We convert (source, x and y) into only x and y. x and y will be processed
    # normally. source will not be used any more.
    if source_dataframe is not None:
        if isinstance(source_dataframe, dict):
            # TODO: If the user passes a tuple that is not a key, add a
            # message suggesting that he may want to use a list instead
            # because a tuple is considered as a key, and not as an iterable
            # of keys
            # Same for DataFrame
            if y not in source_dataframe.keys():
                raise ValueError('The value of y is not a key of the '
                                 'dictionary provided in source_dataframe')
            if isinstance(legend, str) and (legend.lower() == 'auto'):
                if isinstance(y, str):
                    legend = str(y)
            y = source_dataframe[y]

            if x not in source_dataframe.keys():
                raise ValueError('The value of x is not a key of the '
                                 'dictionary provided in source_dataframe')
            x = source_dataframe[x]

        elif isinstance(source_dataframe, pd.DataFrame):
            if y not in source_dataframe.keys():
                raise ValueError('The value of y is not a key of the '
                                 'DataFrame provided in source_dataframe')
            if isinstance(legend, str) and (legend.lower() == 'auto'):
                if isinstance(y, str):
                    legend = str(y)
            y = source_dataframe[y]

            if x is None:
                # Be careful, the behavior is different for a dict and for a
                # Dataframe
                x = source_dataframe.index.values
            else:
                if x not in source_dataframe.keys():
                    raise ValueError('The value of x is not a key of the '
                                     'DataFrame provided in source_dataframe')
                x = source_dataframe[x].values

    if (x is None) or (y is None):
        raise ValueError('X and y must be specified. They must be a one '
                         'dimensional array like')
    if (not isinstance(x, (list, np.ndarray, tuple)))\
            or (not isinstance(y, (list, np.ndarray, tuple))):
        raise ValueError('X and y must be a one dimensional array like')
    if (np.ndim(x) != 1) or (np.ndim(y) != 1):
        raise ValueError('X and y must be a one dimensional array like')

    # We pre-process `color`
    _color_bar_made = False
    if color is None:
        nb_color_needed = 1
        color = palette_from_name_to_function[session.palette_name](
            nb_color_needed)
        color = [color[0] for _ in y]
    # We pre-process `color`
    # Corner case: if color = [0.5, 0.6, 0.7] and len(y) == 3, we cannot say if
    # color means actually the color defined by [0.5, 0.6, 0.7] or if this
    # quantity should be converted into categorical colors (3 colors here cause
    # the 3 values are different). For that case we use the argument
    # `automatic_color_mapping` in from the session.

    elif (len(color) == 3) \
            and isinstance(color[0], numbers.Real)\
            and session.automatic_color_mapping\
            and (len(y) == 3):
        color = [color, color, color]
    else:
        # General case
        if is_color(color):
            color = [color for _ in y]
        elif isinstance(color, (list, np.ndarray, tuple))\
                and is_color(color[0]):
            if len(color) == len(y):
                pass  # Good case
            elif len(color) == 2:
                # TODO: Implement a linear set of color between the 2 given
                #  colors
                raise ValueError('Number of elements in `color` invalid')
            else:
                # TODO: Improve error message
                raise ValueError('Number of elements in `color` invalid')
        elif isinstance(color, (list, np.ndarray, tuple)) and isinstance(
                color[0], numbers.Real):
            if len(color) != len(y):
                # TODO: Improve error message
                raise ValueError('Number of elements in `color` invalid')

            if not colorbar_type:
                colorbar_type = 'auto'
                _add_color_bar = False
            else:
                _add_color_bar = True

            if colorbar_type.lower() == 'auto':
                if ((len(np.unique(color)) / len(color)) <= 0.5)\
                        and (len(np.unique(color) < 9)):
                    # Data are considered categorical
                    colorbar_type = 'categorical'
                else:
                    colorbar_type = 'continuous'
            else:
                colorbar_type = colorbar_type.lower()

            if colorbar_type == 'categorical':
                if isinstance(legend, str) and (legend.lower() == 'auto'):
                    legend = [str(c) for c in color]
                color_unique = sorted(list(np.unique(color)))
                nb_color_needed = len(color_unique)
                palette_colors = palette_from_name_to_function[
                    session.palette_name](nb_color_needed)
                color = [palette_colors[color_unique.index(c)] for c in color]
            elif colorbar_type == 'continuous':
                palette_colors = palette_from_name_to_function[
                    session.palette_name](256)
                color_mapper = LinearColorMapper(palette=palette_colors,
                                                 low=np.min(color),
                                                 high=np.max(color))
                color = np.array(color)
                col_indexes = (color - color.min()) / (
                            (color.max() - color.min()) / (256 - 1))
                color_min = np.min(color)
                color_max = np.max(color)
                color = [palette_colors[int(ci)] for ci in col_indexes]
                if _add_color_bar:
                    color_bar = ColorBar(color_mapper=color_mapper,
                                         location=(0, 0))
                    _color_bar_made = True

    color = [format_color(c) for c in color]

    # We pre-process `legend`
    # add_legend = True
    if (legend is None) or (legend == 'auto'):
        legend = ['' for _ in y]
        # add_legend = False
    elif isinstance(legend, str):
        legend = [legend for _ in y]
    elif isinstance(legend, (list, np.ndarray, tuple)):
        if len(legend) != len(y):
            raise ValueError('The number of elements in `legend` is not '
                             'consistent with the data')

    # We pre-process `size`
    if isinstance(size, numbers.Real):
        size = [size for _ in y]
    elif isinstance(size, (list, np.ndarray, tuple)):
        if len(size) != len(y):
            raise ValueError('The size argument given is non consistent '
                             'with the data')

    # We pre-process `alpha`
    if isinstance(alpha, numbers.Real):
        alpha = [alpha for _ in y]
    elif isinstance(alpha, (list, np.ndarray, tuple)):
        if len(alpha) != len(y):
            raise ValueError(
                'The alpha argument given is non consistent with the data')

    # We pre-process `x_axis_type` and `y_axis_type`
    if x_axis_type.lower() == 'auto':
        if isinstance(x[0], numbers.Real):
            x_axis_type = 'linear'
        else:
            try:
                pd.to_datetime(x[0], errors='raise')
            except ValueError:
                raise ValueError('`x_axis_type` is set to `auto` and x[0] '
                                 'is neither a number, nor an object parsable '
                                 'as a date. Object x[0]: {}'.format(x[0]))
            x_axis_type = 'datetime'
            x = pd.to_datetime(x)
    elif x_axis_type.lower() in ['numeric', 'numerical']:
        x_axis_type = 'linear'
    elif x_axis_type.lower() in ['date', 'datetime', 'time']:
        x_axis_type = 'datetime'
        x = pd.to_datetime(x)
    # Same with y axis
    if y_axis_type.lower() == 'auto':
        if isinstance(y[0], numbers.Real):
            y_axis_type = 'linear'
        else:
            try:
                pd.to_datetime(y[0], errors='raise')
            except ValueError:
                raise ValueError('`y_axis_type` is set to `auto` and y[0] '
                                 'is neither a number, nor an object parsable '
                                 'as a date. Object y[0]: {}'.format(y[0]))
            y_axis_type = 'datetime'
            y = pd.to_datetime(y)
    elif y_axis_type.lower() in ['numeric', 'numerical']:
        y_axis_type = 'linear'
    elif y_axis_type.lower() in ['date', 'datetime', 'time']:
        y_axis_type = 'datetime'
        y = pd.to_datetime(y)

    # We group x and y based on legend because in bokek, figure.scatter can
    # only set one legend label by scatter plot. So if the legend contains
    # an iterable of strings, we need to look for unique values and mask
    # all attributes
    legend_unique = np.unique(legend)
    mask_all = [l_i == np.array(legend) for l_i in legend_unique]
    x = [np.array(x)[mask] for mask in mask_all]
    y = [np.array(y)[mask] for mask in mask_all]
    color = [np.array(color)[mask] for mask in mask_all]
    size = [np.array(size)[mask] for mask in mask_all]
    alpha = [np.array(alpha)[mask] for mask in mask_all]

    steps = []
    legend_exist = False
    legend_unique = [str(lu) for lu in legend_unique]
    for (x_i, y_i, col_i, leg_i, s_i, a_i) in zip(x, y, color, legend_unique,
                                                  size, alpha):
        if leg_i:
            legend_exist = True

            def step(f, x_copy=x_i, y_copy=y_i, col_c=col_i, leg_c=leg_i,
                     s_c=s_i, a_c=a_i):
                f.scatter(x=x_copy, y=y_copy, color=col_c, legend_label=leg_c,
                          size=s_c, alpha=a_c)
        else:
            def step(f, x_copy=x_i, y_copy=y_i, col_c=col_i,
                     s_c=s_i, a_c=a_i):
                f.scatter(x=x_copy, y=y_copy, color=col_c, size=s_c, alpha=a_c)
        steps.append(step)

    if legend_exist:
        def make_legend_interactive(f):
            f.legend.click_policy = "hide"
        steps.append(make_legend_interactive)

    def _make_fig():
        fig = figure(width=width, height=height, title=title,
                     background_fill_color=session.background_color,
                     x_axis_label=x_label, y_axis_label=y_label,
                     x_axis_type=x_axis_type, y_axis_type=y_axis_type)
        fig.title.align = 'center'
        fig.title.text_color = '#33331a'
        fig.xgrid.grid_line_dash = [8, 3, 2, 3]
        fig.ygrid.grid_line_dash = [8, 3, 2, 3]
        fig.toolbar.autohide = True
        if _color_bar_made and _add_color_bar:
            color_mapper = LinearColorMapper(palette=palette_colors,
                                             low=color_min,
                                             high=color_max)
            c_bar = ColorBar(color_mapper=color_mapper, location=(0, 0))
            fig.add_layout(c_bar, 'right')
        return fig

    plot = Plot(make_figure=_make_fig, steps=steps, description=description,
                figure=_make_fig(), width=width, grid_visible=grid_visible,
                width_session=session.width, session=session)

    if save_path:
        save_base(plot=plot, save_path=save_path,
                  file_exists_mode=session.file_exists_mode,
                  width_total_as_session=False, share_x=False, share_y=False)

    if show_plot:
        return show_base(plot) or plot
    else:
        return plot


def _update_point_default_args(point, session):
    def point_updated(x, y, source_dataframe=None, width=session.width,
                      height=session.height, description=session.description,
                      title=session.title, x_label=None, y_label=None,
                      show_plot=session.show_plot, color=None,
                      colorbar_type='auto', legend='auto', size=6, alpha=1,
                      x_axis_type='auto', y_axis_type='auto',
                      save_path=session.save_path,
                      grid_visible=session.grid_visible):
        plot = point(x=x, y=y, source_dataframe=source_dataframe, width=width,
                     height=height, description=description, title=title,
                     x_label=x_label, y_label=y_label, show_plot=show_plot,
                     color=color, colorbar_type=colorbar_type, legend=legend,
                     size=size, alpha=alpha, x_axis_type=x_axis_type,
                     y_axis_type=y_axis_type, grid_visible=grid_visible,
                     session=session, save_path=save_path)
        return plot
    return point_updated
