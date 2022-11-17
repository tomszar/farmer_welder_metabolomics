import clarite
import pandas as pd
import statsmodels.formula.api as smf

from farmer_welder.data import load, clean
from farmer_welder.stats import stats
from statsmodels.stats.multitest import multipletests


def main():
    """
    Main routine
    """
    welders = pd.read_csv('data/processed/welders.csv')
    grouping = welders.loc[:, 'project_id'] == 37016
    exposures = ['elt', 'e90', 'fe', 'mn', 'pb']
    metabolites = load.get_metabolites()
    welders = clean.transform_to_dummy(welders)
    welders.loc[:, exposures] = stats.transform_data(welders.loc[:, exposures],
                                                     grouping=grouping)
    welders.loc[:, metabolites] = stats.transform_data(welders.loc[:, metabolites],
                                                       grouping=grouping)
    # Removing metabolites starting with numbers meanwhile
    metabolites = metabolites[4:]
    covariates = 'age + years_of_education + sexd + ' \
                 'smoked_regularly + project_idd'

    # Creating results dataset
    combinations = [(x, y) for x in exposures for y in metabolites]
    res = pd.DataFrame(combinations, columns=['exposures', 'metabolites'])
    res.loc[:, 'converged'] = True
    res.loc[:, ['pvalue', 'coef']] = 0
    res = res.set_index(['exposures', 'metabolites'])

    for exp in exposures:
        for met in metabolites:
            dat = welders
            dat.loc[:, [exp, met]] = clarite.modify.remove_outliers(dat.loc[:, [exp, met]])
            formula = met + ' ~ ' + covariates + ' + ' + exp + ' * Visit'
            md = smf.mixedlm(formula, dat,
                             groups=dat.loc[:, 'study_id'], missing='drop')
            mdf = md.fit()
            res.loc[(exp, met), 'converged'] = mdf.converged
            res.loc[(exp, met), 'pvalue'] = mdf.pvalues[exp]
            res.loc[(exp, met), 'coef'] = mdf.params[exp]

    # Correct for multiple testing
    converged_tests = res.loc[:, 'converged']
    pvalue_fdr = multipletests(res.loc[converged_tests, 'pvalue'],
                               method='fdr_bh')
    res.loc[:, 'pvalue_fdr'] = 1
    res.loc[converged_tests, 'pvalue_fdr'] = pvalue_fdr[1]
    res.to_csv('results/reports/LMM_res.csv')
