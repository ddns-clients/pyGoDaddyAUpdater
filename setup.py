from setuptools import setup

setup(
    name='pyGoDaddyUpdater',
    version='1.0',
    packages=['pyGoDaddyUpdater',
              'pyGoDaddyUpdater.values',
              'pyGoDaddyUpdater.network',
              'pyGoDaddyUpdater.preferences',
              'pyGoDaddyUpdater.logging_utils'],
    url='https://gitlab.javinator9889.com/Javinator9889/pyGoDaddyAUpdater',
    license='GPL-3.0',
    author='Javinator9889',
    author_email='javialonso007@hotmail.es',
    description='DDNS service for dynamically update GoDaddy A Records',
    include_package_data=False,
    zip_safe=True,
    download_url="https://gitlab.javinator9889.com/Javinator9889/pyGoDaddyAUpdater/repository/master/archive.zip",
    entry_points={
        'console_scripts': ['godaddy_ddns=pyGoDaddyUpdater.__main__:parser()']
    },
    install_requires=['daemonize'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
