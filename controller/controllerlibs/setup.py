from setuptools import setup, find_packages

setup(
    name='controllerlibs',
    version='0.1.0',
    description='shared libraries of controller',
    url='',
    author='nobuyuki matsui',
    author_email='nobuyuki.matsui@gmail.com',
    license='',
    keywords='',
    packages=find_packages(),
    install_requires=[
        "Flask>=1.0",
        "requests>=2.18",
        "pytz>=2018.5",
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
