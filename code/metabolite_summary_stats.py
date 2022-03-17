import load
import stats
import figures
import numpy as np

farmers = load.load_data('farmers')
welders = load.load_data('welders',
                         baseline=True)
replace_subects = {'Retired': 'Welder',
                   'Active': 'Welder'}
welders = welders.replace(replace_subects)

covs = ['age', 'sex']
predictors = ['research_subject']
outcomes = list(welders.iloc[:, 25:].columns)

res = stats.EWAS(outcomes,
                 covs,
                 predictors,
                 welders)
res.to_csv('../results/welder_res_binary.csv')

predictors = ['lifetime_exposure']
change_bool = welders['lifetime_exposure'] > 0
welders.loc[change_bool, 'lifetime_exposure'] = np.log10(
    welders.loc[change_bool, 'lifetime_exposure'])
res = stats.EWAS(outcomes,
                 covs,
                 predictors,
                 welders)
res.to_csv('../results/welder_res_cont.csv')

# Violin plots
concen = np.log2(farmers.iloc[:, 26:] + 0.01)
groups = farmers['research_subject']
figures.concentration_violinplot(concen,
                                 groups,
                                 filename='metabolites_farmers_grouped.pdf')
figures.concentration_violinplot(concen,
                                 filename='metabolites_farmers_total.pdf')

concen = np.log2(welders.loc[:, outcomes] + 0.01)
groups = welders['research_subject']
figures.concentration_violinplot(concen,
                                 groups,
                                 filename='metabolites_welders_grouped.pdf')
figures.concentration_violinplot(concen,
                                 filename='metabolites_welders_total.pdf')

# PCA
# pca_scores = stats.generate_PCA(concen)
# figures.plot_pca_scores(pca_scores,
#                         groups=groups)
# figures.plot_pca_scores(pca_scores,
#                         continuous=farmers['age'],
#                         filename='metabolites_pca_age')
#
