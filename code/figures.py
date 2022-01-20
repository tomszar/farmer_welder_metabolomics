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


def plot_pca_scores(pca_scores,
                    groups=None,
                    continuous=None,
                    filename='metabolites_pca'):
    '''
    Plot the PCA scores

    Parameters
    ----------
    pca_scores: np.ndarray
        scores from a PCA
    groups: np.array
        grouping categories to plot
    continuous: np.array
        continuous variable to use for color
    filename: str
        name of figure file
    '''
    fig, ax = plt.subplots(figsize=(8, 8))
    if groups is not None and continuous is not None:
        print('Cannot plot groups and continuous at the same time')
    elif groups is not None:
        for i in np.unique(groups):
            b = groups == i
            ax.scatter(pca_scores[b, 0],
                       pca_scores[b, 1])
    elif continuous is not None:
        ax.scatter(pca_scores[:, 0],
                   pca_scores[:, 1],
                   c=continuous)
    else:
        ax.scatter(pca_scores[:, 0],
                   pca_scores[:, 1])

    plt.tight_layout()
    plt.savefig('../results/' + filename + '.pdf',
                dpi=600)
