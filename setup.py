from setuptools import setup, find_packages

setup(
    name="shellutils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "v = shellutils.v:main",
            "todo = shellutils.todo:main",
        ],
    },
    author="Morten Hustveit",
    author_email="morten.hustveit@gmail.com",
    description="Miscellaneous shell utilities.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mortehu/shellutils",
)
