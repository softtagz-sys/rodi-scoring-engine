import spacy
from transformers import AutoTokenizer, AutoModel
import phunspell
from app.config import settings

nlp = spacy.load(settings.SPACY_MODEL)
tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
bertje_model = AutoModel.from_pretrained(settings.MODEL_NAME)
spell_checker = phunspell.Phunspell(settings.HUNSPELL_DICTIONARY)
