import random
from os import listdir, mkdir
from os.path import isfile, join, abspath, dirname
import json
import csv

#gif = random.choice([x for x in open(
#    f"starkid_dnu/{random.choice([y for y in listdir('starkid_dnu') if isfile(join('starkid_dnu', y)) and 'json' not in y and 'csv' not in y])}"
#).read().splitlines() if x != ""])
# gif=random.choice([y for y in listdir('starkid_dnu') ])#if isfile(join('starkid_dnu', y)) and 'json' not in y])
#if "\\n" in gif:
#    gif = gif.replace("\\n", "\n")
#print(gif)
#
# for i in range(20):
#     print("\nSK")
#     quote = random.choice([x for x in open(
#         f"starkid_dnu/{random.choice([y for y in listdir('starkid_dnu') if isfile(join('starkid_dnu', y)) and 'quotes' in y])}"
#     ).read().splitlines()]).split("\n")[0]
#     if "\\n" in quote:
#         quote = quote.replace("\\n", "\n")
#     print(quote)
#
#     quote = random.choice([x for x in open(
#         f"starkid_dnu/{random.choice([y for y in listdir('starkid_dnu') if isfile(join('starkid_dnu', y)) and 'quotes' in y])}"
#     ).read().splitlines()])
#     if "\\n" in quote:
#         quote = quote.replace("\\n", "\n")
#     print(quote)
#
#     quote = random.choice([x for x in open(
#         f"starkid_dnu/{random.choice([y for y in listdir('starkid_dnu') if isfile(join('starkid_dnu', y))])}"
#     ).read().splitlines()])
#     if "\\n" in quote:
#         quote = quote.replace("\\n", "\n")
#     print(quote)

# gifs = []
# quotes = []
# dir = f"{abspath(dirname(__file__))}/starkid_dnu"
# for file in listdir(dir):
#     if isfile(join(dir, file)):
#         if "gif" in file:
#             gifs.append(join(dir, file))
#         if "quote" in file:
#             quotes.append(join(dir, file))
#
# for file in gifs:
#     with open(file, "r") as f:
#         [print(k) for k in f.read().splitlines()]
#
# for file in quotes:
#     with open(file, "r") as f:
#         [print(k) for k in f.read().splitlines()]

#
# with open(random.choice(gifs), "r") as f:
#     gif = f.read().splitlines()
#
# with open(random.choice(quotes), "r") as f:
#     quote = f.read().splitlines()
#
# print(random.choice(gif))
# print(random.choice(quote))

# with open(f"{abspath(dirname(__file__))}/starkid_dnu/black_friday.json", "r") as f:
#     data = json.load(f)
#     print(type(data))

# [print("y", y) for y in [x for x in [i.keys() for i in data]]]

# for i in data:
#    [print(k) for k in i.keys()]

# print(data[0].keys())
# print(data[0].items())
# print(data[0].values())
# print(data[0]["gif"])

# print(random.choice(data)["quote"])

# for file in listdir(f"{abspath(dirname(__file__))}/starkid_dnu"):
#     print(file)
#
# #def json_gen(file)
#
# string = "||​||||​||"
#
# iter_start = 10
# iter_end = 400
# iter_steps = 10
#
# for i in range(iter_start, iter_end, iter_steps):
#     print(f"{str(i)} {string * i}")

# import shutil
#
# target_dir = "/home/pi/Documents/GitHub/AliBot/starkids"
# new_dir = "/home/pi/Documents/GitHub/AliBot/starkid_dnu"
#
# try:
#     mkdir(new_dir)
# except:
#     print("it exists")
#
# for file in listdir(target_dir):
#     print(file)
#     if "json" not in file and isfile(join(target_dir,file)):
#         shutil.move(join(target_dir, file), join(new_dir,file))
#         print("moved file")

#target_dir = "/home/aeroali/AliBot/gifs"

#for file in listdir(target_dir):
#    print(file)
#    k = open(f"{target_dir}/{file}").read().splitlines()
#    print(k)


# file = random.choice([y for y in listdir('starkids') if isfile(join('starkids', y))])

#star_dir = r"/home/pi/Documents/GitHub/AliBot/starkid_dnu"
#files = []

#for file in listdir(star_dir):
#files.append(join(star_dir, file))
#for file in files:
folder = "home/aeroali/AliBot/test/"
file1 = "tgwdlm.csv"
#if isfile(join(folder,file1)):
#    json_arr = []
    # print(file1)
file2 = str(file1).split(".csv")[0]
file2 += ".json"
#file2 = file2.replace("starkid_dnu", "starkids")
#print(file1.split("/")[1:][-1:][0])
#print(file2.split("/")[1:][-1:][0])
json_arr = []
with open(file1, "r") as f1, open(file2, "w") as f2:
    csv_r = csv.DictReader(f1)
    for row in csv_r:
        json_arr.append(row)
        json_str = json.dumps(json_arr, indent=4)
        #print(json_str)
    f2.write(json_str)





with open(f"tgwdlm.json", "r") as f:
    data = json.load(f)
    for ran in data:
        gif = ran["gif"]
        quote = ran["quote"]
        if "\\n" in quote:
            quote = str(quote).replace("\\n", "\n")
        if len(quote) >= 255:
            var_title = "<200b>"
            var_description = quote
        else:
            var_title = quote
            var_description = None
        print(var_description, gif)

