import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def concentration_violinplot(D,
                             transform=False):
    '''
    Plot a violinplot from metabolite concentration values.

    Parameters
    ----------
    D: pd.DataFrame
        Dataframe with concentration values
    transform: bool
        Whether to log2 transform the concentration values or not
    '''
    if transform:
        D = np.log2(D)

    def set_axis_style(ax, labels):
        ax.yaxis.set_tick_params(direction='out',
                                 labelrotation=10,
                                 labelsize=10)
        ax.set_yticks(np.arange(1, len(labels) + 1), labels=labels)
        ax.set_ylim(0.25, len(labels) + 0.75)
        ax.set_ylabel('Metabolite name')

    # Violin plot
    fig, ax = plt.subplots(figsize=(8, 12))
    ax.set_title('Metabolite concentration values')
    ax.set_xlabel('Log2 concentration')
    ax.violinplot(D,
                  widths=1,
                  vert=False)
    lab = list(D.columns)
    set_axis_style(ax, lab)
    plt.tight_layout()
    plt.savefig('../results/metabolites_violinplot.pdf',
                dpi=600)


def plot_pca_scores(pca_scores):
    '''
    Plot the PCA scores

    Parameters
    ----------
    pca_scores: np.ndarray
    '''
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(pca_scores[:, 0],
               pca_scores[:, 1])

    plt.tight_layout()
    plt.savefig('../results/metabolites_pca.pdf',
                dpi=600)
