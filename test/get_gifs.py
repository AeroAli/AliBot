import csv
from os import listdir, mkdir
from os.path import isfile, join, abspath, dirname
import json

keeps = "test/keep"
froops = "test/hugbox.csv"
out_f = "test/extract_me.csv"
# teetels = ["id","category_name","image_url"]
teetels = ["id","category_name","image_url"]
keeping = [teetels]
tar_dir = "gifs"


with open(keeps,"r") as k, open(froops, "r") as f, open(out_f, "w") as o:
    keeper = [line.rstrip() for line in k]
    # csvFile = csv.DictReader(f)
    # for line in csvFile:
    #     if line["id"] in keeper:
    #        keeping.append(line)
    # csv2 = csv.DictWriter(o, fieldnames=teetels)
    # csv2.writeheader()
    # csv2.writerows(keeping)

    csv_reader = csv.reader(f, delimiter=',')
    line_count = 1
    for row in csv_reader:
        if row[0] in keeper:
            row_mut = row[1:]
            row_mut.insert(0, line_count)
            keeping.append(row_mut)
            line_count += 1
    [print(line) for line in keeping]
    # [o.write(line) for line in keeping]
    
    # csv_writer = csv.writer(o, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # [csv_writer.writerow(line) for line in keeping]


for file in listdir(tar_dir):
    F = join(tar_dir, file)
    if isfile(F) and "csv" not in file:
        with open(F, "r") as f:
            lines = f.read().splitlines()
            print(file)
            for line in lines:
                print(f"{line_count}, {file}, {line}")
                k = [line_count, file, line]
                line_count += 1
                keeping.append(k)
                
with open(out_f, "w") as o:
    csv_writer = csv.writer(o, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    [csv_writer.writerow(line) for line in keeping]
