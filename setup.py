from setuptools import setup, find_packages


with open('README.md') as f:
  readme = f.read()

with open('LICENSE') as f:
  license = f.read()

setup(
  name='modelexp',
  version='0.1.0',
  description='General purpose package to fit models to experimental data',
  url='https://github.com/DomiDre/modelexp',
  author='Dominique Dresen',
  author_email='dominique.dresen@uni-koeln.de',
  license=license,
  long_description=readme,
  install_requires=[
    'numpy',
    'matplotlib'
  ],
  python_requires='>2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
  platforms=['Linux'],
  package_dir={'modelexp': 'modelexp'},
  packages=[
    'modelexp',
    'modelexp._data',
    'modelexp._gui',
    'modelexp._experiment',
    'modelexp._fit',
  ],
  keywords='model data experiment science'
)
  # packages=find_packages(
  #   exclude=(
  #     '_build',
  #     'docs',
  #     '_static',
  #     '_templates'
  #     'tests',
  #     )
  # )
