import clarite
import pandas as pd
import statsmodels.formula.api as smf
from typing import List

from farmer_welder.data import load, clean
from farmer_welder.stats import stats
from statsmodels.stats.multitest import multipletests


def transform(dat: pd.DataFrame,
              replace_columns: dict,
              exposures: List[str],
              metabolites: List[str],
              grouping: List[bool]) -> pd.DataFrame:
    """
    Transform column names and transform data

    Parameters
    ----------
    dat: pd.DataFrame
        Original dataset.
    replace_columns: dict
        Dictionary with column names to replace.
    exposures: List[str]
        List of exposures to transform.
    metabolites: List[str]
        List of metabolites to transform.
    grouping: list[bool]
        List of bool to separate two groups.

    Returns
    -------
    dat: pd.DataFrame
        Transformed dataset.
    """
    dat = dat.rename(columns=replace_columns)
    dat = clean.transform_to_dummy(dat)
    dat.loc[:, exposures] = stats.transform_data(dat.loc[:, exposures],
                                                 grouping=grouping)
    dat.loc[:, metabolites] = stats.transform_data(dat.loc[:, metabolites],
                                                   grouping=grouping)
    return dat


def analysis(dat: pd.DataFrame,
             exposures: List[str],
             metabolites: List[str],
             covariates: str,
             baseline: bool = True) -> pd.DataFrame:
    """
    Main analysis.

    Parameters
    ----------
    dat: pd.DataFrame
        Data frame to run analysis.
    exposures: List[str]
        List of exposures to transform.
    metabolites: List[str]
        List of metabolites to transform.
    covariates: str
        Covariates in formula style (e.g. 'cov1 + cov2').
    baseline: bool
        Run the analysis with baseline data (no repeated measures). Else, runs
        a linear mixed model for repeated measures.

    Returns
    -------
    res: pd.DataFrame
        Results table.
    """
    # Creating results dataset
    combinations = [(x, y) for x in exposures for y in metabolites]
    res = pd.DataFrame(combinations, columns=['exposures', 'metabolites'])
    res.loc[:, 'converged'] = True
    res.loc[:, ['pvalue', 'coef', 'nobs']] = 0
    res = res.set_index(['exposures', 'metabolites'])

    for exp in exposures:
        for met in metabolites:
            dat.loc[:, [exp, met]] = clarite.modify.remove_outliers(dat.loc[:, [exp, met]])
            if baseline:
                formula = met + ' ~ ' + covariates + ' + ' + exp
                mdf = smf.ols(formula, dat,
                              missing='drop').fit()
            else:
                formula = met + ' ~ ' + covariates + ' + ' + exp + ' * Visit'
                mdf = smf.mixedlm(formula, dat,
                                  groups=dat.loc[:, 'study_id'], missing='drop').fit()
                res.loc[(exp, met), 'converged'] = mdf.converged
            res.loc[(exp, met), 'pvalue'] = mdf.pvalues[exp]
            res.loc[(exp, met), 'coef'] = mdf.params[exp]
            res.loc[(exp, met), 'nobs'] = mdf.nobs

    # Correct for multiple testing
    converged_tests = res.loc[:, 'converged']
    pvalue_fdr = multipletests(res.loc[converged_tests, 'pvalue'],
                               method='fdr_bh')
    res.loc[:, 'pvalue_fdr'] = 1
    res.loc[converged_tests, 'pvalue_fdr'] = pvalue_fdr[1]
    return res


def main():
    """
    Main routine
    """
    welders = pd.read_csv('data/processed/welders.csv')
    grouping = welders.loc[:, 'project_id'] == 37016
    welders_bs = load.load_baseline_data('welders')
    grouping_bs = welders_bs.loc[:, 'project_id'] == 37016
    exposures = ['elt', 'e90', 'fe', 'mn', 'pb']
    og_metabolites = load.get_metabolites()
    metabolites = load.get_metabolites(True)
    replace_metabolites = dict(zip(og_metabolites, metabolites))
    welders = transform(welders, replace_metabolites, exposures, metabolites,
                        grouping)
    welders_bs = transform(welders_bs, replace_metabolites, exposures,
                           metabolites, grouping_bs)
    covariates = 'age + years_of_education + sexd + ' \
                 'smoked_regularly + project_idd'

    res = analysis(welders, exposures, metabolites, covariates, baseline=False)
    res_bs = analysis(welders_bs, exposures, metabolites, covariates)
    res.to_csv('results/reports/LMM_res.csv')
    res_bs.to_csv('results/reports/LR_res.csv')
