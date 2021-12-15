import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # DATA
    url = './data/film.csv'
    df = pd.read_csv(url, index_col='ID')
    # Theme
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
    g = sns.FacetGrid(df, row="Language", aspect=9, height=1.2)
    g.map_dataframe(sns.kdeplot, x="IMDB Score", fill=True, alpha=1)
    g.map_dataframe(sns.kdeplot, x="IMDB Score", color='black')
    g.fig.subplots_adjust(hspace=-.5)
    g.set_titles("")
    g.set(yticks=[],ylabel="")
    g.despine(left=True)
    plt.savefig('./result/ridgeplot_v4.png')

