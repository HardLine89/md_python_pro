import re
import bleach
import mistune
from django import template

register = template.Library()


@register.filter(name="strip_links")
def strip_tags_and_nbsp(value):
    """
    Удаляет HTML, Markdown-теги и заменяет &nbsp; на пробелы.
    """
    if not value:
        return ""

    # Удаление HTML-тегов
    clean_value = bleach.clean(value, tags=[], strip=True)

    # Парсинг Markdown в AST
    markdown_renderer = mistune.create_markdown(renderer="ast")
    parsed_markdown = markdown_renderer(clean_value)

    # Функция для извлечения текста из AST
    def extract_text(ast_nodes):
        text = []
        for node in ast_nodes:
            if node["type"] == "text":
                text.append(node["raw"])
            elif "children" in node:
                text.append(extract_text(node["children"]))
        return " ".join(text)

    clean_text = extract_text(parsed_markdown)

    # Убираем символы Markdown (_ * ~ `)
    clean_text = re.sub(r"[_*~`]", "", clean_text)

    # Замена &nbsp; на пробел
    return clean_text.replace("&nbsp;", " ")
