import pandas as pd

def convert(xlsx_filepath: str, csv_filepath: str):
    df = pd.read_excel(xlsx_filepath, header=0)
    df.to_csv(csv_filepath, index=False)
