from setuptools import setup, find_packages

setup(
    name="database-remote",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    description="Database Remote Management tool",
    author="wtalioy",
    python_requires=">=3.10",
)