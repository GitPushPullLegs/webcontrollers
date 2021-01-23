from setuptools import setup, find_packages

setup(
    name='webcontrollers',
    version='0.0.11',
    description='A package to faciliate the interaction with CAASPP, SEIS, and more.',
    url='https://github.com/GitPushPullLegs/webcontrollers',
    author='Joe Aguilar',
    author_email='jose.aguilar.6694@gmail.com',
    license='MIT License',
    packages=find_packages(exclude=[]),
    install_requires=['selenium',
                      'wait @ git+https://github.com/GitPushPullLegs/wait.git',
                      'python-dateutil'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    package_data={'': ['webcontrollers/common/drivers/chromedriver.exe', 'webcontrollers/common/html/welcome.html']},
    include_package_data=True,
)