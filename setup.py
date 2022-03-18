from distutils.core import setup

setup(
    name='PyEasyQiwi',
    version='1.0.1',
    packages=['PyEasyQiwi', 'PyEasyQiwi.qiwi_service'],
    install_requires=['requests'],
    url='https://github.com/Kur-up/EasyQiwiAPI',
    license='Apache License 2.0',
    author='Lev Kurapov',
    author_email='kurup.performance@gmail.com',
    long_description=open('README.md').read(),
    description='Library for easy interaction with the P2P API of the Qiwi service!'
)