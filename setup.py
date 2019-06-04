from setuptools import setup, find_packages

setup(
    name='PythonBuildForLinux',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
            'argcomplete',
    ],
    entry_points={
        'console_scripts': [
            'pbl = pab:main',
        ],
    },
)
