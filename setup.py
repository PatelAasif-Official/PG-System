from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in pg_system/__init__.py
from pg_system import __version__ as version

setup(
	name="pg_system",
	version=version,
	description="karkhana.io Assignment",
	author="patelasif52@gmail.com",
	author_email="patelasif52@gmail.com ",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
