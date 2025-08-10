import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertModel
from sklearn.model_selection import train_test_split
import pandas as pd
from tqdm import tqdm

# ======================
# 🚀 Dataset Class
# ======================
class DocumentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        inputs = self.tokenizer(
            self.texts[idx],
            truncation=True,
            padding='max_length',
            max_length=self.max_len,
            return_tensors='pt'
        )
        return {
            'input_ids': inputs['input_ids'].squeeze(0),         # shape: [512]
            'attention_mask': inputs['attention_mask'].squeeze(0),
            'label': torch.tensor(self.labels[idx], dtype=torch.long)
        }

# ======================
# 🤖 BERT Classifier
# ======================
class BERTDocumentClassifier(nn.Module):
    def __init__(self, num_classes=3):
        super(BERTDocumentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.drop = nn.Dropout(p=0.3)
        self.fc = nn.Linear(self.bert.config.hidden_size, num_classes)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output  # shape: [batch_size, hidden_size]
        output = self.drop(pooled_output)
        return self.fc(output)  # shape: [batch_size, num_classes]

# ======================
# 📄 Load Data
# ======================
df = pd.read_csv('final_dataset.csv')  # Ensure this CSV exists in the working directory
label_map = {'valid': 0, 'fake': 1, 'invalid': 2}
print(df.columns)
exit()

df['label'] = df['label'].map(label_map)

# ======================
# ✂️ Train/Val Split
# ======================
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['text'].tolist(), df['label'].tolist(), test_size=0.1, random_state=42
)

# ======================
# 🔤 Tokenizer
# ======================
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# ======================
# 📦 Datasets & Loaders
# ======================
train_dataset = DocumentDataset(train_texts, train_labels, tokenizer)
val_dataset = DocumentDataset(val_texts, val_labels, tokenizer)

train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

# ======================
# 🧠 Model Setup
# ======================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = BERTDocumentClassifier().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.AdamW(model.parameters(), lr=2e-5)
best_val_acc = 0

# ======================
# 🎯 Training Loop
# ======================
for epoch in range(5):  # Adjust epochs as needed
    model.train()
    total_loss = 0
    correct = 0
    total = 0

    print(f"\n🌟 Epoch {epoch+1}")

    for batch in tqdm(train_loader, desc="Training"):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        correct += (predicted == labels).sum().item()
        total += labels.size(0)

    train_acc = correct / total
    avg_loss = total_loss / len(train_loader)
    print(f"✅ Train Loss: {avg_loss:.4f} | Accuracy: {train_acc:.4f}")

    # ======================
    # 🔍 Validation
    # ======================
    model.eval()
    val_correct = 0
    val_total = 0
    with torch.no_grad():
        for batch in val_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)

            outputs = model(input_ids, attention_mask)
            _, predicted = torch.max(outputs, 1)
            val_correct += (predicted == labels).sum().item()
            val_total += labels.size(0)

    val_acc = val_correct / val_total
    print(f"🔎 Val Accuracy: {val_acc:.4f}")

    # ======================
    # 💾 Save Best Model
    # ======================
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save(model.state_dict(), "bert_doc_classifier.pth")
        print("📌 Model saved (best so far)")

print("\n🎉 Training complete.")
