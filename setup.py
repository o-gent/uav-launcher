# https://setuptools.pypa.io/en/latest/userguide/quickstart.html

from setuptools import setup

setup(
    name='uav_launcher',
    version='1.0.0',
    packages=['uav_launcher'],
    install_requires=[
        'odrive',
    ],
)