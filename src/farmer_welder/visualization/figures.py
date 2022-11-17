import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from typing import Union
from matplotlib import cm
from farmer_welder.stats import stats


def concentration_violinplot(dat: Union[pd.DataFrame, pd.Series],
                             ax: plt.Axes,
                             group_by: Union[pd.Series, None]):
    """
    Plot a violin plot from metabolite concentration values.

    Parameters
    ----------
    dat: pd.DataFrame or pd.Series
        Dataframe with concentration values.
    ax: plt.Axes
        Axis to use for the plot.
    group_by: pd.Series or None
        Series with the group information.
    """
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
        return pos

    # Violin plot
    colors = cm.get_cmap('Set2')
    lab = []
    if isinstance(dat, pd.DataFrame):
        lab = list(dat.columns)
    elif isinstance(dat, pd.Series):
        lab = [dat.name]

    if group_by is not None:
        patches = []
        group_labels = group_by.unique()
        group_labels.sort()
        n_groups = len(group_by.unique())
        pos = set_axis_style(ax, lab, n_groups)
        for i in range(n_groups):
            p = mlines.Line2D([], [],
                              color=colors(i),
                              marker='o',
                              label=group_labels[i],
                              ms=10,
                              ls='-')
            patches.append(p)
        ax.legend(handles=patches)
    else:
        n_groups = 1
        pos = set_axis_style(ax, lab)

    for g in range(n_groups):
        if group_by is not None:
            sub = group_labels[g]
            subjects = group_by == sub
            list_indices = [*range(g, len(pos), n_groups)]
            pos_m = [pos[i] for i in list_indices]
        else:
            subjects = np.repeat(True, len(dat))
            pos_m = pos

        # Filter NA data using np.isnan if DataFrame
        if isinstance(dat, pd.DataFrame):
            datm = dat.loc[subjects, :]
            mask = ~np.isnan(np.array(datm))
            datm_na = [d[m] for d, m in zip(np.array(datm).T, mask.T)]
        elif isinstance(dat, pd.Series):
            datm = dat.loc[subjects]
            datm_na = datm.dropna()
        else:
            datm_na = pd.DataFrame()

        parts = ax.violinplot(datm_na,
                              pos_m,
                              widths=1,
                              showmedians=True,
                              vert=False)
        # Explicitly set color
        for pc in parts['bodies']:
            pc.set_color(colors(g))
            pc.set_alpha(0.7)


def plot_pca_scores(pca_scores: np.ndarray,
                    groups: Union[np.ndarray, pd.Series, None] = None,
                    continuous: Union[np.ndarray, pd.Series, None] = None,
                    filename: str = 'metabolites_pca'):
    '''
    Plot the PCA scores

    Parameters
    ----------
    pca_scores: np.ndarray
        scores from a PCA.
    groups: np.ndarray or pd.Series
        grouping categories to plot.
    continuous: np.ndarray or pd.Series
        continuous variable to use for color
    filename: str
        name of figure file without extension.
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
                                pca_scores[b, comp + 1],
                                label=i)
                comp = comp + 2
        plt.legend()
    elif continuous is not None:
        comp = 0
        for m in range(n_plots):
            scatter = axes[m].scatter(pca_scores[:, comp],
                                      pca_scores[:, comp + 1],
                                      c=continuous,
                                      label=continuous)
            comp = comp + 2
        # produce a legend with a cross-section of continuous from the scatter
        handles, labels = scatter.legend_elements(prop="colors", alpha=0.6)
        plt.legend(handles, labels, loc="upper right", title="Sizes")
    else:
        comp = 0
        for m in range(n_plots):
            axes[m].scatter(pca_scores[:, comp],
                            pca_scores[:, comp + 1])
            comp = comp + 2

    plt.tight_layout()
    plt.savefig('results/figures/' + filename + '.pdf',
                dpi=600)


def correlation_plot(data: Union[pd.DataFrame, np.ndarray],
                     labels: Union[list[str], None] = None,
                     estimate_corr: bool = True,
                     filename: str = 'correlation_plot.png'):
    '''
    Generation a correlation plot over all columns of data

    Parameters
    ----------
    data: pd.DataFrame
        Data from which to generate the correlation plot
    estimate_corr: bool
        Whether to estimate the correlation or not. If False,
        it's assumed that the data is a correlation or distance matrix
    filename: str
        Name of the plot file
    '''
    if estimate_corr:
        # Generate correlation and labels
        correlations = np.array(pd.DataFrame(data).corr())
        np.fill_diagonal(correlations,
                         0, wrap=False)
    else:
        correlations = np.array(data)
        np.fill_diagonal(correlations,
                         0, wrap=False)

    # Sort the matrix to look better
    idx = stats.cluster_corr(correlations)
    correlations = correlations[idx, :][:, idx]

    # Generate the figure
    fig, ax = plt.subplots(figsize=(10, 8))
    vmin = correlations.min()
    vmax = correlations.max()
    if vmin < 0:
        cmap = 'PiYG'
    else:
        cmap = 'Reds'
    im = ax.imshow(correlations,
                   cmap=cmap,
                   vmin=-1,
                   vmax=1)
    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax,)
    cbar.ax.set_ylabel('Correlation coefficient',
                       rotation=-90,
                       va='bottom')
    # Turn spines off and create white grid
    ax.spines[:].set_visible(False)
    ax.set_xticks(np.arange(correlations.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(correlations.shape[0]+1)-.5, minor=True)
    ax.grid(which='minor', color='w', linestyle='-', linewidth=3)
    ax.tick_params(which='minor', bottom=False, left=False)
    # Set tick labels and rotations
    if labels is not None:
        tuples = sorted(zip(list(idx), labels))
        idxl, labels = [t[0] for t in tuples], [t[1] for t in tuples]
        ax.set_xticks(np.arange(len(correlations)),
                      labels=labels,
                      rotation=45,
                      ha='right')
        ax.set_yticks(np.arange(len(correlations)),
                      labels=labels)
    # Save figure
    fig.tight_layout()
    fig.savefig('results/figures/' + filename,
                dpi=600)
