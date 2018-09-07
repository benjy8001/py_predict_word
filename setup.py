from setuptools import setup, find_packages

__NAME__ = 'predict'
__VERSION__ = '0.1'


setup(
    name=__NAME__,
    version=__VERSION__,
    description="predict",
    author='Benjamin Mabille',
    author_email='benjy80@gmail.com',
    url='https://github.com/benjy8001/',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'predict = predict.main:main',
        ]
    },
    package_data={
        'predict.lib': ['picoTTS'],
    },
)
