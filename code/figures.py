import numpy as np
import matplotlib.pyplot as plt


def concentration_violinplot(D,
                             group_by: list = None,
                             transform: bool = False,
                             filename: str = 'metabolites_violinplot.pdf'):
    '''
    Plot a violinplot from metabolite concentration values.

    Parameters
    ----------
    D: pd.DataFrame
        Dataframe with concentration values
    group_by: list of str
        List with group names to use
    transform: bool
        Whether to log2 transform the concentration values or not
    filename: str
        File name of the figure with extension
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
            for i in range(0, len(pos), 2):
                lp = (pos[i] + pos[i + 1]) / 2
                label_pos.append(lp)
        else:
            pos = np.arange(1, len(labels) + 1)
            label_pos = pos
            ax.set_ylim(0.25, len(labels) + 0.75)

        ax.set_yticks(label_pos, labels=labels)
        ax.set_ylabel('Metabolite name')
        return(pos)

    # Violin plot
    fig, ax = plt.subplots(figsize=(8, 12))
    ax.set_title('Metabolite concentration values')
    ax.set_xlabel('Log2 concentration')
    lab = list(D.columns)
    if group_by is not None:
        n_groups = len(group_by.unique())
        pos = set_axis_style(ax, lab, n_groups)
    else:
        n_groups = 1
        pos = set_axis_style(ax, lab)

    for g in range(n_groups):
        if group_by is not None:
            sub = group_by.unique()[g]
            subjects = group_by == sub
            pos_m = pos[range(g, len(pos), 2)]
        else:
            subjects = np.repeat(True, len(D))
            pos_m = pos

        Dm = D.loc[subjects, :]
        ax.violinplot(Dm,
                      pos_m,
                      widths=1,
                      vert=False)
    fig.tight_layout()
    fig.savefig('../results/' + filename,
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
