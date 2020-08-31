from setuptools import setup, find_packages

setup(
    name = "key-value-server",
    version = "0.0.1",
    author = "Kristof Jakab",
    author_email = "kristof.jakab@gmail",
    description = "Basic key-value server for demonstration purposes only",
    url = "https://github.com/jakabk/key-value-server.git",
    install_requires = [
        "pickleDB~=0.9",
    ],
    extras_require = {
        "test": [
            "pytest~=5.3",
            "pytest-cov~=2.8",
            "pytest-watch~=4.2",
        ],
    },
    packages = find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX:: Linux",
    ],
    python_requires = '>=3.7',
)
