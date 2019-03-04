import setuptools
from mutagene.version import __version__

setuptools.setup(name='mutagene',
                 version=__version__,
                 description='Mutational analysis with Python',
                 long_description=open('README.md').read().strip(),
                 long_description_content_type="text/markdown",
                 author='Alexander Goncearenco',
                 author_email='alexandr.goncearenco@nih.gov',
                 url='http://www.ncbi.nlm.nih.gov/projects/mutagene/',
                 install_requires=[
                         'bayesian-optimization',
                         'clustergrammer',
                         'numpy',
                         'pandas',
                         'requests',
                         'scikit-learn',
                         'scipy',
                         'statsmodels',
                         'twobitreader',
                         'tqdm'],
                 test_suite='nose.collector',
                 tests_require=[
                        'nose',
                        'pytest',
                        'pytest-cov',
                        'coverage'],
                 scripts=['bin/mutagene'],
                 packages=['mutagene'],
                 include_package_data=True,
                 license='Public Domain',
                 zip_safe=False,
                 keywords='bioinformatics cancer mutations',
                 classifiers=[
                        'Programming Language :: Python :: 3 :: Only',
                        "Operating System :: OS Independent",
                        'License :: Public Domain',
                        'Development Status :: 4 - Beta',
                        'Intended Audience :: Science/Research',
                        'Topic :: Scientific/Engineering :: Bio-Informatics',
                        'Topic :: Scientific/Engineering :: Medical Science Apps.',
                        'Environment :: Console'
                 ])
