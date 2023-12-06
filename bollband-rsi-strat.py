rsi_series = rsi(close_prices, length=RSI_LENGTH)

# Calculate Bollinger Bands with a 20-day SMA and 2 standard deviations using pandas_ta
# See documentation here https://tradingstrategy.ai/docs/programming/api/technical-analysis/volatility/help/pandas_ta.volatility.bbands.html#bbands
bollinger_bands = bbands(close_prices, length=MOVING_AVERAGE_LENGTH, std=STDDEV)

# bbands() returns a dictionary of items with different name mangling
bb_upper = bollinger_bands[f"BBU_{MOVING_AVERAGE_LENGTH}_{STDDEV}"]
bb_lower = bollinger_bands[f"BBL_{MOVING_AVERAGE_LENGTH}_{STDDEV}"]
bb_mid = bollinger_bands[f"BBM_{MOVING_AVERAGE_LENGTH}_{STDDEV}"]  # Moving average

if not position_manager.is_any_open():
    # No open positions, decide if BUY in this cycle.
    # We buy if the price on the daily chart closes above the upper Bollinger Band.
    if price_latest > bb_upper.iloc[-1] and rsi_series[-1] >= RSI_THRESHOLD:
        buy_amount = cash * POSITION_SIZE
        trades += position_manager.open_1x_long(
            pair, buy_amount, stop_loss_pct=STOP_LOSS_PCT
        )

else:
    # We have an open position, decide if SELL in this cycle.
    # We close the position when the price closes below the 20-day moving average.
    if price_latest < bb_mid.iloc[-1]:
        trades += position_manager.close_all()
