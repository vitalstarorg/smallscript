from setuptools import setup, find_packages

setup(
    name='smallscript',
    version='0.3.4',
    packages=find_packages(),
    install_requires=[
        'antlr4-python3-runtime',
        'graphviz'
    ],
    author='Man Chan',
    author_email='man.chan@gmail.com',
    description='smallscript',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vitalstarorg/smallscript',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)