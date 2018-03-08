from pip.req import parse_requirements
from setuptools import find_packages, setup

install_reqs = parse_requirements("requirements.txt", session=False)

# requirements is a list of requirements
requirements = [str(ir.req) for ir in install_reqs if ir.req is not None]

setup(
    name='bq_models',
    version='0.1.0',
    packages=find_packages(exclude=['tests*']),
    description='BQ Manager models',
    author='Clifford Richardson',
    author_email='cmrallen@gmail.com',
    install_requires=requirements
)
