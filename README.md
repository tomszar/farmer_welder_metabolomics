# Farmer Welder Metabolomics

This repository contains the necessary step to reproduce the metabolomics analysis on the farmer-welder project.
To reproduce the analysis follow the next steps:

## Clone the repository

To clone the repository, open the Terminal, and type:

```bash
git clone https://github.com/tomszar/farmer_welder_metabolomics.git
```

And enter the repository:

```bash
cd farmer_welder_metabolomics
```

## Create the conda environment

With [Anaconda](https://www.anaconda.com/products/individual) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) already installed in your system, install the conda environment using the `environment.yml` file:

```bash
conda env create -f environment.yml
```

And then, activate the environment

```bash
conda activate farmer_welder
```
