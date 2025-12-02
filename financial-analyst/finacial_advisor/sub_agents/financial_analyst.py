import yfinance as yf
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm(model="openai/gpt-4o")

# 문자열 보다 구조체로 
def get_compay_info(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker" : ticker,
        "success" : True,
        "compay_name" : info.get("longName", "NA"),
        "industry" : info.get("industry", "NA"),
        "sector" : info.get("sector", "NA"),
    }

def get_income_statement(ticker: str):
    stock = yf.Ticker(ticker)
    #return stock.income_stmt.to_json()
    return {
        "ticker" : ticker,
        "success" : True,
        "income_statement" : stock.income_stmt.to_json(),
    }

def get_balance_sheet(ticker: str):
    stock = yf.Ticker(ticker)
    #return stock.balance_sheet.to_json()
    return {
        "ticker" : ticker,
        "success" : True,
        "balance_sheet" : stock.balance_sheet.to_json(),
    }


def get_cash_flow(ticker: str):
    stock = yf.Ticker(ticker)
    return {
        "ticker" : ticker,
        "success" : True,
        "cash_flow" : stock.cash_flow.to_json(),
    }

def get_stock_price(ticker: str, period: str):
    """
    Args:
        ticker: str
            Symbol of the company(i.e AAPL) 
        period: str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Default: 1mo
    Returns:
        

    """
    stock = yf.Ticker(ticker)
    history = stock.history(period=preiod)
    info = stock.info
    return {
        "ticker" : ticker,
        "success" : True,
        "stock_price" : history.to_json(),
        "cuurent_price": info.get("currentPrice")
    }

def get_financial_metrics(ticker: str):
    stock = yf.Ticker(ticker)
    info = stock.info
    return {
        "ticker" : ticker,
        "success" : True,
        "financial_metrics" : info.get("marketCap", "NA"),
        "pe_ratio" : info.get("trailingPE", "NA"),
        "dividend_yield" : info.get("dividendYield", "NA"), # 배당 수익률
        "beta": info.get("beta", "NA"), #
    }



financial_analyst = Agent(
    name="FinancialAnalyst",
    model=MODEL,
    description="Analyzes detailed financial statements including income, balance sheet, and cash flow",
    instruction="""
    You are a Financial Analyst who performs deep financial statement analysis. Your job:
    
    1. **Income Analysis**: Use get_income_statement() to analyze revenue, profitability, and margins
    2. **Balance Sheet Analysis**: Use get_balance_sheet() to examine assets, liabilities, and financial position
    3. **Cash Flow Analysis**: Use get_cash_flow() to assess cash generation and capital allocation
    
    **Your Financial Tools:**
    - **get_income_statement(ticker)**: Revenue, profit margins, and profitability analysis
    - **get_balance_sheet(ticker)**: Assets, debt, equity, and financial strength ratios
    - **get_cash_flow(ticker)**: Operating cash flow, free cash flow, and capital expenditure
    
    Analyze the financial health and performance of companies using comprehensive financial statement data.
    Focus on key financial ratios, trends, and indicators that reveal the company's financial strength.
    """,
    tools=[
        get_income_statement,
        get_balance_sheet,
        get_cash_flow,
    ],
)
