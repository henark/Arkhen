"""
Setup configuration for Framework Arkhen v2.0
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="arkhen-framework",
    version="2.0.0",
    author="Rafael Oliveira",
    author_email="rafael@arkhen.dev",
    description="Framework Arkhen v2.0: Sistemas de Informação Interdimensionais",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/henark/arkhen-framework",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0"
        ],
        "quantum": [
            "qiskit[all]>=0.44.0",
            "cirq>=1.2.0",
            "pennylane>=0.32.0"
        ],
        "simulation": [
            "tensornetwork>=0.4.6",
            "mesa>=2.1.0",
            "vpython>=7.6.4"
        ]
    },
    entry_points={
        "console_scripts": [
            "arkhen=arkhen.cli:main",
            "arkhen-simulate=arkhen.simulation:run_simulation",
            "arkhen-blockchain=arkhen.blockchain:run_network",
        ],
    },
    include_package_data=True,
    package_data={
        "arkhen": [
            "data/*.json",
            "config/*.yaml",
            "templates/*.html"
        ]
    },
    keywords=[
        "quantum computing",
        "blockchain", 
        "cosmology",
        "universe simulation",
        "NMSI",
        "quantum mechanics",
        "distributed systems",
        "artificial intelligence"
    ],
    project_urls={
        "Bug Reports": "https://github.com/henark/arkhen-framework/issues",
        "Source": "https://github.com/henark/arkhen-framework",
        "Documentation": "https://arkhen-framework.readthedocs.io/",
    },
)