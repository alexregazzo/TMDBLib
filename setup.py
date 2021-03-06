import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytmdb",
    version="0.0.1",
    author="Alex Regazzo",
    author_email="alex_regazzo@hotmail.com",
    description="This module has the purpose of connecting to TMDB API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexregazzo/TMDBLib",
    project_urls={
        "Bug Tracker": "https://github.com/alexregazzo/TMDBLib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages('.'),
    python_requires=">=3.6",
    install_requires=['requests']
)
