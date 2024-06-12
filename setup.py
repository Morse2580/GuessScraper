from pathlib import Path
from setuptools import setup, find_namespace_packages


# Load packages from requirements.txt
BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]
    
setup(
    name='my_scraping_project',
    version='0.1.0',
    description='A web scraping project for real estate research',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_namespace_packages(),
    install_requires=[required_packages],
)

