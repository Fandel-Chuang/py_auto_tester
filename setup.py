from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="py_auto_tester",
    version="0.2.0",
    author="Fandaw",
    author_email="542483297@qq.com",
    description="A Python package that provides automatic testing functionality based on docstrings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Fandaw/py_auto_tester",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Unit",
    ],
    python_requires='>=3.6',
    install_requires=[
        # 列出你的包的依赖项
    ],
)