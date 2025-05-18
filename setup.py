from setuptools import setup, find_packages

setup(
    name="amiga_xbox_direct",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
)
