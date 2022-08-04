from setuptools import setup
from pathlib import Path


scripts = [str(p) for p in Path(__file__).parent.joinpath('scripts').iterdir()]


setup(
    name='cog-example',
    scripts=scripts,
    install_requires=[
        'cogapp~=3.3',
    ],
)
