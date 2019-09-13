import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-middleware-filter",
    version="0.0.1",
    author="Winrey",
    author_email="i@iaside.com",
    description="A wrapper to let some of the django middleware only enable for specified route.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/winrey/django-middleware-filter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)