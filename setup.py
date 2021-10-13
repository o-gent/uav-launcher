# https://setuptools.pypa.io/en/latest/userguide/quickstart.html

from setuptools import setup

setup(
    name='uav_launcher',
    version='0.0.1',
    packages=['uav_launcher'],
    install_requires=[
        'odrive',
    ],
)