from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="Hotel Reservation Prediction APP",
    description="This is an end to end machine learning project with GCP, Zenkins, MLFLOW, Docker, Flask to show the demostration of mlops",
    version="1.0.0",
    author="Amaresh",
    packages=find_packages(),
    install_requires=requirements
)