from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="arxiv_collector",
    version="0.0.1",
    author="Wing-Kit Lee",
    author_email="wklee4993@gmail.com",
    description="A package to collect abstracts from arxiv.org",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wingkitlee/arxiv_collector",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['arxiv-collect=arxiv_collector.collect:main']
    }
)
