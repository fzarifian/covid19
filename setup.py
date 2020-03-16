from setuptools import setup, find_packages


setup(
    name='covid19',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        covid19=covid19.click:cli
    ''',
)
