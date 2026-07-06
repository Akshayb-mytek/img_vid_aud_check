from transformers import pipeline

classifier = pipeline("text-classification")

def analyze_text(text):
    result = classifier(text[:512])[0]

    if "toxic" in result["label"].lower():
        return "toxic"
    return "clean"
