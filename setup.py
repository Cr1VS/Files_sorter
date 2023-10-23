from setuptools import setup, find_namespace_packages

setup(
    name='Files_sorter',
    version='1.0.0',
    author='Vladyslav K.',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['clean=Files_sorter.clean:run']}
)