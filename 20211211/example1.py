import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np


def test1():
    # read dataset
    df = pd.read_csv('data/cereal.csv')
    # get correlations
    df_corr = df.corr()  # 13X13
    # irrelevant fields
    fields = ['rating', 'shelf', 'cups', 'weight']
    df_corr.drop(fields, inplace=True)  # 9X13
    # drop cols
    df_corr.drop(fields, axis=1, inplace=True)  # 9X9

    mask = np.triu(np.ones_like(df_corr, dtype=np.bool))

    sb.heatmap(df_corr, mask=mask)
    plt.show()




def test2():
    # read dataset
    df = pd.read_csv('data/cereal.csv')
    # get correlations
    df_corr = df.corr()  # 13X13
    # irrelevant fields
    fields = ['rating', 'shelf', 'cups', 'weight']
    df_corr.drop(fields, inplace=True)  # 9X13
    # drop cols
    df_corr.drop(fields, axis=1, inplace=True)  # 9X9

    mask = np.triu(np.ones_like(df_corr, dtype=np.bool))

    # adjust mask and df
    mask = mask[1:, :-1]
    corr = df_corr.iloc[1:, :-1].copy()
    # plot heatmap
    sb.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='Blues',
               vmin=-1, vmax=1, cbar_kws={"shrink": .8})
    # yticks
    plt.yticks(rotation=0)
    plt.show()


def test3():
    # read dataset
    df = pd.read_csv('data/cereal.csv')
    # get correlations
    df_corr = df.corr()  # 13X13
    # irrelevant fields
    fields = ['rating', 'shelf', 'cups', 'weight']
    df_corr.drop(fields, inplace=True)  # 9X13
    # drop cols
    df_corr.drop(fields, axis=1, inplace=True)  # 9X9

    fig, ax = plt.subplots(figsize=(12, 10))
    # mask
    mask = np.triu(np.ones_like(df_corr, dtype=np.bool))
    # adjust mask and df
    mask = mask[1:, :-1]
    corr = df_corr.iloc[1:, :-1].copy()
    # color map
    cmap = sb.diverging_palette(0, 230, 90, 60, as_cmap=True)
    # plot heatmap
    sb.heatmap(corr, mask=mask, annot=True, fmt=".2f",
               linewidths=5, cmap=cmap, vmin=-1, vmax=1,
               cbar_kws={"shrink": .8}, square=True)
    # ticks
    yticks = [i.upper() for i in corr.index]
    xticks = [i.upper() for i in corr.columns]
    plt.yticks(plt.yticks()[0], labels=yticks, rotation=0)
    plt.xticks(plt.xticks()[0], labels=xticks)
    # title
    title = 'CORRELATION MATRIX\nSAMPLED CEREALS COMPOSITION\n'
    plt.title(title, loc='left', fontsize=18)
    plt.show()


if __name__ == "__main__":
    #test1()
    #test2()
    test3()




