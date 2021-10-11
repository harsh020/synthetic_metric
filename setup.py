import setuptools


setuptools.setup(
    name="synmetric",
    version="0.0.1",
    author="Harsh Soni",
    author_email="author@example.com",
    description="Metric to evaluate data quality for synthetic data.",
    url="https://github.com/harsh020/synthetic_metric",
    project_urls={
        "Bug Tracker": "https://github.com/harsh020/synthetic_metric/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "synmetric"},
    packages=setuptools.find_packages(where="synmetric"),
    python_requires=">=3.6",
    install_requires = [
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy'
    ]
)
