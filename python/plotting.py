import matplotlib.pyplot as plt
import seaborn as sns
import time
from data_handlers import calc_time
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D


def seg_plot(DF, x_col, y_col):
    """ Simple Scatter Plot For Visualizing Data."""
    plt.figure(figsize=(20, 15))
    sns.scatterplot(x=DF[x_col], y=DF[y_col], hue=DF['Label'], palette=['g', 'r', 'c', 'm', 'y'])
    plt.title('Segmentation (K-means)')


def variance_chart(pcs_pointer):
    """ Simple Variance Chart For Visualizing How Much Is Explained By Each Variable Passed."""
    plt.figure(figsize=(20, 15))
    plt.plot(range(1, len(pcs_pointer.components_) + 1), pcs_pointer.explained_variance_ratio_.cumsum(), marker='o',
             linestyle='--')
    plt.title("Explained Variance By Components")
    plt.xlabel("Number of Components")
    plt.ylabel("Cumulative Explained Variance")


def compare_hmap(DF, components):
    """ Heatmap For Visualizing How The Components Stack Up In Terms Of Correlations."""
    plt.figure(figsize=(20, 15))
    sns.heatmap(DF,
                vmin=-1,
                vmax=1,
                cmap='RdBu',
                annot=True)
    plt.yticks(range(len(components)),
               components,
               rotation=45,
               fontsize=12)
    plt.title('Components vs Original Features', fontsize=12)


def corr_hmap(DF):
    """ Simple Heatmap Which Takes A DataFrame as Input And Outputs A Chart Showing DataFrame Correlations."""
    data = None
    if isinstance(DF, pd.DataFrame):
        data = DF.corr()
    if type(DF) == list:
        data = DF
    plt.figure(figsize=(20,15))
    sns.heatmap(data, vmin=-1, vmax=1, annot=True, cmap="RdBu")
    plt.title("Correlation Heatmap", fontsize=14)
    plt.yticks(rotation=0)
    plt.show()


def pplot(DF, hue=None):
    """ Seaborn Pair Plot For Visualizing How All The Data Correlates To One Another In Charts."""
    start = time.time()
    sns.pairplot(DF, hue=hue)
    plt.show()
    print(calc_time(start, time.time()))


def scatter_3D(DF, comp1="Component 1", comp2="Component 2", comp3="Component 3", colored_by="K-means PCA", cmap=None,
               elev=None, azim=None):
    """ Creates A 3D scatter plot of 3 variables."""
    if cmap is None:
        cmap = 'icefire_r'

    fig = plt.figure(figsize=(20, 15))
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)

    ax.set_xlabel(comp1)
    ax.set_ylabel(comp2)
    ax.set_zlabel(comp3)

    ax.legend(DF[colored_by])

    ax.scatter3D(DF[comp1], DF[comp2], DF[comp3], c=DF[colored_by], cmap=cmap)

    plt.title(colored_by)
    ax.view_init(elev, azim)
    plt.show()



