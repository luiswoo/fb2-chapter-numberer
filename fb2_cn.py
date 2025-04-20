import sys
import os
from lxml import etree

def add_numbers_to_titles(input_file):
    # Парсим XML с сохранением пробелов и комментариев
    parser = etree.XMLParser(remove_blank_text=True, strip_cdata=False)
    tree = etree.parse(input_file, parser)
    root = tree.getroot()

    # Находим все заголовки внутри секций в теле книги
    counter = 1
    for title in root.xpath('//fb:body//fb:section/fb:title', 
                            namespaces={'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'}):
        # Ищем первый тег <p> внутри <title>
        p_tag = title.find('.//fb:p', namespaces={'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'})
        if p_tag is not None and p_tag.text:
            p_tag.text = f"{counter:02d}. {p_tag.text}"
            counter += 1

    # Сохраняем результат
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_numbered{ext}"
    tree.write(output_file, 
              encoding='utf-8', 
              xml_declaration=True, 
              pretty_print=True)
    print(f"Файл сохранен как: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python fb2_cn.py <путь_к_fb2_файлу>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    
    if not os.path.exists(input_path):
        print(f"Ошибка: файл '{input_path}' не найден")
        sys.exit(1)
    
    add_numbers_to_titles(input_path)