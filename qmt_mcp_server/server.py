from asyncio import to_thread
from time import strftime, localtime
from typing import TypedDict, List, Dict

from xtquant.xtdata import (
    get_instrument_detail,
    download_history_data,
    get_market_data_ex
)
from pandas import DataFrame
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("qmt-mcp-server", dependencies=["pandas", "xtquant"])


class InstrumentDetail(TypedDict):
    """
    Instrument detail

    Attributes:
        ExchangeID (str): Market code of the instrument.
        InstrumentID (str): Instrument code.
        InstrumentName (str): Instrument name.
        ProductID (str): Product ID of the instrument (for futures).
        ProductName (str): Product name of the instrument (for futures).
        ProductType (str): Type of the instrument.
        ExchangeCode (str): Exchange code.
        UniCode (str): Unified rule code.
        CreateDate (str): Listing date (for futures).
        OpenDate (str): IPO date (for stocks).
        ExpireDate (str): Delisting or expiration date.
        PreClose (float): Previous closing price.
        SettlementPrice (float): Previous settlement price.
        UpStopPrice (float): Daily upper limit price.
        DownStopPrice (float): Daily lower limit price.
        FloatVolume (float): Floating share capital.
        TotalVolume (float): Total share capital.
        LongMarginRatio (float): Long margin ratio.
        ShortMarginRatio (float): Short margin ratio.
        PriceTick (float): Minimum price change unit.
        VolumeMultiple (int): Contract multiplier (default is 1 for non-futures).
        MainContract (int): Main contract flag.
        LastVolume (int): Previous day's open interest.
        InstrumentStatus (int): Instrument suspension status.
        IsTrading (bool): Whether the instrument is tradable.
        IsRecent (bool): Whether it is a near-month contract.
    """
    Exception: str
    ExchangeID: str
    InstrumentID: str
    InstrumentName: str
    ProductID: str
    ProductName: str
    ProductType: str
    ExchangeCode: str
    UniCode: str
    CreateDate: str
    OpenDate: str
    ExpireDate: str
    PreClose: float
    SettlementPrice: float
    UpStopPrice: float
    DownStopPrice: float
    FloatVolume: float
    TotalVolume: float
    LongMarginRatio: float
    ShortMarginRatio: float
    PriceTick: float
    VolumeMultiple: int
    MainContract: int
    LastVolume: int
    InstrumentStatus: int
    IsTrading: bool
    IsRecent: bool


@mcp.tool()
async def get_instrument_detail_tool(stock_code: str) -> str:
    """
    Retrieve detailed information about a financial instrument.

    Args:
        stock_code (str): The stock code of the instrument. 
                          Example: '000001.SZ' for Shenzhen or '000001.SH' for Shanghai.

    Returns:
        str: A string representation of the instrument's details if successful.
            If an error occurs, returns an error message describing the issue.
    """
    try:
        instrument_detail: InstrumentDetail = await to_thread(
            get_instrument_detail,
            stock_code=stock_code
        )
        return str(instrument_detail)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def download_history_data_tool(
        stock_code: str,
        period: str = '1d',
        start_time: str = '',
        end_time: str = '',
        incrementally: bool = True) -> str:
    """
    Download historical market data for a specific stock.

    Args:
        stock_code (str): The stock code of the instrument. 
                            Example: '000001.SZ' for Shenzhen or '000001.SH' for Shanghai.
        period (str, optional): The time interval for the historical data. 
                                Supported values:
                                - "tick": Tick interval
                                - "1m": 1-minute interval
                                - "5m": 5-minute interval
                                - "15m": 15-minute interval
                                - "30m": 30-minute interval
                                - "1h": 1-hour interval
                                - "1d": Daily interval (default)
                                - "1w": Weekly interval
                                - "1mon": Monthly interval
                                - "1q": Quarterly interval
                                - "1hy": Semi-annual interval
                                - "1y": Annual interval.
        start_time (str, optional): The start date/time for the historical data in 'yyyyMMdd' or 'yyyyMMddHHmmss' format. 
                                    Leave empty to fetch data from the earliest available date. Default is ''.
        end_time (str, optional): The end date/time for the historical data in 'yyyyMMdd' or 'yyyyMMddHHmmss' format. 
                                    Leave empty to fetch data up to the latest available date. Default is ''.
        incrementally (bool, optional): If True, only download data that has changed since the last download.
                                        If False, download all available data. Default is True.

    Returns:
        str: A success message if the data is downloaded successfully.
            If an error occurs, returns an error message describing the issue.
    """
    try:
        await to_thread(
            download_history_data,
            stock_code=stock_code,
            period=period,
            start_time=start_time,
            end_time=end_time,
            incrementally=incrementally
        )
        return f"Historical data for {stock_code} downloaded successfully. Please use get_market_data_ex function to get the market data."
    except Exception as e:
        return f"Error: {str(e)}"


