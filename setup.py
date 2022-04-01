from setuptools import setup, find_packages


setup(
    name='farmer_welder',
    version='0.1.0',
    description='Farmer Welder metabolomics analysis',
    author='Tomas Gonzalez Zarzar',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'create_folders=farmer_welder.create_folders:main',
            'merge_data=farmer_welder.merge_data:main',
            'baseline_analysis=farmer_welder.baseline_analysis:main',
            'baseline_plots=farmer_welder.baseline_plots:main',
            'run_summary=farmer_welder.metabolite_summary_stats:main',
        ]
    }
)
