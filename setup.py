from setuptools import setup

setup(
    name='pyGoDaddyAUpdater',
    version='1.0',
    packages=['pyGoDaddyUpdater', 'pyGoDaddyUpdater.values', 'pyGoDaddyUpdater.network', 'pyGoDaddyUpdater.preferences',
              'pyGoDaddyUpdater.logging_utils'],
    url='https://gitlab.javinator9889.com/Javinator9889/pyGoDaddyAUpdater',
    license='GNU General Public License v3.0',
    author='Javinator9889',
    author_email='',
    description='DDNS service for dynamically update GoDaddy A Record'
)