def convert_market_data(market_data: Dict[str, DataFrame]) -> Dict[str, List[Dict]]:
    for stock_code in market_data.keys():
        market_data[stock_code].index.name = 'date'
        market_data[stock_code] = market_data[stock_code].reset_index().to_dict(
            orient='records', index=True)
    return market_data


@mcp.tool()
async def get_market_data_ex_tool(
    stock_list: List[str] = [],
    field_list: List[str] = [],
    period: str = '1d',
    start_time: str = '',
    end_time: str = '',
    count: int = -1,
    dividend_type: str = 'none',
    fill_data: bool = True
) -> str:
    """
    Retrieve market data for a list of stocks. Please make sure you have downloaded the data using download_history_data function.

    Args:
        stock_list (List[str]): A list of stock codes to retrieve data for. 
                                Example: ['000001.SZ', '000002.SZ'].
        field_list (List[str], optional): A list of fields to retrieve. Default is an empty list (all fields).
                                          Example: ['open', 'close', 'high', 'low', 'volume'].
                                          Supported fields include:
                                              - 'time': Time (int)
                                              - 'open': Opening price (float)
                                              - 'high': Highest price (float)
                                              - 'low': Lowest price (float)
                                              - 'close': Closing price (float)
                                              - 'volume': Trading volume (float)
                                              - 'amount': Trading amount (float)
                                              - 'settle': Settlement price (float)
                                              - 'openInterest': Open interest (float)
                                              - 'preClose': Previous closing price (float)
                                              - 'suspendFlag': Suspension flag (1 for suspended, 0 otherwise)
                                          For tick data, additional fields are supported:
                                              - 'lastPrice': Latest price (float)
                                              - 'lastClose': Previous closing price (float)
                                              - 'stockStatus': Suspension flag (1 for suspended, 0 otherwise)
        period (str, optional): The time interval for the market data. Default is '1d'.
                                Supported values:
                                    - "tick": Tick interval
                                    - "1m": 1-minute interval
                                    - "5m": 5-minute interval
                                    - "15m": 15-minute interval
                                    - "30m": 30-minute interval
                                    - "1h": 1-hour interval
                                    - "1d": Daily interval
                                    - "1w": Weekly interval
                                    - "1mon": Monthly interval
                                    - "1q": Quarterly interval
                                    - "1hy": Semi-annual interval
                                    - "1y": Annual interval
        start_time (str, optional): The start date/time for the market data in 'yyyyMMdd' or 'yyyyMMddHHmmss' format. 
                                    Leave empty to fetch data from the earliest available date. Default is ''.
        end_time (str, optional): The end date/time for the market data in 'yyyyMMdd' or 'yyyyMMddHHmmss' format. 
                                  Leave empty to fetch data up to the latest available date. Default is ''.
        count (int, optional): The number of records to retrieve. Default is -1 (all records).
        dividend_type (str, optional): The dividend adjustment type to include in the data. Default is 'none'.
                                       Supported values:
                                           - 'none': No dividend adjustment
                                           - 'front': Forward-adjusted
                                           - 'back': Backward-adjusted
                                           - 'front_ratio': Proportional forward-adjusted
                                           - 'back_ratio': Proportional backward-adjusted
        fill_data (bool, optional): Whether to fill missing data points. Default is True.

    Returns:
        str: A string representation of the market data for the requested stocks.
             If successful, returns the data as a dictionary where each stock code maps to a list of records.
             If an error occurs, returns an error message describing the issue.
    """
    try:
        market_data: Dict[str, DataFrame] = await to_thread(
            get_market_data_ex,
            field_list=field_list,
            stock_list=stock_list,
            period=period,
            start_time=start_time,
            end_time=end_time,
            count=count,
            dividend_type=dividend_type,
            fill_data=fill_data
        )
        market_data: Dict[str, List[Dict]] = await to_thread(convert_market_data, market_data=market_data)
        return str(market_data)
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def get_current_time_tool() -> str:
    """
    Get the current time in 'yyyyMMddHHmmss' format.

    Returns:
        str: The current time in 'yyyyMMddHHmmss' format.
             If an error occurs, returns an error message describing the issue.
    """
    try:
        return await to_thread(
            strftime,
            "%Y%m%d%H%M%S",
            localtime()
        )
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
