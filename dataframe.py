import pandas as pd

def get_df():
    df = pd.read_csv('data.csv')
    return df

def save_df(df):
    df.to_csv('data.csv', index=False)

def add_score(df, bin_board, score):
    new_id = int(bin_board, 2)
    new_row = {'binary': bin_board, 'score': score, 'id': new_id}
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df

def get_score(df, bin_board):
    row = df[df['binary'] == bin_board]
    if not row.empty:
        return row.iloc[0]['score']
    else:
        return None # No score