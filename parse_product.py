#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import sys
import sqlite3
import codecs
from lxml import etree
from lxml import html as lxml_html

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

colors_dict = {
    "36": u"Белый",
    "37": u"Тёмно-синий",
    "38": u"Солнечно-жёлтый",
    "39": u"Чёрный",
    "40": u"Тёмно-зелёный",
    "41": u"Красный",
    "42": u"Бордовый",
    "43": u"Оранжевый",
    "44": u"Ярко-зелёный",
    "45": u"Ярко-синий",
    "46": u"Светло-розовый",
    "47": u"Малиновый",
    "48": u"Оливковый",
    "49": u"Телесный",
    "50": u"Холодный Синий",
    "51": u"Мокрый асфальт",
    "52": u"Пепельный",
    "53": u"Серо-лиловый",
    "54": u"Хаки",
    "55": u"Глубокий Тёмно-синий",
    "56": u"Кирпично-красный",
    "57": u"Шоколадный",
    "58": u"Светлый Графит",
    "59": u"Жёлтый",
    "60": u"Фиолетовый",
    "61": u"Небесно-голубой",
    "62": u"Ультрамарин",
}

sizes_dict = {
    "34": "XS",
    "26": "S",
    "23": "M",
    "22": "L",
    "24": "XL",
    "25": "XXL",
    "33": "XXXL",
    "108": "4XL",
    "109": "5XL",
    "63": "1-2",
    "64": "2-3",
    "65": "3-4",
    "66": "5-6",
    "67": "7-8",
    "68": "9-11",
    "69": "12-13",
    "70": "14-15",
}

conn = sqlite3.connect('dbname.db')
cursor=conn.cursor()

product = sys.argv[1]

parser = lxml_html.HTMLParser(encoding='utf-8')
tree = etree.parse("shop.biznes.ua/index.php?id_product=%s&controller=product&id_lang=1" % product, parser)

title = tree.findall("//h1")[0].text
price = tree.findall("//span[@id='our_price_display']")[0].text

breadcrumb=tree.findall("//div[@class='breadcrumb']")
cat = breadcrumb[0].getchildren()[2].text
sub_cat = breadcrumb[0].getchildren()[4].text

script=tree.findall("//script")
jsscript = script[24].text

cursor.execute("INSERT INTO products (category_name, subcategory_name, product_name) "
               "VALUES ('%s','%s','%s')" % (cat, sub_cat, title));
conn.commit()
product_last_id = cursor.lastrowid

#print u"id: %s, cat: %s subcat: %s title: %s" % (product_last_id, cat, sub_cat, title)

for color_id, color_title in colors_dict.items():
    for size_id, size_title in sizes_dict.items():
        rx_sequence=re.compile(r"^\t\trunsite_combinations_quantity\[\"%s\_%s\"\]\ =\ (\d+);$" % (color_id, size_id),re.MULTILINE)
        for match in rx_sequence.finditer(jsscript):
            quantity = match.groups()[0]
            #print u"%s %s %s" % (color_title, size_title, quantity)
            conn.execute("INSERT INTO products_data (product_id, color_title, size_title, quantity) "
                         "VALUES ('%s','%s','%s', '%s')" % (product_last_id, color_title, size_title, quantity));
            conn.commit()

conn.close()