from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(
	name='ckanext-dcoform',
	version=version,
	description="",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Yu Chen',
	author_email='cheny18@rpi.edu',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.dcoform'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	# Add plugins here, eg
	dcoform=ckanext.dcoform.plugin:ExampleIDatasetFormPlugin

	""",
)
