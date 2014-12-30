#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from lxml import etree
from lxml import html as lxml_html

cat = sys.argv[1]

parser = lxml_html.HTMLParser(encoding='utf-8')
tree = etree.parse("shop.biznes.ua/index.php?id_category=%s&controller=category&id_lang=1" % cat, parser)
ul_product_list = tree.findall("//ul[@id='product_list']/li")

for elem in ul_product_list:
     ul_children = elem.getchildren()[1]
     div_children = ul_children.getchildren()[0]
     #print div_children.tag, div_children.attrib
     print div_children.attrib['href']
