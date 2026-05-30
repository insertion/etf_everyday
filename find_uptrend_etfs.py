#!/usr/bin/env python3
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time


def is_uptrend(ticker, period="6mo", short_ma=20, long_ma=50, max_retries=3):
    """
    判断ETF是否处于上升趋势
    使用移动平均线交叉策略：短期MA > 长期MA 且价格高于两条MA
    """
    retry_count = 0
    while retry_count < max_retries:
        try:
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
            retry_count += 1
            if retry_count < max_retries:
                wait_time = 2 ** retry_count  # 指数退避
                print(f"重试 {ticker} ({retry_count}/{max_retries})，等待 {wait_time} 秒...")
                time.sleep(wait_time)
            else:
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
    print("正在检查处于上升趋势的ETF...")
    print(f"检查周期: 6个月 | 短期MA: 20天 | 长期MA: 50天")
    print("="*60)
    print()
    
    uptrend_etfs = []
    
    for ticker in etf_list:
        print(f"检查 {ticker}...", end=" ", flush=True)
        is_up, price, hist = is_uptrend(ticker)
        
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
        
        time.sleep(1)
    
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


if __name__ == "__main__":
    main()
