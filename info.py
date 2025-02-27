import pandas as pd
import requests
import FinanceDataReader as fdr

def get_stock_code(stock_name):
    stocks = fdr.StockListing('KRX')
    stock_dict = dict(zip(stocks['Name'], stocks['Code']))
    return stock_dict.get(stock_name, None)

# 사용자로부터 종목명 입력받기
stock_name = input("종목명을 입력하세요: ")
code = get_stock_code(stock_name)

if code:
    URL = f"https://finance.naver.com/item/main.nhn?code={code}"
    r = requests.get(URL)

    df = pd.read_html(r.text)[3]
    df.set_index(df.columns[0], inplace=True)
    df.index.rename('주요재무정보', inplace=True)
    df.columns = df.columns.droplevel(2)

    annual_data = pd.DataFrame(df).xs('최근 연간 실적', axis=1)
    quater_data = pd.DataFrame(df).xs('최근 분기 실적', axis=1)

    print(quater_data)
else:
    print("종목명을 찾을 수 없습니다.")
