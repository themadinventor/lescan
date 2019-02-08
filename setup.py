from setuptools import setup
from lescan import __version__

setup(
    name='lescan',
    version=__version__,
    author='Fredrik Ahlberg',
    author_email='fredrik@z80.se',
    description='Minimalistic Bluetooth LE scanning utility',
    url='https://github.com/themadinventor/lescan',
    packages=['lescan'],
    install_requires=['gatt'],
    entry_points={
        'console_scripts': ['lescan = lescan.__main__:main'],
    }
)
