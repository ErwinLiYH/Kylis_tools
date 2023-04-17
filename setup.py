import setuptools
from pip._internal.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.requirement) for ir in install_reqs]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Ktools",
    version="0.3.0",
    author="Erwin Li",
    author_email="erwinli@qq.com",
    description="some personnal tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/erwinliyh/Kylis_tools",
    project_urls={
        "Bug Tracker": "https://github.com/erwinliyh/Kylis_tools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'passwdhd=Ktools.passwd_holder:main',
            'scphp=Ktools.scp_batch:main',
            'csvex=Ktools.csv_extractor:main',
            'csvan=Ktools.csv_analysor:main'
        ],
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=reqs
)