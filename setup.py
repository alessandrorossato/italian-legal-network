from setuptools import setup, find_packages

setup(
    name='Test',  # Replace with your package name
    version='0.1.0',  # Replace with your package version
    packages=find_packages(),  # Automatically discover and include all packages
    install_requires=[
        'beautifulsoup4==4.12.2',
        'numpy==1.25.0',
        'pandas==2.0.3',
        'requests==2.31.0',
        'scipy==1.11.2',
    ],
    entry_points={
        'console_scripts': [
            'your_script_name=your_package_name.module_name:main',  # Replace with your script and module names
        ],
    },
    # Other metadata goes here, such as author, description, license, etc.
    author='alessandrorossato',
    author_email='your.email@example.com',
    description='Italian legal network analysis',
    url='https://github.com/alessandrorossato/Italian-Legal-Network',
)