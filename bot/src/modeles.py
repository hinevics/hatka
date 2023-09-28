import re
from pathlib import Path
import pandas as pd
import joblib
from sklearn.neighbors import NearestNeighbors

from config import PATH_NN_MODEL, PATH_PCA_MODEL, PATH_VECTORIZER_MODEL


def load_model(path: str) -> NearestNeighbors:
    if not Path(path).exists():
        model = joblib.load(path)
        return model
    raise FileExistsError('Файла нет!')


def clear_text(text: str) -> str:
    text = text.lower()
    # DOT
    # text = re.sub(pattern=r'\.', string=text, repl=' DOT ')
    # Comma
    # text = re.sub(pattern=r'\,', string=text, repl=' COMMA ')
    text = re.sub(pattern=r'\W', string=text, repl=' ')
    # text = re.sub(pattern='\d+',repl=' NUMBER ', string=text)
    text = re.sub(pattern=r'\d+', repl='', string=text)
    text = ' '.join([i for i in text.split(' ') if (len(i) > 1 and i not in ['', ' '])])
    # text = "POS " + text + " POS"
    return text


def processing(data: pd.DataFrame) -> pd.DataFrame:
    text_df = pd.DataFrame()
    text_df['text'] = data.text + ' ' + data.note
    text_df['clear_text'] = text_df.text.map(clear_text)
    return text_df


def predict(data: pd.DataFrame):
    pass