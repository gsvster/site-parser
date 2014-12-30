#!/bin/bash

declare -a cat_m=(54 55 56 57 58 61 62 88);
declare -a cat_f=(63 65 66 67 68 69);
declare -a cat_b=(76 78 79 80 81);

STRUCTURE1="CREATE TABLE products (id INTEGER PRIMARY KEY, category_name TEXT, subcategory_name TEXT, product_name TEXT);";
STRUCTURE2="CREATE TABLE products_data (id INTEGER PRIMARY KEY, product_id INTEGER, color_title TEXT, size_title TEXT, quantity TEXT, FOREIGN KEY(product_id) REFERENCES products(id));";
cat /dev/null > dbname.db
echo $STRUCTURE1 > /tmp/tmpstructure1
echo $STRUCTURE2 > /tmp/tmpstructure2
sqlite3 dbname.db < /tmp/tmpstructure1;
sqlite3 dbname.db < /tmp/tmpstructure2;
rm -f /tmp/tmpstructure1;
rm -f /tmp/tmpstructure2;

wget --cookies=on \
     --keep-session-cookies \
     --save-cookies cookies.txt \
     --post-data 'email=xxxxxx@gmail.com&passwd=xxxxxx&SubmitLogin=Login' \
     "http://shop.biznes.ua/index.php?controller=authentication"

function parse_category {
    declare -a argAry1=("${!1}")

    for t in "${argAry1[@]}"
    do
        # викачуємо сторінку категорії з переліком товарів
        wget --load-cookies cookies.txt \
             --reject jpg,gif,png,css,ico,js \
             -p "http://shop.biznes.ua/index.php?id_category=$t&controller=category&id_lang=1"

        # отримуємо перелік лінків на товари через пробіл
        products=`./parse_category.py $t`

        # перетворюємо лінки через пробіл у масив
        IN=$products
        arr=$(echo $IN | tr " " "\n")

        for x in $arr
        do
            # викачуємо кожну сторінку з товаром
            wget --load-cookies cookies.txt \
                 --reject jpg,gif,png,css,ico,js \
                 -p "$x" > /dev/null 2>&1

            echo "> [$x]"

            # отримуємо ID товару з лінку на сторінку товару
            id_product=`echo $x | awk -F'[=&]' '{print $2}'`

            # парсимо сторінку товару
            ./parse_product.py $id_product
        done
    done
}

parse_category cat_m[@]
parse_category cat_f[@]
parse_category cat_b[@]

./html_gen.py > /home/drukteua/public_html/postach.html

rm -rf shop.biznes.ua
rm -rf cookies.txt
rm -rf index.php?controller=authentication
