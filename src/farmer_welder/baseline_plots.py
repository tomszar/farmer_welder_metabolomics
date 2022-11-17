from .data import load
from .visualization import figures


def main():
    bs = load.load_baseline_data('welders')
    metabolites = load.get_metabolites()
    metals = load.get_metals(37016)
    exposures = ['elt', 'e90', 'hrsw'] + metals
    filenames = ['metabolites_welders_bs_corr',
                 'exposures_welders_bs_corr']
    full_corr_name = 'full_welders_bs_corr'
    # Create correlation and violinplots plots by cohort
    for study, dat in bs.groupby('Study ID'):
        figures.correlation_plot(dat[metabolites + metals + exposures],
                                 labels=metabolites + metals + exposures,
                                 filename=full_corr_name + '_' +
                                 str(study) + '.png')
        for i, cols in enumerate([metabolites, exposures]):
            figures.correlation_plot(dat[cols],
                                     labels=cols,
                                     filename=filenames[i] + '_' +
                                     str(study) + '.png')
