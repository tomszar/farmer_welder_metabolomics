import load
import stats
import figures
import numpy as np

farmers = load.load_data('farmers')
welders = load.load_data('welders',
                         baseline=True)
covs = ['age', 'sex', 'project_id']
outcomes = load.get_metabolites()

# Summary figures
# Violin plots
concen = np.log2(farmers.loc[:, outcomes] + 0.01)
groups = farmers['research_subject']
figures.concentration_violinplot(concen,
                                 groups,
                                 filename='metabolites_farmers.pdf')

concen = np.log2(welders.loc[:, outcomes] + 0.01)
groups = welders['research_subject']
figures.concentration_violinplot(concen,
                                 groups,
                                 filename='metabolites_welders.pdf')

metals = load.get_metals(37016)
metal_concentration = np.log2(welders[metals])
figures.concentration_violinplot(metal_concentration,
                                 groups,
                                 filename='metals_welders.pdf')

# PCA
pca = stats.generate_PCA(concen)
pca_scores = pca.transform(concen)
figures.plot_pca_scores(pca_scores,
                        groups=groups)

replace_subjects = {'Retired': 'Welder',
                    'Active': 'Welder'}
welders = welders.replace(replace_subjects)
predictors = ['research_subject']
res = stats.EWAS(outcomes,
                 covs,
                 predictors,
                 welders,
                 remove_outliers=True)
res.to_csv('../results/welder_res_binary.csv')

predictors = ['lifetime_exposure']
change_bool = welders['lifetime_exposure'] > 0
welders.loc[change_bool, 'lifetime_exposure'] = np.log10(
    welders.loc[change_bool, 'lifetime_exposure'])
res = stats.EWAS(outcomes,
                 covs,
                 predictors,
                 welders,
                 remove_outliers=True)
res.to_csv('../results/welder_res_cont.csv')

predictors = ['pb']
res = stats.EWAS(outcomes,
                 covs,
                 predictors,
                 welders,
                 remove_outliers=True)
res.to_csv('../results/welder_res_pb.csv')
