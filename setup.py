from setuptools import setup
import fractal_output

long_description = open('README.rst', 'r').read()

setup(
    name='fractal_output',
    version=fractal_output.__version__,
    packages=['fractal_output'],
    setup_requires=['wheel'],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "fractal_output = fractal_output.__main__:__main__"
        ],
    },
    description="The task manager for python",
    long_description=long_description,
    url='https://github.com/jefersondaniel/fractal-output',
    author='Jeferson Daniel',
    author_email='jeferson.daniel412@gmail.com',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
