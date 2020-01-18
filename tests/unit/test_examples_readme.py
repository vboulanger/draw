import pytest
import depict
import numpy as np
import pandas as pd


def test_read_me(tmpdir):

    depict.line([3, 1, 4, 1, 5, 9, 2, 6, 5, 3], show_plot=False)

    random_walk = np.cumsum(np.random.rand(1000) - 0.5)
    depict.line(random_walk, title='Random walk', legend='Path',
                x_label='Step', show_plot=False)

    depict.session(width=1000, grid_visible=True, palette_name='linear_blue')

    x = np.random.random(1000)
    y = np.random.random(1000)
    color = np.sin(x) + np.sin(y)

    depict.point(x=x, y=y, color=color, show_plot=False)

    x = ['Jan 2018', 'Feb 2018', 'Mar 2018', 'Apr 2018']
    y = [1.1, 2.2, 1.9, 2.8]
    depict.histogram(x=x, y=y, show_plot=False)

    def random_walk():
        return np.cumsum(np.random.rand(1000) - 0.5)
    df = pd.DataFrame({'Col 1': random_walk(), 'Col 2': random_walk()})

    depict.line(y=['Col 1', 'Col 2'], source_dataframe=df, show_plot=False)

    plot_1 = depict.line(y=random_walk(), title='Walk 1', show_plot=False)
    plot_2 = depict.line(y=random_walk(), title='Walk 2', show_plot=False)
    plot_3 = depict.line(y=random_walk(), title='Walk 3', show_plot=False)

    p_1 = depict.point(x=np.arange(10), y=np.arange(10) + np.random.rand(10),
                       show_plot=False)
    p_2 = depict.line(y=np.arange(10), color='purple', show_plot=False)
    p_sum = p_1 + p_2

    description = """
    <h2>Graph generated for the README</h2>
    <br>
    HTML code can be added here
    """
    plot_1 = depict.histogram(np.random.rand(10), description=description,
                              show_plot=False)

    plot = depict.histogram(x=None, y=[1, 2, 3], show_plot=False)
    plot.figure

    depict.point(x=[1, 2, 3], y=[4, 5, 2],
                 save_path=str(tmpdir.join('test.html')), show_plot=False)








