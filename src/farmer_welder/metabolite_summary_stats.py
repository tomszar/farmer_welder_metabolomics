import load
import stats
import figures
import numpy as np

if __name__ == "__main__":
    farmers = load.load_data('farmers')
    welders = load.load_data('welders')

    covs = ['age', 'sex', 'project_id', 'currently_smoking']
    outcomes = load.get_metabolites()
    metals = load.get_metals(37016)

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
                                     filename='metabolites_welders_b.pdf')

    metal_concentration = np.log2(welders[metals])
    figures.concentration_violinplot(metal_concentration,
                                     groups,
                                     filename='metals_welders_b.pdf')

    concen = np.log2(welders_nb.loc[:, outcomes] + 0.01)
    groups = welders_nb['research_subject']
    figures.concentration_violinplot(concen,
                                     groups,
                                     filename='metabolites_welders_nb.pdf')

    metal_concentration = np.log2(welders_nb[metals])
    figures.concentration_violinplot(metal_concentration,
                                     groups,
                                     filename='metals_welders_nb.pdf')

    # PCA
    pca = stats.generate_PCA(concen)
    pca_scores = pca.transform(concen)
    figures.plot_pca_scores(pca_scores,
                            groups=groups)

    # Association study
    replace_subjects = {'Retired': 'Welder',
                        'Active': 'Welder'}
    welders = welders.replace(replace_subjects)
    welders_nb = welders_nb.replace(replace_subjects)
    predictors = ['research_subject']
    res = stats.EWAS(outcomes,
                     covs,
                     predictors,
                     welders,
                     remove_outliers=True)
    res.to_csv('../results/welder_res_binary.csv')

    outcomes_replication = ['Acetate',
                            'Pyruvate',
                            '3-Hydroxyisovalerate',
                            'Formate']
    res = stats.EWAS(outcomes_replication,
                     covs,
                     predictors,
                     welders_nb,
                     remove_outliers=True)
    res.to_csv('../results/welder_res_binary_replication.csv')

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
