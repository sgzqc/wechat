import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    url = "./data/pulsar.csv"
    df = pd.read_csv(url, header=None)
    df = df.stack().reset_index()
    df.columns = ['idx', 'x', 'y']
    sns.set_theme(rc={"axes.facecolor": (0, 0, 0, 0), 'figure.facecolor':'#000000', 'axes.grid':False})
    g = sns.FacetGrid(df, row='idx', aspect=50, height=0.4)
    # Draw the densities in a few steps
    g.map(sns.lineplot, 'x', 'y', clip_on=False, alpha=1, linewidth=1.5)
    g.map(plt.fill_between, 'x', 'y', color='#000000')
    g.map(sns.lineplot, 'x', 'y', clip_on=False, color='#ffffff', lw=2)
    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-0.95)
    g.set_titles("")
    g.set(yticks=[], xticks=[], ylabel="", xlabel="")
    g.despine(bottom=True, left=True)
    plt.savefig('./result/ridgeplot_v6.png', facecolor='#000000')

