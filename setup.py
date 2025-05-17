from setuptools import setup, find_packages

setup(
    name='amiga_xbox_direct',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'farm-ng-amiga',
        'evdev',
    ],
    entry_points={
        'console_scripts': [
            'amiga_xbox_direct=amiga_xbox_direct.main:run_joystick_control',
        ],
    },
)
