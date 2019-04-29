import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typeform_advancedapi",
	install_requires=[
          'requests>=2.21.0'
      ],
    version="1.1.6",
    author='Anton Kaiser',
    author_email='kaiser@kaiser.ovh',
    description="TypeForm API written in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaiseranton/TypeForm_AdvancedAPI",
    packages=['typeform_advancedapi'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)