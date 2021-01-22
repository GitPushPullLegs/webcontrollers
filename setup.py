from setuptools import setup, find_packages

setup(
    name='webcontrollers',
    version='0.0.2',
    description='A package to faciliate the interaction with CAASPP, SEIS, and more.',
    url='https://github.com/GitPushPullLegs/webcontrollers',
    author='Joe Aguilar',
    author_email='jose.aguilar.6694@gmail.com',
    license='MIT License',
    packages=find_packages(),
    install_requires=['selenium'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)