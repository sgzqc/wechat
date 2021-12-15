import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


if __name__ == "__main__":
    # DATA
    url = './data/film.csv'
    df = pd.read_csv(url, index_col='ID')
    # Theme
    sns.set_theme(style="white")
    g = sns.FacetGrid(df, row="Language", aspect=9, height=1.2)
    g.map_dataframe(sns.kdeplot, x="IMDB Score")
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(left=True)
    plt.savefig('./result/ridgeplot_v3.png')
