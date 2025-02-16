from django import template
import re

register = template.Library()


@register.filter(name="strip_links")
def strip_tags_and_nbsp(value):
    """
    Удаляет HTML-теги и заменяет &nbsp; на пробелы.
    """
    # Удаление HTML-тегов
    clean_value = re.sub(r"<.*?>", "", value)
    # Замена символов &nbsp; на пробел
    clean_value = clean_value.replace("&nbsp;", " ")
    return clean_value
