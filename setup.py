from setuptools import setup, find_packages

setup(
    name="cybexdump",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "mysql-connector-python",
        "rich",
        "schedule",
        "python-crontab",  # installs as 'crontab'
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "cybexdump=cybexdump.cli:main",
        ],
    },
    python_requires=">=3.7",
)
