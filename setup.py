from setuptools import setup, find_packages

setup(
    name="evocuriosity",
    version="0.1.0",
    description="A local-first Python SDK implementing a cognitive architecture for curiosity-driven AI.",
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
