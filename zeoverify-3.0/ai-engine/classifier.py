def detect_doc_type(text):
    keywords = ["sale deed", "plot no", "stamp duty", "sub-registrar", "property"]
    count = sum(1 for k in keywords if k in text.lower())
    if count >= 2:
        return "real_estate"
    else:
        return "invalid"

