from distutils.core import setup

setup(
    name='ijpython_roi',
    version='0.1dev',
    packages=['ijroi',],
    install_requires=['tifffile','ast', 'numpy', 'json'],
)