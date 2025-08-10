from transformers import BertTokenizer
import pandas as pd

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def preprocess_bert(text_list, max_length=512):
    return tokenizer(
        text_list,
        padding='max_length',
        truncation=True,
        max_length=max_length,
        return_tensors="pt"
    )

def load_dataset(path):
    df = pd.read_csv(path)
    texts = df['text'].tolist()
    labels = df['label'].map({'valid': 0, 'fake': 1, 'invalid': 2}).tolist()
    return preprocess_bert(texts), labels
