# news/templatetags/custom_filters.py
import re
from django import template
from typing import Any


register = template.Library()


BANNED_WORDS = {
    'редиска',
    'дурачок',
    'бяка',
    'негодяй',
    'злюка'
}

WORD_PATTERN= re.compile(r'\b[а-яА-Яa-zA-Z][а-яa-z]*\b')

@register.filter
def censor(value:Any) -> str:
    """
    Фильтр для цензурирования запрещённых слов в строке.
    Применяется только к строкам. Иначе — ошибка.
    """
    if not isinstance(value,str):
        raise TypeError(f"Фильтр 'censor' применим только к строкам")

    def replace_match(match):
        word = match.group()
        lower_word =  word.lower()
        if lower_word in BANNED_WORDS:
            return word[0] + '*' * (len(word) - 1)
        return word
    return WORD_PATTERN.sub(replace_match, value)