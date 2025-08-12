# ML Model Files

## Important Note
The large ML model files are not included in this repository due to GitHub's file size limits. You need to download them separately to use the ML classification features.

## Required Files
The following files need to be downloaded and placed in the `saved_model/` directory:

1. **model.safetensors** (255MB) - The trained transformer model
2. **label_encoder.pkl** - Label encoder for classification
3. **embedder.pkl** (87MB) - Text embedding model
4. **vectorizer.pkl** - Text vectorizer

## Download Instructions

### Option 1: Download from Cloud Storage
If you have access to the cloud storage where these files are hosted, download them and place them in the `saved_model/` directory.

### Option 2: Train Your Own Model
You can train your own model using the training scripts in the `ml_model/` directory:

```bash
cd zeoverify-3.0/ai-engine/ml_model
python train.py
```

### Option 3: Use Rule-Based Classification
If you don't have the ML model files, the system will automatically fall back to rule-based classification, which still provides good results for document verification.

## File Structure
After downloading, your `saved_model/` directory should look like this:

```
saved_model/
├── config.json
├── model.safetensors          # Download required
├── tokenizer.json
├── vocab.txt
├── label_encoder.pkl          # Download required
├── embedder.pkl              # Download required
└── vectorizer.pkl            # Download required
```

## Verification
To verify that the ML model is working:

1. Start the API server
2. Check the logs for "✅ ML model loaded successfully"
3. Upload a document to test classification

If you see "⚠️ ML model not found, using rule-based classification", it means the model files are missing and the system is using the fallback method.
