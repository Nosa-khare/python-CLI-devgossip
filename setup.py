import setuptools

with open("README.md", "r") as description:
    long_description = description.read()

setuptools.setup(
    name="DevGossip-Nosakhare", # Replace with your own username
    version="0.2.0",
    author="Nosakhare Edokpayi",
    author_email="co.nosakhare@gmail.com",
    entry_points={'console_scripts': ['CLI-DevGossip = DevGossip.__main__:main']},
    description="A package of a light weight chat application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nosa-khare/CLI-DevGossip",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
