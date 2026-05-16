import pandas as pd
import json

def analyze_data():
    titck_path = 'titck_liste_18.04.csv'
    atc_path = 'ATC_14_04.xlsx'
    
    # Read TITCK
    try:
        df_titck = pd.read_csv(titck_path, sep=';') # Try semicolon first, if fails try comma
    except:
        df_titck = pd.read_csv(titck_path)
    
    # Read ATC
    df_atc = pd.read_excel(atc_path)
    
    analysis = {
        'TITCK': {
            'shape': df_titck.shape,
            'columns': list(df_titck.columns),
            'head': df_titck.head(3).to_dict(orient='records')
        },
        'ATC': {
            'shape': df_atc.shape,
            'columns': list(df_atc.columns),
            'head': df_atc.head(3).to_dict(orient='records')
        }
    }
    
    with open('data_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    analyze_data()
