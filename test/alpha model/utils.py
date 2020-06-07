import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import io
import base64
import click
import datetime


def plot_series(df, code, method='mv', cum_on=False, threshold=None, figsize=None, is_saving=False, is_base64=False, is_showing=True):

    if isinstance(code, str):
        code = [code]

    def _plot_series(df, code):

        def format_date(x, pos=None):
            thisind = np.clip(int(x+0.5), 0, N-1)
            return df.index[thisind].strftime('%m/%d')

        N = df.shape[0]
        for i in df.columns:
            try:
                if not(cum_on):
                    df.reset_index()[i].plot()
                else:
                    df.reset_index()[i].cumprod().plot()
            except:
                pass
        if threshold is not None:
            ax.axhline(threshold, linestyle='--', color='blue')
            ax.axhline(-1 * threshold, linestyle='--', color='blue')
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        # plt.legend([f'{code} -- {j}' for j in df.columns])
        # plt.title(code)

    if figsize is None:
        fig = plt.figure(figsize=(12, 8))
    else:
        fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1)
    
    if not(is_showing):
        matplotlib.use('Agg')

    if (df.index.name is not None):
        for c in code:
            if 'code' in df.columns:
                _plot_series(df.drop('code', axis=1), c)
            else:
                _plot_series(df, c)
        plt.legend([f'{c} : {col}' for c in code for col in df.columns])

    elif (df.index.names is not None) and (len(df.index.names) > 1):
        for c in code:
            if 'date' in df.index.names:
                _plot_series(df.loc[(slice(None), c), :].reset_index().set_index('date').drop('code', axis=1), c)
            elif 'datetime' in df.index.names:
                _plot_series(df.loc[(slice(None), c), :].reset_index().set_index('datetime').drop('code', axis=1), c)
        plt.legend([f'{c} : {col}' for c in code for col in df.columns])

    
    # N = df.shape[0]
    # for i in df.columns:
    #     try:
    #         if not(cum_on):
    #             df.reset_index()[i].plot()
    #         else:
    #             df.reset_index()[i].cumprod().plot()
    #     except:
    #         pass
    # if threshold is not None:
    #     ax.axhline(threshold, linestyle='--', color='blue')
    #     ax.axhline(-1 * threshold, linestyle='--', color='blue')
    # ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    # plt.legend(df.columns)
    # plt.title(code)


        

    if is_saving:
        try:
            plt.savefig('image/temp.png', format='png')
        except:
            print('saving figure has some problem')
    elif is_base64:
        with io.BytesIO() as f:
            plt.savefig(f, format='png')
            return 'data:image/png;base64,' + base64.b64encode(f.getvalue()).decode('utf8')
    if is_showing:
        plt.show()
