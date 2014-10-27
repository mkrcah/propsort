from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = "propsort",
    version = "0.1-dev",
    author = "Marcel Krcah",
    author_email = "marcel.krcah@gmail.com",
    description = "Sort your Java/Scala/Play properties file according to a template.",
    license = "MIT",
    keywords = "java scala play properties file i18n",
    url = "https://github.com/mkrcah/propsort",
    packages = find_packages(),
    include_package_data=True,
    entry_points = {'console_scripts': ['propsort=propsort.main:cli']},
    install_requires=requirements
)