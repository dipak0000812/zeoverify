import torch
from transformers import BertTokenizer
from train import BERTDocumentClassifier
import torch.nn.functional as F

# Load model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BERTDocumentClassifier()
model.load_state_dict(torch.load("bert_doc_classifier.pth", map_location=torch.device('cpu')))
model.eval()

# Labels
label_map = {0: "valid", 1: "fake", 2: "invalid"}

def predict_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    with torch.no_grad():
        logits = model(input_ids, attention_mask)
        probs = F.softmax(logits, dim=1)
        confidence, predicted_class = torch.max(probs, dim=1)

    label = label_map[predicted_class.item()]
    confidence_pct = round(confidence.item() * 100, 2)

    return label, confidence_pct

# Test
if __name__ == "__main__":
    while True:
        user_input = input("\n📄 Enter text (or 'exit'): ")
        if user_input.lower() == 'exit':
            break
        label, score = predict_text(user_input)
        print(f"🔍 Prediction: {label.upper()} | Confidence: {score}%")
