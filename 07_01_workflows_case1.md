---
layout: default
title:  Scenario 1 - Trading Workflow
parent: Workflows 
nav_order: 26
---

# Creating a Trading Workflow in KAWA

This scenario shows how to build an automated trading pipeline (Workflow) in KAWA.

The pipeline runs on a schedule and, step by step, does the following: loads and prepares market data, runs a Python script to calculate signals, and sends notifications and a short report.

## 1. Create a workflow

- Go to Home → Workflows and click **+ Workflow**.
- Enter a name, e.g., **Daily — Signals & Report**.

> Recommendation: create separate workflows for different frequencies (Daily / Intraday) and markets.

## 2. Trigger

- In the WHEN area, choose At a scheduled time.
- Frequency: Daily
- Time: 06:10 (after market close).
- Time zone: the exchange’s time zone (e.g., America/New_York).
- Only on business days: On.

## 3. Action steps

### 3.1 Step 1 — Transform data: prepare market data

#### 3.1.1 Go to Add action 

→ Transform data and choose the OHLCV source.

#### 3.1.2 Time 

Use a single time column for all records. Ensure the timestamp is UTC ISO-8601 (e.g., 2025-10-17T20:00:00Z).

#### 3.1.3 Order matters

Sort by timestamp (New -> Old) so EMA/RSI are calculated correctly.

#### 3.1.4 Adding simple metrics (Enrich → Formula)

- Body ratio — share of the candle body in the day’s range
Name: `body_ratio`
Formula:
`ROUND( ABS(close - open) / ( ABS(high - low) + 1 / POWER(10, 7) ), 4 )`

Meaning (0…1):

  - 0 ≈ neutral/doji (open ≈ close)
  - 1 ≈ strong one-direction day (big body, small wicks)

- Range % — relative daily volatility
Name: `range_pct`
Formula:

`ROUND( (high - low) / ( (high + low + close) / 3 + 1 / POWER(10, 7) ), 6 )`

Meaning: Higher = a more volatile day. Good for comparing different tickers.

- Close position in range — where the close sits within the day’s range
Name: `close_pos_in_range`
Formula:

`ROUND( (close - low) / ( ABS(high - low) + 1 / POWER(10, 7) ), 4 )`

Meaning (0…1):

- 0 = closed near low
- 0.5 = around the middle
- 1 = closed near high

#### 3.1.5 Enrich → Lookup column

Goal: pull the exchange and currency for each ticker.

- Source sheet: ref_symbols
- Columns to pull: exchange, currency

Result: the source table gets new columns exchange and currency (e.g., NASDAQ, USD) for each symbol.

#### 3.1.6 Enrich → Manual input

Goal: add simple constants for easier filtering and report/email subjects.

- Add: **session**
- 
Value: "**EOD**"

Why: marks the daily run; used in the AI report and filters.

- Add: **market**
- 
Value: "**US**"

Why: market tag; inserted into email subject and used for grouping.

#### 3.1.7 Data quality checks 

- OHLC rules: high ≥ max(open, close), low ≤ min(open, close), high ≥ low.
- Volume: volume ≥ 0; optionally flag volume = 0.
- Uniqueness: no duplicate symbol + timestamp.
- Types: price/volume columns are numeric; no stray text.

#### 3.1.8 Row guardrails (Behavior)

For our scenario set exactly these parameters:

- If no rows are found → Interrupt the workflow.
- If more than [Max num of rows] are found → Interrupt the workflow.

> The 1,000 threshold in this field is fixed (not editable).

- Max num of rows → set a value greater than the current number of rows in the table.

  - Example: if the source has ~800 rows, set 1000.
  - If you add new tickers/history, increase this value accordingly.
  - If Max num of rows ≤ the table size, the workflow will not start.

### 3.2 Step 2 — Run python script

**Goal**: generate signals from Step 1 data (OHLCV) using the Python tool compute_indicators_and_signals.

1. Choose the tool

- Open Add action → Run python script.
- In Select python tool from the library, choose **compute_indicators_and_signals**.

