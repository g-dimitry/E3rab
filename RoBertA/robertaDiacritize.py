from transformers import pipeline
from transformers import RobertaTokenizerFast
from utils import diacritize


arabic_letters = ['أ', 'ة', 'إ', 'ؤ', 'آ', 'ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز',
                  'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي', 'ئ', 'ئ', 'ء']
arabic_diac = ["َ", "ً", "ِ", "ٍ", "ُ", "ٌ", "ْ", "َّ", "ِّ", "ُّ"]


def robertaDiacritize(pathToModel: str, original: str) -> str:
    roberta_tokenizer = RobertaTokenizerFast.from_pretrained(pathToModel)

    # Adding the tokens by hand
    roberta_tokenizer.add_tokens(arabic_diac)
    roberta_tokenizer.add_tokens(" ")
    roberta_tokenizer.add_tokens(arabic_letters)

    fill_mask = pipeline(
        "fill-mask",
        model=pathToModel,
        tokenizer=roberta_tokenizer
    )
    prediction = diacritize(original, fill_mask, passes=3, isDataset=False)
    return prediction
