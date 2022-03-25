from .data import load


def main():
    farmers = load.load_data('farmers')
    welders = load.load_data('welders')

    farmers.to_csv('data/processed/farmers.csv',
                   index=False)
    welders.to_csv('data/processed/welders.csv',
                   index=False)
    print('Farmer and Welder data consolidated')
