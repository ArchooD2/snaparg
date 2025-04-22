from setuptools import setup, find_packages

setup(
    name='snaparg',
    version='0.1.0',
    packages=find_packages(),
    description='A typo-tolerant CLI parser wrapper for argparse',
    author='PJ Hayes',
    author_email='archood2next@gmail.com',
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6',
)
