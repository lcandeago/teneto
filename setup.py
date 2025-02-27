"""
General setup for module
"""

from setuptools import setup, find_packages

setup(name='teneto',
      version='0.4.5',
      python_requires='>3.5',
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      install_requires=[
		'nilearn>=0.4.0',
		'pybids>=0.7.1',
        'statsmodels>=0.8.0',
        'networkx>=2.0',
        'python-louvain>=0.13',
        'pandas>=0.21',
        'scipy>=1.0.0',
        'numpy>=1.15.1',
        'templateflow>=0.3'],
      description='Temporal network tools',
      packages=find_packages(),
      author='William Hedley Thompson',
      author_email='hedley@startmail.com',
      url='https://www.github.com/wiheto/teneto',
      download_url='https://github.com/wiheto/teneto/archive/0.3.3.tar.gz',
      package_data={'':['./teneto/data']},
      include_package_data = True,
      entry_points={
      'console_scripts': ['teneto = teneto.__main__:main'
          ]
      },
      long_description='Temporal network tools. A package for deriving, analysing and plotting temporal network representations. Additional tools for temporal network analysis with neuroimaging contexts.'
      )
