import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="listdir",
    version="1.0.0",
    author="Jonas",
    author_email="jonas.eukan@gmail.com",
    description="A implementation of ls using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Saliovin/listdir",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': ['listdir=listdir.listdir:main'],
    },
    include_package_data=True,
)