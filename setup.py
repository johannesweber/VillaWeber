from setuptools import setup

setup(
    name='VillaWeber',
    packages=['villaweber'],
    include_package_data=True,
    install_requires=[
        'flask',
        'openpyxl',
        'pandas',
        'xknx',
        'sqlalchemy',
        'fritzconnection'
    ],
)