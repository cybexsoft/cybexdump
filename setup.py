from setuptools import setup, find_packages
import os

# Create a simple launcher script
with open('cybexdump_launcher.py', 'w') as f:
    f.write('''#!/usr/bin/env python3
import sys
import os

# Add package root to Python path
package_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, package_root)

from cybexdump.cli import cli

if __name__ == '__main__':
    cli()
''')

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
            "cybexdump=cybexdump_launcher:cli",
        ],
    },
    python_requires=">=3.7",
)
