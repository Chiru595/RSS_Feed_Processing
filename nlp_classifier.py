# nlp_classifier.py
import spacy

nlp = spacy.load("en_core_web_sm")

def classify_article(text):
    doc = nlp(text)
    # Basic keyword matching for classification
    if 'terrorism' in doc.text or 'protest' in doc.text or 'riot' in doc.text:
        return 'Terrorism / protest / political unrest / riot'
    elif 'disaster' in doc.text or 'earthquake' in doc.text:
        return 'Natural Disasters'
    elif 'happy' in doc.text or 'uplifting' in doc.text:
        return 'Positive/Uplifting'
    else:
        return 'Others'
