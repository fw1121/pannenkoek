from setuptools import setup, find_packages
from setuptools.command.install import install
from codecs import open
from os import path


# Get the long description from the relevant file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        print "Installing Pannenkoek!"
        install.run(self)



setup(
    name = "pannenkoek",
      long_description=long_description,
    version = "0.1.8",
    packages = find_packages(),
    scripts = ['pannenkoek/pannenkoek.py', 'pannenkoek/lefse/format_input.py', 'pannenkoek/lefse/run_lefse.py', 'pannenkoek/lefse/lefse.py'],

    # Project uses reStructuredText, so ensure that the
    # docutils get installed or upgraded on the target
    # machine
    install_requires = ['rpy2', 'numpy', 'matplotlib', 'argparse', 'pandas', 'biopython'],
      
      cmdclass={
      'install': CustomInstallCommand,
      },
      
      

    package_data = {
        # If any package contains *.txt or *.rst files,
        # include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the
        # 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Thomas W. Battaglia",
    author_email = "tb1280@nyu.com",
    description = "A wrapper for Qiime and LEfSe analysis. Split an OTU table by time and make certain comparisons with ease.",
    license = "MIT",
    keywords = "Biology Microbiome LEFSE QIIME Formatting Diversity Python Bioinformatics",

    # project home page, if any :
    url = "https://github.com/twbattaglia/pannenkoek",

    # could also include long_description, download_url,
    # classifiers, etc.
)
