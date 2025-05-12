from setuptools import setup, find_packages

setup(
    name="finance-agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "twilio",
        "google-api-python-client",
        "openai"
    ],
) 