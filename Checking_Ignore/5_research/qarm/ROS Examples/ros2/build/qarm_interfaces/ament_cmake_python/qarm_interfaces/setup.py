from setuptools import find_packages
from setuptools import setup

setup(
    name='qarm_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('qarm_interfaces', 'qarm_interfaces.*')),
)
