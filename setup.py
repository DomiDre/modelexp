from setuptools import setup, find_packages


with open('README.md') as f:
  readme = f.read()

with open('LICENSE') as f:
  license = f.read()

setup(
  name='model.py',
  version='1.0.0',
  author='Dominique Dresen',
  author_email='dominique.dresen@uni-koeln.de',
  url='https://github.com/DomiDre/modelpy',
  description='General purpose package to fit models to data',
  long_description=readme,
  license=license,
  packages=find_packages(exclude=('tests', 'docs'))
)
