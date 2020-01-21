import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="depict",
    version="0.1.5",
    author="Victor Boulanger",
    author_email="vb@live.fr",
    description="Business grade visualizations in seconds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vboulanger/depict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.5',
    install_requires=['bokeh>=1.4.0', 'seaborn>=0.9.0', 'pandas>=0.24.2'],
    extras_require={'test': ['pytest', 'pycodestyle'],
                    'doc': ['Sphinx', 'sphinx-rtd-theme']},
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
)

# https://pypi.org/classifiers/
