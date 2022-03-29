import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from typing import Union
from matplotlib import cm


def concentration_violinplot(D: pd.DataFrame,
                             group_by: Union[pd.Series, None],
                             transform: bool = False,
                             filename: str = 'metabolites_violinplot.pdf',
                             **kwargs):
    '''
    Plot a violinplot from metabolite concentration values.

    Parameters
    ----------
    D: pd.DataFrame
        Dataframe with concentration values
    group_by: pd.Series or None
        Series with the group information
    transform: bool
        Whether to log2 transform the concentration values or not
    filename: str
        File name of the figure with extension
    kwargs: Keyword arguments specific to the axes function
    '''
    if transform:
        D = np.log2(D)

    def set_axis_style(ax, labels, n_groups=1):
        ax.yaxis.set_tick_params(direction='out',
                                 labelrotation=10,
                                 labelsize=10)
        if n_groups > 1:
            ticks = np.arange(1, (len(labels) * (n_groups + 1)) + 1)
            base_bool = list(np.repeat(True, n_groups))
            base_bool.append(False)
            select_bool = base_bool * len(labels)
            pos = ticks[select_bool]
            label_pos = []
            for i in range(0, len(pos), n_groups):
                max_ind = i + n_groups - 1
                lp = (pos[i] + pos[max_ind]) / 2
                label_pos.append(lp)
        else:
            pos = np.arange(1, len(labels) + 1)
            label_pos = pos
            ax.set_ylim(0.25, len(labels) + 0.75)

        ax.set_yticks(label_pos, labels=labels)
        return(pos)

    # Violin plot
    colors = cm.get_cmap('Set2')
    fig = plt.figure(figsize=(8, 12),
                     dpi=300)
    ax = fig.add_subplot(111,
                         **kwargs)
    lab = list(D.columns)
    if group_by is not None:
        patches = []
        n_groups = len(group_by.unique())
        pos = set_axis_style(ax, lab, n_groups)
        for i in range(n_groups):
            p = mlines.Line2D([], [],
                              color=colors(i),
                              marker='o',
                              label=group_by.unique()[i],
                              ms=10,
                              ls='-')
            patches.append(p)
        ax.legend(handles=patches)
    else:
        n_groups = 1
        pos = set_axis_style(ax, lab)

    for g in range(n_groups):
        if group_by is not None:
            sub = group_by.unique()[g]
            subjects = group_by == sub
            list_indices = [*range(g, len(pos), n_groups)]
            pos_m = [pos[i] for i in list_indices]
        else:
            subjects = np.repeat(True, len(D))
            pos_m = pos

        Dm = D.loc[subjects, :]
        # Filter NA data using np.isnan
        mask = ~np.isnan(np.array(Dm))
        Dm_na = [d[m] for d, m in zip(np.array(Dm).T, mask.T)]
        parts = ax.violinplot(Dm_na,
                              pos_m,
                              widths=1,
                              showmedians=True,
                              vert=False)
        # Explicitly set color
        for pc in parts['bodies']:
            pc.set_color(colors(g))
            pc.set_alpha(0.7)

    fig.tight_layout()
    fig.savefig('results/figures/' + filename,
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
    n_vars = pca_scores.shape[1]
    n_plots = n_vars // 2
    rows = 2
    cols = int(np.ceil(n_plots / 2))
    height = 6
    width = height * (cols / rows)
    fig = plt.figure(figsize=(width, height))
    axes = []
    for a in range(n_plots):
        ax = fig.add_subplot(rows, cols, a + 1)
        axes.append(ax)

    if groups is not None and continuous is not None:
        print('Cannot plot groups and continuous at the same time')
    elif groups is not None:
        for i in np.unique(groups):
            b = groups == i
            comp = 0
            for m in range(n_plots):
                axes[m].scatter(pca_scores[b, comp],
                                pca_scores[b, comp + 1])
                comp = comp + 2
    elif continuous is not None:
        comp = 0
        for m in range(n_plots):
            axes[m].scatter(pca_scores[:, comp],
                            pca_scores[:, comp + 1],
                            c=continuous)
            comp = comp + 2
    else:
        comp = 0
        for m in range(n_plots):
            axes[m].scatter(pca_scores[:, comp],
                            pca_scores[:, comp + 1])
            comp = comp + 2

    plt.tight_layout()
    plt.savefig('results/figures/' + filename + '.pdf',
                dpi=600)
