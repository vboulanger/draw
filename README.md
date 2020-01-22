<img src="https://raw.githubusercontent.com/vboulanger/depict/master/logo_and_name.png" alt = "drawing" WIDTH=500/></img>

<br>

<a href="https://travis-ci.com/vboulanger/depict">
<img src="https://travis-ci.com/vboulanger/depict.svg?branch=master" alt="CI" />
</a>

<a href='https://depict.readthedocs.io/en/latest/?badge=latest'>
<img src='https://readthedocs.org/projects/depict/badge/?version=latest' alt='Documentation Status' />
</a>

<a href="https://pypi.org/project/depict/">
<img src="https://img.shields.io/pypi/v/depict.svg" alt="latest release" />
</a>
<a href="https://pypi.org/project/depict/">
<img src="https://img.shields.io/pypi/status/depict.svg" alt="status" />
</a>
<a href="https://pypi.org/project/depict/">
<img src="https://img.shields.io/pypi/l/depict.svg" alt="license" />
</a>
<a href="https://pepy.tech/project/depict">
<img src="https://pepy.tech/badge/depict" alt="download" />
</a>

**Business grade visualizations in seconds.**


Depict is built on the top of Bokeh. It aims at providing one-line access 
to the most common types of graph by setting opinionated default and avoiding 
boilerplate code. Graphs are aesthetic, efficiently rendered, interactive and
sharable.

It is made for data-{scientist, analyst, engineer, lead, etc} seeking to 
create beautiful plots while reducing the graph-tweaking time.

# Guiding principles
* **Made simple**

While Bokeh, Matplotlib, Dash and many others provide a tremendous flexibility,
Depict will get you faster to the classical graphs by making choices for you.
Scatter plots, histograms and other heat-maps are accessible in one line.
* **Looking fresh**

Graphs should be ready to share and pleasant to look at, for technical and 
 non technical audience. Depict takes care of the freshness of your graphs
 to let you focus on the maths. 
* **Stay organized**

Depict helps you save you graphs in html with textual metadata and share them
around. Your plots are kept interactive, contextualized and readable in the
browser.

* **Infinitely customizable with Bokeh**

You want to personalize you graph further? You can use Bokeh glyphs to 
interact with depict figure and get access to a fine level of granularity.

# Install


* Install depict from PyPI (recommended):

    `pip install depict`

* Install depict from GitHub sources:
    
    Clone the git repository
     
    `git clone https://github.com/vboulanger/depict.git`
   
    Inside the depict folder, install the package
    
  ```
  cd depict  
  sudo python setup.py install
  ```

# Documentation
The documentation can be found at: [https://depict.readthedocs.io](https://depict.readthedocs.io).


# Get started
### Hello world

```python
import depict

depict.line([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])
```
![Image_1](https://raw.githubusercontent.com/vboulanger/depict/master/images_read_me/plot_1.png)

### Key features
Common to all examples:
```python
import depict
import numpy as np
import pandas as pd
```
* #### One line graphs
```python
random_walk = np.cumsum(np.random.rand(1000) - 0.5)
depict.line(random_walk, title='Random walk', legend='Path', x_label='Step')
```
![Image_1](https://raw.githubusercontent.com/vboulanger/depict/master/images_read_me/plot_random_walk.png)
* #### Sessions
Your graph parameters are stored in a session to keep your graphs visually
consistent and avoid boilerplate code.
```python
depict.session(width=1000, grid_visible=True, palette_name='linear_blue')
```

* #### Color bars made easy
```python
x = np.random.random(1000)
y = np.random.random(1000)
color = np.sin(x) + np.sin(y)

depict.point(x=x, y=y, color=color)
```
![Image_1](https://raw.githubusercontent.com/vboulanger/depict/master/images_read_me/colorbar.png)


* #### Smart date handling and parsing
```python
x = ['Jan 2018', 'Feb 2018', 'Mar 2018', 'Apr 2018']
y = [1.1, 2.2, 1.9, 2.8]
depict.histogram(x=x, y=y)
```
![Image_1](https://raw.githubusercontent.com/vboulanger/depict/master/images_read_me/datetime_parsing.png)

* #### Flexibility
Native compatibility with numpy arrays and pandas dataframes as well as NaN and
NaT handling.
```python
random_walk = lambda : np.cumsum(np.random.rand(1000) - 0.5)
df = pd.DataFrame({'Col 1': random_walk(), 'Col 2': random_walk()})

depict.line(y=['Col 1', 'Col 2'], source_dataframe=df)
```
![Image_1](https://raw.githubusercontent.com/vboulanger/depict/master/images_read_me/plot_random_walk_2.png)

* #### Matrix-like layout
You plots can be rendered in line and column just like a matrix would be.
```python
random_walk = lambda : np.cumsum(np.random.rand(1000) - 0.5)
plot_1 = depict.line(y=random_walk(), title='Walk 1', show_plot=False)
plot_2 = depict.line(y=random_walk(), title='Walk 2', show_plot=False)
plot_3 = depict.line(y=random_walk(), title='Walk 3', show_plot=False)

depict.show([[plot_1, plot_2], [plot_3]])
```
![Image_1](https://raw.githubusercontent.com/vboulanger/depict/master/images_read_me/matrix-like-layout.png)

* #### Sum graphs, just like numbers
Plots sharing a consistent background space can be summed and their content
will be superimposed.
```python
p_1 = depict.point(x=np.arange(10), y=np.arange(10) + np.random.rand(10))
p_2 = depict.line(y=np.arange(10), color='purple')
p_sum = p_1 + p_2

depict.show([[p_1, p_2], p_sum])
```
![Image_1](https://raw.githubusercontent.com/vboulanger/depict/master/images_read_me/sum_graph.png)

* #### Textual metadata
Graphs often come along with a context. For that reason you can add
HTML-formatted text to be displayed below your graph.

```python
description = """
<h2>Graph generated for the README</h2>
<br>
HTML code can be added here
"""
plot_1 = depict.histogram(np.random.rand(10), description=description)
```
![Image_1](https://raw.githubusercontent.com/vboulanger/depict/master/images_read_me/hist_example_context.png)

* #### Direct access to Bokeh figure
To access a finer level of customization, you can retrieve the Bokeh figure
object easily and interact with it.  
```python
plot = depict.histogram(x=None, y=[1, 2, 3], show_plot=False)
plot.figure  # This is a Bokeh figure
```
* #### HTML export
Graphs as HTML files allow you to keep them fully interactive and readable
without any specific software and on several platforms.

```python
depict.point(x=[1, 2, 3], y=[4, 5, 2], save_path='my_plot.html')
```

* #### Jupyter notebook / JupyterLab integration
Bokeh is nicely integrated in Jupyter notebooks and so does Depict.

![Image_1](https://raw.githubusercontent.com/vboulanger/depict/master/images_read_me/notebook_integration.png)


# Contributing
The development of Depict takes place on Github. Any contribution is welcome!
 

