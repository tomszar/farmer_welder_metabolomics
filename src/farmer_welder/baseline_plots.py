from .data import load
from .stats import stats
from .visualization import figures


def main():
    bs = load.load_baseline_data('welders')
    metabolites = load.get_metabolites()
    metals = load.get_metals(37016)
    exposures = ['elt', 'e90', 'hrsw']
    filenames = ['metabolites_welders_bs_corr',
                 'metals_welders_bs_corr',
                 'exposures_welders_bs_corr']
    full_corr_name = 'full_welders_bs_corr'
    # Create correlation and violinplots plots by cohort
    for study, dat in bs.groupby('Study ID'):
        figures.correlation_plot(dat[metabolites + metals + exposures],
                                 full_corr_name + '_' + str(study) + '.pdf')
        for i, cols in enumerate([metabolites, metals, exposures]):
            figures.correlation_plot(dat[cols],
                                     filenames[i] + '_' + str(study) + '.pdf')
            groups = dat['research_subject']
            names = ['metabolites', 'metals']
            titles = ['Metabolite concentrations',
                      'Metal concentrations']
            if i < 2:
                if i == 0:
                    data_violin = dat[cols] + 1/100000000
                else:
                    data_violin = dat[cols]
                data_violin = stats.transform_data(data_violin)
                filename = names[i] + '_welders_bs_' + str(study) + '.pdf'
                figures.concentration_violinplot(data_violin,
                                                 groups,
                                                 filename=filename,
                                                 xlabel='Log2 concentration',
                                                 title=titles[i])
            elif i == 2:
                titles = ['Lifetime exposure',
                          'Short-term exposure',
                          'Hours welding']
                for m, expo in enumerate(cols):
                    data_violin = dat[[expo]]
                    data_violin = stats.transform_data(data_violin,
                                                       log2_transform=False)
                    filename = expo + '_welders_bs_' + str(study) + '.pdf'
                    figures.concentration_violinplot(data_violin,
                                                     groups,
                                                     filename=filename,
                                                     xlabel='Exposure value',
                                                     title=titles[m])
