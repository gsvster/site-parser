#!/usr/bin/python
# -*- coding:utf-8 -*-

import sqlite3
import sys
import datetime
import codecs

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

conn = sqlite3.connect('dbname.db')
c = conn.cursor()
c2 = conn.cursor()
c3 = conn.cursor()
c4 = conn.cursor()

print u"<html>" \
      u"<head>" \
      u"<meta charset=\"UTF-8\"/>" \
      u"<link rel=\"stylesheet\" href=\"table.css\">" \
      u"<script src='http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js' type='text/javascript'></script>" \
      u"<script type=\"text/javascript\">" \
      u"$(document).ready(function(){"
print u"  $(\"table#report tr#attrdata\").hide();"
print u"  $(\"table#report tr#titledata\").click(function(){"
print u"    $(this).next(\"table#report tr\").toggle();"
print u"    $(this).find(\".arrow\").toggleClass(\"up\");"
print u"  });"
#print u"  $(\"table#report tr#attrdata\").addClass(\"odd\");"
#print u"  $(\"table#report tr:odd\").addClass(\"odd\");"
#print u"  $(\"table#report tr:not(.odd)\").hide();"
print u"});" \
      u"</script>" \
      u"<style type=\"text/css\">" \
      u"  #report img { float:right;}" \
      u"  #report div.arrow { background:transparent url(jexpand/arrows.png) no-repeat scroll 0px -16px; width:16px; height:16px; display:block;}" \
      u"  #report div.up { background-position:0px 0px;} " \
      u"</style>" \
      u"</head>" \
      u"<body>"
print u"<table id='report'>"
print u"<tr><th>Категорія</th><th>Підкатегорія</th><th>Назва</th><th>Дія</th></tr>"
for row in c.execute("SELECT category_name, subcategory_name, product_name, id FROM products"):
    print u"<tr id='titledata'><td>%s</td><td>%s</td><td>%s</td><td><div class=\"arrow\"></div></td></tr>" % (row[0], row[1], row[2])
    print u"<tr id='attrdata'><td colspan='4'>"
    print u"<table>"
    print u"<tr>"
    print u"<td></td>"
    for row2 in c2.execute("SELECT size_title "
                           "FROM products_data "
                           "WHERE product_id='%s' "
                           "GROUP BY size_title" % row[3]):
        print u"<th>%s</th>" % row2[0]
    print u"</tr>"

    print u"<tr>"
    for row3 in c3.execute("SELECT color_title "
                                "FROM products_data "
                                "WHERE product_id='%s' "
                                "GROUP BY color_title" % row[3]):
        print u"<th>%s</th>" % row3[0]
        for row2 in c2.execute("SELECT size_title "
                               "FROM products_data "
                               "WHERE product_id='%s' "
                               "GROUP BY size_title" % row[3]):
            q = c4.execute("SELECT quantity "
                           "FROM products_data "
                           "WHERE product_id='%s' AND size_title = '%s' AND color_title='%s' " % (row[3],row2[0],row3[0]))
            quantity = q.fetchone()
            if quantity:
                print u"<td style=\"text-align:center;\">%s</td>" % quantity
            else:
                print u"<td>-</td>"
        print u"</tr>"

    print u"</table>"

    print u"</td></tr>"

print u"</table></body>"
print u"Generated: %s" % str(datetime.datetime.now())
print u"</html>"

conn.close()