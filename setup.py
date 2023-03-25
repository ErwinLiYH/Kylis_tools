import setuptools
from pip._internal.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)
reqs = [str(ir.requirement) for ir in install_reqs]
print(install_reqs)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Ktools",
    version="0.0.1",
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
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=reqs
)