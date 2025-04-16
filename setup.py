from setuptools import setup

setup(
    name="qmt-mcp-server",
    version="0.1.0",
    description="QMT MCP Server for financial data access",
    author="jm12138",
    package=["qmt_mcp_server"],
    install_requires=[
        "pandas",
        "xtquant",
        "mcp",
    ],
    entry_points={
        'console_scripts': [
            'qmt-mcp-server=qmt_mcp_server:run',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
