from setuptools import find_packages, setup

setup(
    name='fwutil',
    packages=find_packages(),
    description='File writing util',
    author='1fexd',
    license='GPL-3',
    setuptools_git_versioning={"enabled": True},
    setup_requires=["setuptools-git-versioning<2"]
)
