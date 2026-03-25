from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="evocuriosity",
    version="0.2.2",
    description="A local-first Python SDK implementing a cognitive architecture for curiosity-driven AI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daksha Dubey",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "networkx",
        "scipy"
        # Optional: "sentence-transformers" can be installed by the user if advanced embeddings are needed
    ],
    python_requires=">=3.8",
)
