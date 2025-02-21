import string
import torch
from app.dependencies import nlp, tokenizer, bertje_model, spell_checker

def lemmatize(text):
    return " ".join([token.lemma_ for token in nlp(text)])

def correct_spelling(text):
    tokens = text.translate(str.maketrans('', '', string.punctuation)).split()
    corrected_tokens = []
    spelling_mistakes = {}

    for word in tokens:
        if not spell_checker.lookup(word):
            suggestion = spell_checker.suggest(word)[0] if spell_checker.suggest(word) else word
            spelling_mistakes[word] = suggestion
            corrected_tokens.append(suggestion)
        else:
            corrected_tokens.append(word)

    return " ".join(corrected_tokens), spelling_mistakes

def semantic_similarity(model_text, student_text):
    inputs_model = tokenizer(model_text, return_tensors="pt", padding=True, truncation=True)
    inputs_student = tokenizer(student_text, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        model_emb = bertje_model(**inputs_model).last_hidden_state.mean(dim=1)
        student_emb = bertje_model(**inputs_student).last_hidden_state.mean(dim=1)

    return torch.nn.functional.cosine_similarity(model_emb, student_emb).item()

def score_answer(model_answer, student_answer, keywords, spellcheck_enabled):
    if not model_answer or not student_answer:
        raise ValueError("Empty answers not allowed")

    lemmatized_model = lemmatize(model_answer)
    lemmatized_student = lemmatize(student_answer)

    # Apply spell checking if enabled
    if spellcheck_enabled:
        corrected_student, spelling_mistakes = correct_spelling(lemmatized_student)
    else:
        corrected_student = lemmatized_student
        spelling_mistakes = {}

    # Calculate keyword score and track correct and incorrect keywords
    correct_keywords = [word for word in keywords if word in corrected_student]
    incorrect_keywords = [word for word in keywords if word not in corrected_student]
    keyword_score = len(correct_keywords) / len(keywords) if keywords else 0

    # Calculate semantic similarity score
    similarity_score = semantic_similarity(lemmatized_model, corrected_student)

    # Calculate spelling accuracy (if enabled)
    total_words = len(lemmatized_student.split())
    misspelled_words = len(spelling_mistakes)
    spelling_accuracy = (total_words - misspelled_words) / total_words if total_words > 0 else 1

    # Weighted final score
    final_score = (
        0.6 * keyword_score +
        0.3 * similarity_score +
        (0.1 * spelling_accuracy if spellcheck_enabled else 0)
    )

    return {
        "final_score": final_score,
        "keyword_score": keyword_score,
        "similarity_score": similarity_score,
        "spelling_accuracy": spelling_accuracy if spellcheck_enabled else None,
        "spelling_mistakes": spelling_mistakes if spellcheck_enabled else None,
        "correct_keywords": correct_keywords,
        "incorrect_keywords": incorrect_keywords
    }