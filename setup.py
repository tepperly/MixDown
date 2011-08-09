'''
Setup file for installing MixDown
'''
from setuptools import setup

setup(
 name = "mixdown",
 version = "1.0",
 author = "Tom Epperly, Chris White, Lorin Hochstein, Prakashkumar Thiagarajan",
 author_email = "epperly2@llnl.gov, white238@llnl.gov, lorinh@gmail.com, tprak@seas.upenn.edu",
 url = "https://github.com/tepperly/MixDown/",
 packages = ['md'],
 scripts = ['MixDown'],
 description = "Meta-build tool for managing collections of third-party libraries",
)
