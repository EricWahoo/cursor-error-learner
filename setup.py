from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cursor-error-learner",
    version="1.0.0",
    author="Eric Wahoo",
    author_email="",
    description="Automatic error tracking and learning for Python code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EricWahoo/cursor-error-learner",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Debugging",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.9",
    install_requires=[
        "ast",
        "typing-extensions>=4.0.0",
        "pathlib",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "error-learner=error_learner.cli:main",
        ],
        "cursor.extensions": [
            "error-learner = error_learner.extension:tracker",
        ],
    },
)