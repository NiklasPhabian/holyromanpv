#!/usr/bin/env/python


import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

scripts = ['bin/make_plots.py',
	   'bin/make_html.py',
	   'bin/get_daystats.py',
	   'bin/get_monthstats.py',
	   'bin/get_realtime.py',
	   'bin/get_sce_page.py',
	   'bin/get_sce_page.sh',
	   'bin/kill_chrome.sh',
	   'bin/update_website.sh',
	   'bin/upload_dropbox.py']


setup(
    name="holyromanpv",
    version='0.1',
    description="PV monitor",
    license="MIT",
    author="Niklas Griessbaum",
    author_email="griessbaum@gmail.com",
    packages=[
        "holyromanpv",
    ],
    #scripts=scripts,
    python_requires=">=3.5",
    install_requires=install_requires,
) 
