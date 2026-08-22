from setuptools import setup, find_packages

setup(
    name="samdas",
    version="1.0.0",
    description="SAMDAS: Zero-Trust Cognitive Firewall SDK for Autonomous AI",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "websockets",
        "pydantic",
        "sentence-transformers",
        "scipy",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "samdas-dashboard=samdas.cli:run_dashboard",
        ],
    },
)