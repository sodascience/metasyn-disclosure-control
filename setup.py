# based on https://github.com/pypa/sampleproject
# MIT License

# Always prefer setuptools over distutils
from setuptools import setup, find_namespace_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='metasynth-disclosure',
    version="0.1",  # noqa
    description='Disclosure control for the MetaSynth package.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sodascience/metasynth-disclosure-control',
    author='Soda Development Team',
    keywords='metasynth disclosure',
    packages=find_namespace_packages(include=['metasynthcontrib.*']),
    install_requires=[
        "metasynth", "numpy",
    ],

    extras_require={
    },

    entry_points={
        "metasynth.disttree": [
            "disclosure = metasynthcontrib.disclosure.disttree:DisclosureDistributionTree",
        ],
    },

    project_urls={
        'Bug Reports':
            "https://github.com/sodascience/metasynth-disclosure-control",
        'Source':
            "https://github.com/sodascience/metasynth-disclosure-control",
    },
)
