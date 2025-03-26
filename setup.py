from setuptools import setup, find_packages

setup(
    name="nombres-arg",
    version="0.4.10",
    description="A package for accessing names and last names from Argentina.",
    author="Adrián Zelaya",
    author_email="zelaya.adrian@gmail.com",
    license="CC0-1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "requests",
        "spacy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
