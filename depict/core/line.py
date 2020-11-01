from .plot import Plot
from .tools import show_base, save_base, is_color, format_color, is_iterable
from ..tools.color_palettes import palette_from_name_to_function

import numbers

from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.models import ColorBar, LinearColorMapper
import numpy as np
import pandas as pd


def line_base(y, x, source_dataframe, width, height, description, title,
              x_label, y_label, show_plot, color, colorbar_type, legend,
              line_width, alpha, style, x_axis_type, y_axis_type, x_range,
              y_range, fill_between, grid_visible, session, save_path):
    """ One dimensional plot. This is the docstring of line

    Args:
        x (array-like): X-axis data
        y (array-like): y-axis data
        x_range (array-like) Range of the x-axis. E.g. `[0, 1]`
        y_range (array-like) Range of the y-axis. E.g. `[0, 1]`
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

            if isinstance(y, (list, np.ndarray)):
                if not all([y_i in source_dataframe.keys() for y_i in y]):
                    raise ValueError('At least some of the values of y are '
                                     'not keys of the dictionary provided in '
                                     'source_dataframe')
                if legend.lower() == 'auto':
                    legend = [y_i if isinstance(y_i, str) else '' for y_i in y]
                y = [source_dataframe[y_i] for y_i in y]
            else:
                if y not in source_dataframe.keys():
                    raise ValueError('The value of y is not a key of the '
                                     'dictionary provided in source_dataframe')
                if legend.lower() == 'auto':
                    if isinstance(y, str):
                        legend = str(y)
                y = [source_dataframe[y]]

            if x is None:
                pass  # Will be treated as the default x behavior
            elif isinstance(x, (list, np.ndarray)):
                if not all([x_i in source_dataframe.keys() for x_i in x]):
                    raise ValueError('At least some of the values of x are '
                                     'not keys of the dictionary provided in '
                                     'source_dataframe')
                x = [source_dataframe[x_i] for x_i in x]
            else:
                if x not in source_dataframe.keys():
                    raise ValueError('The value of x is not a key of the '
                                     'dictionary provided in source_dataframe')
                x = source_dataframe[x]

        elif isinstance(source_dataframe, pd.DataFrame):
            if isinstance(y, (list, np.ndarray)):
                if not all([y_i in source_dataframe.keys() for y_i in y]):
                    raise ValueError('At least some of the values of y are '
                                     'not keys of the DataFrame provided in '
                                     'source_dataframe')
                if legend.lower() == 'auto':
                    legend = [y_i if isinstance(y_i, str) else '' for y_i in y]
                y = [source_dataframe[y_i].values for y_i in y]
            else:
                if y not in source_dataframe.keys():
                    raise ValueError('The value of y is not a key of the '
                                     'DataFrame provided in source_dataframe')
                if legend.lower() == 'auto':
                    if isinstance(y, str):
                        legend = str(y)
                y = [source_dataframe[y]]

            if x is None:
                # Be careful, the behavior is different for a dict and for a
                # Dataframe
                x = source_dataframe.index.values
            elif isinstance(x, (list, np.ndarray)):
                if not all([x_i in source_dataframe.keys() for x_i in x]):
                    raise ValueError('At least some of the values of x are '
                                     'not keys of the DataFrame provided in '
                                     'source_dataframe')
                x = [source_dataframe[x_i].values for x_i in x]
            else:
                if x not in source_dataframe.keys():
                    raise ValueError('The value of x is not a key of the '
                                     'DataFrame provided in source_dataframe')
                x = source_dataframe[x].values

    # We pre-process `x` and `y`
    if x is None:
        if isinstance(y[0], (list, np.ndarray, tuple)):
            x = [np.arange(len(y_i)) for y_i in y]
        else:
            x = [np.arange(len(y))]
            y = [y]
    elif np.ndim(x) == 1:
        if np.ndim(y) == 1:
            x = [x]
            y = [y]
        elif np.ndim(y) == 2:
            x = [x for _ in y]
    elif np.ndim(x) == 2:
        if np.ndim(y) == 1:  # Corner case
            y = [y for _ in x]

    # We pre-process `color`
    _color_bar_made = False
    if color is None:
        nb_color_needed = len(y)
        color = palette_from_name_to_function[session.palette_name](
            nb_color_needed)
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
                if ((len(np.unique(color)) / len(color)) <= 0.5) and (
                  len(np.unique(color) < 9)):
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

    # We pre-process `line_width`
    if isinstance(line_width, numbers.Real):
        line_width = [line_width for _ in y]
    elif isinstance(line_width, (list, np.ndarray, tuple)):
        if len(line_width) != len(y):
            raise ValueError('The line_width argument given is non consistent '
                             'with the data')

    # We pre-process `alpha`
    if isinstance(alpha, numbers.Real):
        alpha = [alpha for _ in y]
    elif isinstance(alpha, (list, np.ndarray, tuple)):
        if len(alpha) != len(y):
            raise ValueError(
                'The alpha argument given is non consistent '
                'with the data')

    # We pre-process `style`
    if isinstance(style, str):
        style = [style.lower() for _ in y]
    elif isinstance(style, (list, np.ndarray, tuple)):
        if len(style) != len(y):
            raise ValueError(
                'The style argument given is non consistent '
                'with the data')
        style = [s.lower() for s in style]

    def guess_style(style):
        # This list is to be completted to match as much as possible with
        # Matplotlib equivalent attribute
        if style in ['-', '--', '---']:
            return 'dashed'
        elif style in ['.', '..', '...']:
            return 'dotted'
        elif style == '.-':
            return 'dotdash'
        elif style == '-.':
            return 'dashdot'
        else:
            return style
    style = [guess_style(s) for s in style]

    # We pre-process `x_axis_type` and `y_axis_type`
    if x_axis_type.lower() == 'auto':
        if isinstance(x[0][0], numbers.Real):
            x_axis_type = 'linear'
        else:
            try:
                pd.to_datetime(x[0][0], errors='raise')
            except ValueError:
                # TODO: Change message error can x[0][0] may not make sense for
                # the user. Same for y axis below
                error_msg = (
                    '`x_axis_type` is set to `auto` and x[0][0] '
                    'is neither a number, nor an object parsable '
                    'as a date. Object x[0][0]: {}'
                ).format(x[0][0])
                raise ValueError(error_msg)
            x_axis_type = 'datetime'
            x = [pd.to_datetime(x_i) for x_i in x]
    elif x_axis_type.lower() in ['numeric', 'numerical']:
        x_axis_type = 'linear'
    elif x_axis_type.lower() in ['date', 'datetime', 'time']:
        x_axis_type = 'datetime'
        x = [pd.to_datetime(x_i) for x_i in x]
    # Same with y axis
    if y_axis_type.lower() == 'auto':
        if isinstance(y[0][0], numbers.Real):
            y_axis_type = 'linear'
        else:
            try:
                pd.to_datetime(y[0][0], errors='raise')
            except ValueError:
                error_msg = (
                    '`y_axis_type` is set to `auto` and y[0][0] '
                    'is neither a number, nor an object parsable '
                    'as a date. Object y[0][0]: {}'
                ).format(y[0][0])
                raise ValueError(error_msg)
            y_axis_type = 'datetime'
            y = [pd.to_datetime(y_i) for y_i in y]
    elif y_axis_type.lower() in ['numeric', 'numerical']:
        y_axis_type = 'linear'
    elif y_axis_type.lower() in ['date', 'datetime', 'time']:
        y_axis_type = 'datetime'
        y = [pd.to_datetime(y_i) for y_i in y]

    steps = []
    legend_exist = False
    for (x_i, y_i, col_i, leg_i, lw_i, a_i, s_i) in zip(x, y, color, legend,
                                                        line_width, alpha,
                                                        style):
        if leg_i:
            legend_exist = True

            def step(f, x_copy=x_i, y_copy=y_i, col_c=col_i, leg_c=leg_i,
                     lw_c=lw_i, a_c=a_i, s_c=s_i):
                f.line(x=x_copy, y=y_copy, color=col_c, legend_label=leg_c,
                       line_width=lw_c, alpha=a_c, line_dash=s_c)
        else:
            def step(f, x_copy=x_i, y_copy=y_i, col_c=col_i, lw_c=lw_i,
                     a_c=a_i, s_c=s_i):
                f.line(x=x_copy, y=y_copy, color=col_c, line_width=lw_c,
                       alpha=a_c, line_dash=s_c)
        steps.append(step)

    if legend_exist:
        def make_legend_interactive(f):
            f.legend.click_policy = "hide"
        steps.append(make_legend_interactive)

    if fill_between:
        if len(y) == 1:
            pass
            # TODO: Add warning and a piece of code to explain how to fill the
            #  area between 2 curves
        elif len(y) >= 2:
            if not all(x[0] == x[1]):
                # TODO: Transform this error into a warning and explain better
                raise ValueError('When `fill_between` is True, x[0] and x[1] '
                                 'must be the same.')

            def fill_between_curves(f, x_0=x[0], y_0=y[0], y_1=y[1]):
                f.varea(x=x_0, y1=y_0, y2=y_1, alpha=alpha[0], color=color[0])
            steps.append(fill_between_curves)

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
        if x_range is not None:
            if not is_iterable(x_range):
                raise ValueError('`x_range` argument should be an iterable')
            fig.x_range = Range1d(x_range[0], x_range[1])
        if y_range is not None:
            if not is_iterable(y_range):
                raise ValueError('`y_range` argument should be an iterable')
            fig.y_range = Range1d(y_range[0], y_range[1])
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


def _update_line_default_args(line, session):
    def line_updated(y, x=None, source_dataframe=None, width=session.width,
                     height=session.height, description=session.description,
                     title=session.title, x_label=None, y_label=None,
                     show_plot=session.show_plot, color=None,
                     colorbar_type='auto', legend='auto', line_width=1,
                     alpha=1, style='solid', x_axis_type='auto',
                     y_axis_type='auto', x_range=None, y_range=None,
                     fill_between=False, save_path=session.save_path,
                     grid_visible=session.grid_visible):
        """Plot a graph with one-dimensional line(s)

        Args:
            y (array-like of dimension 1 or 2): The y-coordinates for the
                points of the line(s). If `y` is 1-d, one line will be drawn,
                if  it is 2-d, a set of lines will be drawn.
                The values can be either numbers, or dates (datetimes or
                parsable strings). If a `source_dataframe` is given, `x` and
                `y` should be column names / keys.

            x (None, array-like of dimension 1 or 2): The x-coordinates for the
                points of the line(s). If `None`, indexes starting from 0 and
                adapted to `y` will be used. If `y` is 1-d, one line will be
                drawn, if  it is 2-d, a set of lines will be drawn.
                The values can be either numbers, or dates (datetimes or
                parsable strings). If a `source_dataframe` is given, `x` and
                `y` should be column names / keys.

            source_dataframe (None, Pandas DataFrame or dict): Input data as
                Pandas DataFrame or dictionary. If it is a Pandas DataFrame,
                and `x` is None, the index of the dataframe is used as `x`

            width (int): The width of the graph, including any axes, titles,
                etc

            height (int): The height of the graph, including any axes, titles,
                etc

            description (str): HTML-formatted text that will be kept bellow the
                graph. It generally includes metadata, details about the,
                graphs, etc. It will be kept when the graph is displayed,
                exported or rendered in a grid with other graphs. If The graph
                is summed with other graph, their metadata will be concatenated
                (adding a new line between both)

            title (str): Title of the graph. The attributes of the title
                (font), cannot be tuned directly in depict

            x_label (None, str): Label of the x-axis

            y_label (None, str): Label of the y-axis

            show_plot (bool): Whether or not the graph must be displayed
                immediatly after its creation

            color (None, str, array-like): If None, the first color of the
                palette is used.
                If string, a color name is expected (hexadecimal, RGB, and
                usual colors are accepted), and it will be the same for all
                the lines.
                If array-like, the length of color should correspond to the
                number of lines drawn, they will correspond to each line
                respectively

            colorbar_type ({`auto`, `categorical`, `continuous`}): If 'auto',
                the best type will be chosen wrt the data. If `categorical`:
                a legend will be used, not a colorbar. If `continuous`, a
                colorbar will be displayed on the right side of the plot.
                The data defining the color must be passed in `color`

            legend ('auto', array-like): If `auto`, the legend will be set when
                a Pandas DataFrame ora dictionary is provided (the name of the
                columns / keys will be the legend). If array-like, the length
                of `legend` must match with the number of curves dranw

            line_width (Number, array-like): Width of the line(s). If Number
                it will the same for all the lines. If it is an array-like,
                its length must match with the number of lines drawn. They will
                correspond to each line respectively

            alpha (Number, array-like): Alpha value of the line(s). If Number
                it will the same for all the lines. If it is an array-like,
                its length must match with the number of lines drawn. They will
                correspond to each line respectively

            style ({'solid', 'dashed', 'dotted', 'dotdash', dashdot'} or array
                like of those): Style of the line(s). If it is an array-like,
                its length must match with the number of lines drawn. They will
                correspond to each line respectively

            x_axis_type ({'auto', 'numerical', 'datetime'}): Type of the axis.
                If 'auto', the type will be set automatically based on the data
                provided. If 'numerical', 'datetime', the type is set
                accordingly

            y_axis_type ({'auto', 'numerical', 'datetime'}): Type of the axis.
                If 'auto', the type will be set automatically based on the data
                provided. If 'numerical', 'datetime', the type is set
                accordingly

            x_range (array-like): Range of the x-axis

            y_range (array-like): Range of the y-axis

            fill_between (bool): If True, there must be at least 2 curves to
                plot and the area between the first 2 curves is filled. The
                color of the first line and its alpha value are used for the
                part filled. In depict, you cannot have more control about
                this area

            save_path (None, str): If None, the graph is not saved. If str,
                the graph is saved in html at the gicen path. If the html
                extension is missing, it will be added automatically

            grid_visible (bool): Whether the background grid must be displayed.
                In depict, you cannot have further control about the background
                grid

        Returns:
            None
        """
        plot = line(y=y, x=x, source_dataframe=source_dataframe, width=width,
                    height=height, description=description, title=title,
                    x_label=x_label, y_label=y_label, show_plot=show_plot,
                    color=color, colorbar_type=colorbar_type, legend=legend,
                    line_width=line_width, alpha=alpha, style=style,
                    x_axis_type=x_axis_type, y_axis_type=y_axis_type,
                    x_range=x_range, y_range=y_range,
                    fill_between=fill_between, grid_visible=grid_visible,
                    session=session, save_path=save_path)
        return plot
    return line_updated
