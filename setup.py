'''
setup.py is an important part of Python packaging and distribution when a
project uses setuptools. It defines the configuration needed to build,
package, install, and distribute the project.

This configuration can include:
- Project metadata, such as the name, version, description, author, license,
  project URL, and README content.
- Python packages and modules to include in the distribution.
- Runtime dependencies and optional dependencies for additional features
  or development tools.
- Supported Python versions and package classifiers.
- Package data, such as templates, configuration files, and other resources.
- Command-line entry points and executable scripts.
- Build options for compiled extensions and other packaging settings.

Modern projects can declare these settings in pyproject.toml instead.
This comment documents setup.py's purpose; executable configuration is
needed for this file to configure setuptools.
'''


from setuptools import setup, find_packages 
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    Reads the requirements from a file and returns them as a list of strings.

    Args:
        file_path (str): The path to the requirements file.

    Returns:
        List[str]: A list of requirement strings.
    """
    with open('requirements.txt', "r") as f:
        return [line.strip() if line != '-e .' else line.strip() for line in f if line.strip()]



    setup(
        name="mlops-pipeline",
        version="0.1.0",
        description="A machine learning operations (MLOps) pipeline project.",
        author="Anurag Rachoti",
        author_email="anuragrachoti@gmail.com",
        packages=find_packages(),
        install_requires=get_requirements('requirements.txt')
    )
