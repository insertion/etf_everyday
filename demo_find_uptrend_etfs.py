#!/usr/bin/env python3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_mock_data(ticker, period="6mo"):
    """生成模拟的ETF历史数据"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    prices = []
    
    # 为不同ticker生成不同的价格模式
    if ticker in ['SPY', 'QQQ', 'VOO']:
        # 上升趋势
        base_price = {'SPY': 500, 'QQQ': 450, 'VOO': 490}[ticker]
        for i in range(len(dates)):
            trend = i * 0.5  # 上升趋势
            noise = np.random.normal(0, 5)
            prices.append(base_price + trend + noise)
    elif ticker in ['XLE', 'GLD', 'SLV']:
        # 下降趋势
        base_price = {'XLE': 80, 'GLD': 200, 'SLV': 25}[ticker]
        for i in range(len(dates)):
            trend = -i * 0.2  # 下降趋势
            noise = np.random.normal(0, 2)
            prices.append(base_price + trend + noise)
    else:
        # 震荡
        base_price = 100
        for i in range(len(dates)):
            noise = np.random.normal(0, 3)
            prices.append(base_price + noise)
    
    data = pd.DataFrame({
        'Date': dates,
        'Open': prices,
        'High': [p * 1.02 for p in prices],
        'Low': [p * 0.98 for p in prices],
        'Close': prices,
        'Volume': np.random.randint(1000000, 5000000, len(dates))
    })
    data.set_index('Date', inplace=True)
    return data


def is_uptrend(ticker, period="6mo", short_ma=20, long_ma=50, use_mock=True):
    """
    判断ETF是否处于上升趋势
    使用移动平均线交叉策略：短期MA > 长期MA 且价格高于两条MA
    """
    try:
        if use_mock:
            hist = generate_mock_data(ticker, period)
        else:
            import yfinance as yf
            etf = yf.Ticker(ticker)
            hist = etf.history(period=period)
        
        if len(hist) < long_ma:
            return False, None, None
        
        hist['Short_MA'] = hist['Close'].rolling(window=short_ma).mean()
        hist['Long_MA'] = hist['Close'].rolling(window=long_ma).mean()
        
        last = hist.iloc[-1]
        prev = hist.iloc[-2]
        
        current_price = last['Close']
        short_ma_val = last['Short_MA']
        long_ma_val = last['Long_MA']
        
        uptrend_condition = (
            short_ma_val > long_ma_val and
            current_price > short_ma_val and
            current_price > long_ma_val and
            last['Short_MA'] > prev['Short_MA']
        )
        
        return uptrend_condition, current_price, hist
        
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return False, None, None


def main():
    etf_list = [
        'SPY', 'QQQ', 'DIA', 'IWM', 'VTI',
        'XLF', 'XLE', 'XLV', 'XLY', 'XLP',
        'XLK', 'XLC', 'XLI', 'XLB', 'XLU',
        'VOO', 'IVV', 'VUG', 'VTV', 'IJR',
        'EFA', 'EEM', 'VGK', 'VPL', 'EWJ',
        'TLT', 'IEF', 'SHY', 'BND', 'AGG',
        'GLD', 'SLV', 'USO', 'UNG', 'DBC'
    ]
    
    print("="*60)
    print("ETF上升趋势检测器 (演示版 - 使用模拟数据)")
    print(f"检查周期: 6个月 | 短期MA: 20天 | 长期MA: 50天")
    print("="*60)
    print()
    
    uptrend_etfs = []
    
    for ticker in etf_list:
        print(f"检查 {ticker}...", end=" ", flush=True)
        is_up, price, hist = is_uptrend(ticker, use_mock=True)
        
        if is_up:
            print("✓ 上升趋势")
            uptrend_etfs.append({
                'Ticker': ticker,
                'Current Price': round(price, 2),
                'Short MA (20)': round(hist.iloc[-1]['Short_MA'], 2),
                'Long MA (50)': round(hist.iloc[-1]['Long_MA'], 2)
            })
        else:
            print("✗ 非上升趋势")
    
    print()
    print("="*60)
    print(f"找到 {len(uptrend_etfs)} 个处于上升趋势的ETF:")
    print("="*60)
    
    if uptrend_etfs:
        df = pd.DataFrame(uptrend_etfs)
        print(df.to_string(index=False))
    else:
        print("没有找到符合条件的ETF")
    
    print()
    print("="*60)
    print("\n说明:")
    print("- 此为演示版本，使用模拟数据")
    print("- SPY、QQQ、VOO被设置为上升趋势示例")
    print("- XLE、GLD、SLV被设置为下降趋势示例")
    print("- 其他ETF为震荡模式")
    print("="*60)


if __name__ == "__main__":
    main()
