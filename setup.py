from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("VERSION") as version_file:
    version = version_file.read().strip()

setup(
    name="prompt_parser",
    version=version,
    author="Alexandru Mariuti",
    author_email="alex@mariuti.com",
    description="A simple Python library for parsing LLM prompts.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nank1ro/prompt-parser",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    project_urls={
        "GitHub": "https://github.com/nank1ro/prompt-parser",
        "Changelog": "https://github.com/nank1ro/prompt-parser/blob/main/CHANGELOG.md",
    },
)
