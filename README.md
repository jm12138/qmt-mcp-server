# QMT MCP Server

## 项目简介

- 基于 QMT 平台的 MCP (Model Communication Protocol) 服务器，用于提供股票市场数据查询和处理功能。

## 功能特性

- 获取股票详细信息
- 下载股票历史数据
- 查询股票市场数据

## 工具函数

- `get_current_time_tool`: 获取当前时间
- `get_instrument_detail_tool`: 获取股票的详细信息
- `download_history_data_tool`: 下载特定股票的历史市场数据
- `get_market_data_ex_tool`: 获取多只股票的市场数据

## 快速开始

1. 安装 QMT-MCP-Server

    ```bash
    $ pip install git+https://github.com/jm12138/qmt-mcp-server
    ```

2. 启动 QMT 或 MiniQMT 客户端


3. 编辑客户端配置文件

    ```json
    {
        "servers": {
            "qmt-mcp-server": {
                "type": "stdio",
                "command": "qmt-mcp-server"
            }
        }
    }
    ```

4. 启动客户端使用