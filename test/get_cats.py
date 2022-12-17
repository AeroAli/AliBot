# test / get_cats.py

import csv

file = "gifs/hug_cog.csv"

with open(file, "r") as f:
    rows = csv.DictReader(f, delimiter=",")
    cats = []

    for row in rows:
        cat = str(row["category_name"])
        if cat not in cats:
            cats.append(cat)

[print(cat) for cat in cats]