```python
import logging
import numpy as np
import pandas as pd

from kywy.client.kawa_decorators import kawa_tool  # for local installs use: from kawa.client.kawa_decorators import kawa_tool

logger = logging.getLogger('script-logger')


def _ema(s: pd.Series, span: int) -> pd.Series:
    return pd.Series(s, dtype="float64").ewm(span=span, adjust=False).mean()

def _rsi(close: pd.Series, period: int = 14) -> pd.Series:
    c = pd.Series(close, dtype="float64")
    d = c.diff()
    up = d.clip(lower=0.0)
    dn = (-d.clip(upper=0.0))
    au = up.ewm(alpha=1/period, adjust=False).mean()
    ad = dn.ewm(alpha=1/period, adjust=False).mean()
    rs = au / ad.replace(0.0, np.nan)
    return 100 - (100 / (1 + rs))

def _atr(h: pd.Series, l: pd.Series, c: pd.Series, period: int = 14) -> pd.Series:
    h = pd.Series(h, dtype="float64"); l = pd.Series(l, dtype="float64"); c = pd.Series(c, dtype="float64")
    pc = c.shift(1)
    tr = pd.concat([(h - l).abs(), (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1/period, adjust=False).mean()


@kawa_tool(
    inputs={'symbol': str},              # UI will show a "symbol" input to map a column from Step 1
    outputs={'signal': str},             # metadata only; we return the full DataFrame
)
def compute_indicators_and_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expects from Step 1 columns: timestamp, symbol, open, high, low, close, volume.
    Returns one row per symbol with signal and basic indicators evaluated on the last bar.
    """
    logger.info('Starting compute_indicators_and_signals')
    if df is None or df.empty:
        return pd.DataFrame(columns=[
            "timestamp","symbol","signal","confidence","entry","sl","tp1","tp2",
            "ema_20","ema_50","rsi_14","atr_14","ema_cross"
        ])

    # Normalize types
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
    for col in ("open","high","low","close","volume"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['timestamp','symbol','close']).sort_values(['symbol','timestamp'])

    # Compute indicators across full history
    df['ema_20'] = df.groupby('symbol', group_keys=False)['close'].apply(lambda s: _ema(s, 20))
    df['ema_50'] = df.groupby('symbol', group_keys=False)['close'].apply(lambda s: _ema(s, 50))
    df['rsi_14'] = df.groupby('symbol', group_keys=False)['close'].apply(lambda s: _rsi(s, 14))
    df['atr_14'] = df.groupby('symbol', group_keys=False).apply(
        lambda g: _atr(g['high'], g['low'], g['close'], 14)
    ).reset_index(level=0, drop=True)

    # Take the last bar per ticker and generate a signal
    last_rows = df.groupby('symbol', as_index=False, group_keys=False).tail(1).copy()

    def decide(row):
        fast, slow, rsi = row['ema_20'], row['ema_50'], row['rsi_14']
        if pd.notna(fast) and pd.notna(slow):
            if fast > slow and (pd.isna(rsi) or rsi < 70):   # RSI filter
                return "BUY", 0.7
            if fast < slow and (pd.isna(rsi) or rsi > 30):
                return "SELL", 0.7
        return "HOLD", 0.0

    sig_conf = last_rows.apply(lambda r: pd.Series(decide(r), index=['signal','confidence']), axis=1)
    last_rows[['signal','confidence']] = sig_conf

    # Levels using a simple ATR multiplier
    def levels(row):
        entry = float(row['close'])
        atr = float(row['atr_14']) if pd.notna(row['atr_14']) else entry * 0.01
        if row['signal'] == 'BUY':
            return entry - 1.0*atr, entry + 1.0*atr, entry + 2.0*atr
        if row['signal'] == 'SELL':
            return entry + 1.0*atr, entry - 1.0*atr, entry - 2.0*atr
        return None, None, None

    last_rows[['sl','tp1','tp2']] = last_rows.apply(lambda r: pd.Series(levels(r), index=['sl','tp1','tp2']), axis=1)
    last_rows['entry'] = last_rows['close']
    last_rows['ema_cross'] = last_rows['ema_20'] - last_rows['ema_50']

    out_cols = ["timestamp","symbol","signal","confidence","entry","sl","tp1","tp2",
                "ema_20","ema_50","rsi_14","atr_14","ema_cross"]
    return last_rows.reindex(columns=out_cols).sort_values('symbol').reset_index(drop=True)
```

2. Connect inputs

- Map the tool inputs to the outputs from Step 1 (Match tool inputs).

3. Behavior (guardrails) — use the same limits as in Step 1:

- If no rows are found → Interrupt workflow.
- If more than N rows are found → Interrupt workflow.
- Max number of rows → 12 (for our example: 3 tickers × 1 latest bar × small buffer).

>These limits protect you from an empty source or a row “explosion” due to duplicates/errors.

### 3.3 Step 3 — AI prompt

Goal: generate a short EOD report in Markdown based on the latest snapshot from Step 2.

1. Add the action → AI prompt

2. Insert the prompt

Copy the text below into the Prompt field.

```
You are a pragmatic trading assistant. Produce a concise end-of-day (EOD) report in Markdown.

## Context
- Run date (UTC): {{1 - timestamp}}
- Market: {{1 - market}}
- Session: {{1 - session}}

## Instructions
Use the table **signals_eod** (inserted below) where each row is the latest bar per symbol with columns:
timestamp, symbol, signal, confidence, entry, sl, tp1, tp2, ema_20, ema_50, rsi_14, atr_14, ema_cross.

Create:

1) **Summary (≤120 words).** Count BUY/SELL/HOLD from the table; mention any outliers (very high RSI or ATR). Keep neutral tone.

2) **Signals table.** Render a compact Markdown table with columns:  
Symbol | Signal | Conf | Entry | SL | TP1 | TP2 | RSI | ATR  
- Sort: BUY first (by Conf desc), then SELL, then HOLD.  
- Round prices to 2–4 decimals where appropriate.

3) **Notes.** Mention if any values are missing (e.g., ATR not available) and any simple risk caveats.

## Signals
{{signals_eod}}
```

3. Connect the data

- In the prompt toolbar, click + → Use data from.
For the context variables, insert:
Use data from → 1. Transform data → Aggregated values → timestamp, market, and session.

- For the signals table, scroll the prompt to the ## Signals section, click + → Use data from → 2. Run python script → Grid, and insert the grid from Step 2.