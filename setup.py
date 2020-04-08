from setuptools import setup, find_packages


setup(
    name='persist',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=0.0.1,

    description='Save (and restore) complicated classes to (and from) a file',
    scripts=[],

    # The project's main homepage.
    url='https://github.com/fergalm/persist',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    package_dir={'': 'persist'},
    packages=find_packages('persist', exclude=[]),
    data_files=[]
)
