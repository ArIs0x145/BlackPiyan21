from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="blackpiyan",
    version="0.1.0",
    author="BlackPiyan Team",
    author_email="aris0x145@gmail.com",
    description="模擬21點遊戲中莊家補牌策略的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CornHub114514/BlackPiyan",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "blackpiyan=blackpiyan.__main__:main",
        ],
    },
) 