import setuptools


setuptools.setup(
    name="discriminator",
    version="0.0.1",
    author="Harsh Soni",
    author_email="author@example.com",
    description="Metric to evaluate data quality for synthetic data.",
    url="https://github.com/harsh020/real_synthetic_discriminator",
    project_urls={
        "Bug Tracker": "https://github.com/harsh020/real_synthetic_discriminator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "discriminator"},
    packages=setuptools.find_packages(where="discriminator"),
    python_requires=">=3.6",
    install_requires = [
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy'
    ]
)
