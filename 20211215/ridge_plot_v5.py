import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# function to draw labels
def label(x, color, label):
    ax = plt.gca() #get current axis
    ax.text(0, .2, label, color='black', fontsize=13,ha="left", va="center", transform=ax.transAxes)


if __name__ == "__main__":
    # DATA
    url = './data/film.csv'
    df = pd.read_csv(url, index_col='ID')
    # Theme
    sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0), 'axes.linewidth':2})
    palette = sns.color_palette("Set2", 12)
    # create a grid with a row for each 'Language'
    g = sns.FacetGrid(df, palette=palette, row="Language", hue="Language", aspect=9, height=1.2)

    # map df - Kernel Density Plot of IMDB Score for each Language
    g.map_dataframe(sns.kdeplot, x="IMDB Score", fill=True, alpha=1)
    g.map_dataframe(sns.kdeplot, x="IMDB Score", color='black')

    # iterate grid to plot labels
    g.map(label, "Language")
    # adjust subplots to create overlap
    g.fig.subplots_adjust(hspace=-.5)

    # remove subplot titles
    g.set_titles("")
    # remove yticks and set xlabel
    g.set(yticks=[], ylabel="",xlabel="IMDB Score")
    # remove left spine
    g.despine(left=True)
    # set title
    plt.suptitle('Netflix Originals - IMDB Scores by Language', y=0.98)
    plt.savefig('./result/ridgeplot_v5.png')
