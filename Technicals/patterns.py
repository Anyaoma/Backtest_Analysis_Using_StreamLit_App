import sys
sys.path.append("../")
import pandas as pd


ENGULFING_FACTOR = 1.1

def candle_properties(df): #the candle properties depend on the candle patterns i would like to follow
    body = abs(df.mid_c - df.mid_o)
    df['body'] = body
    df['body_prev'] = df['body'].shift(1)
    direction = df.mid_c - df.mid_o #this is to determine the colour of the candle
    df['direction'] = [1 if x>=0 else -1 for x in direction]
    df['direction_prev'] = df['direction'].shift(1)


def engulfing(row):
    if row.direction != row.direction_prev: #this is to determine a difference in candle colour from the previous candle
        if row.body >= row.body_prev * ENGULFING_FACTOR:
            return True
        return False
    return False

def apply_properties_patterns(df):
    candle_properties(df)
    df['ENGULFING'] = df.apply(engulfing, axis=1)
    return df