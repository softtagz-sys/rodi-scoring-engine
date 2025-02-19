import string
import torch
from app.dependencies import nlp, tokenizer, bertje_model, spell_checker

def lemmatize(text):
    return " ".join([token.lemma_ for token in nlp(text)])

def correct_spelling(text):
    tokens = text.translate(str.maketrans('', '', string.punctuation)).split()
    corrected_tokens = [spell_checker.suggest(word)[0] if not spell_checker.lookup(word) else word for word in tokens]
    return " ".join(corrected_tokens)

def semantic_similarity(model_text, student_text):
    inputs_model = tokenizer(model_text, return_tensors="pt", padding=True, truncation=True)
    inputs_student = tokenizer(student_text, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        model_emb = bertje_model(**inputs_model).last_hidden_state.mean(dim=1)
        student_emb = bertje_model(**inputs_student).last_hidden_state.mean(dim=1)

    return torch.nn.functional.cosine_similarity(model_emb, student_emb).item()

def score_answer(model_answer, student_answer, keywords):
    lemmatized_model = lemmatize(model_answer)
    lemmatized_student = lemmatize(student_answer)

    corrected_student = correct_spelling(lemmatized_student)
    keyword_score = sum(1 for word in keywords if word in corrected_student) / len(keywords) if keywords else 0
    similarity_score = semantic_similarity(lemmatized_model, corrected_student)

    final_score = 0.7 * keyword_score + 0.3 * similarity_score
    return final_score
