from setuptools import setup, find_packages

setup(
    name="prompt_parser",
    version="0.1.0",
    author="Alexandru Mariuti",
    author_email="alex@mariuti.com",
    description="A simple Python library for parsing LLM prompts.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
