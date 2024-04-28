#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='cli password manager',
      version='1.0',
      packages=find_packages(),
      scripts=['pm_cli.py'],
      )
