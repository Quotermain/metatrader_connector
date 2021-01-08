import pickle

with open('data/thresholds/open_close_day_dif.pickle', 'rb') as file:
    dict_open_close_day_dif = pickle.load(file)
with open('data/thresholds/open_close_5min_dif.pickle', 'rb') as file:
    dict_open_close_5min_dif = pickle.load(file)

def check_trade_conditions(ticker, df_day, df_5min):

    condition_short = (
        (df_day.close[-1] - df_day.open[-1]) > 0 and
        (df_5min.close[-2] - df_5min.open[-2]) > 0 and
        (
            (df_day.close[-1] - df_day.open[-1]) / df_day.open[-1] >
            dict_open_close_day_dif[ticker]
        ) and
        (
            (df_5min.close[-2] - df_5min.open[-2]) / df_5min.open[-2] >
            dict_open_close_5min_dif[ticker]
        ) and
        (
            (df_5min.close[-1] - df_5min.open[-1]) /   df_5min.open[-1] <
            dict_open_close_5min_dif[ticker]
        )
    )

    condition_long = (
        (df_day.close[-1] - df_day.open[-1]) < 0 and
        (df_5min.close[-2] - df_5min.open[-2]) < 0 and
        (
            (df_day.open[-1] - df_day.close[-1]) / df_day.close[-1] >
            dict_open_close_day_dif[ticker]
        ) and
        (
            (df_5min.open[-2] - df_5min.close[-2]) / df_5min.close[-2] >
            dict_open_close_5min_dif[ticker]
        ) and
        (
            (df_5min.open[-1] - df_5min.close[-1]) / df_5min.close[-1] <
            dict_open_close_5min_dif[ticker]
        )
    )

    if condition_short:
        return 'short'
    elif condition_long:
        return 'long'
    else:
        return None

if __name__ == '__main__':
    pass
