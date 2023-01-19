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

## Create the conda environment and install

With [Conda](https://docs.conda.io/en/latest/), or [Mamba](https://mamba.readthedocs.io/en/latest/installation.html) already installed in your system, install the environment using the `environment.yml` file:

```bash
mamba env create -f environment.yml
```

Then, activate the environment, load gcc, and install the farmer_welder package and dependencies with [poetry](https://python-poetry.org/docs/).

```bash
conda activate farmer_welder
poetry install
```

For Penn State's Roar system, make sure to run the following before installing the package

```bash
module load gcc
```

## Steps to reproduce the analysis

First, create the data and results layout by running:

```bash
create_folders
```

And copy all the files located in the Penn State Roar's path `mah546/default/datasets/welder_farmer_study/` to the `data/raw` folder.
Then, create the merged data files used for most analysis, by typing:

```bash
merge_data
```

To generate some descriptive plots, run:

```bash
exploratory_plots
```

Finally, to run the analysis, run:

```bash
run_analysis
```
