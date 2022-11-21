# test / gen_json.py

import json
import csv
from os import listdir
from os.path import isfile, join
import random


def gen_csvs():
    target_dir = r"/home/aeroali/AliBot/starkid_dnu"
    files = []

    for file in listdir(target_dir):
        if isfile(join(target_dir, file)) and "test" not in file and "json" not in file and "csv" not in file:
            # print(file)
            files.append(join(target_dir, file))

    # print("Files")
    # [print(x) for x in files]

    # print(len(files))

    for file in files:
        #    # print(file)
        # k = []
        with open(file, "r") as f1:
            
            print(file.split("/")[1:][-1:][0])
            
            file2 = file
            if len(file2.split("_")) > 2:
                file2 = "_".join(file2.split("_", 2)[:2])
            elif len(file2.split("_")) == 2:
                file2 = "".join(file2.split("_")[:1])
            file2 += ".csv"

            rows = []
            print(file2.split("/")[1:][-1:][0])

            with open(file2, "a+") as f2:
                f2.write("gif,quote\n")
                for i in f1.read().splitlines():
                    if "gif" in file:
                        rows.append(f"\"{i}\",​\n")
                    if "quote" in file:
                        rows.append(f"​,\"{i}\"\n")

                for x in rows:
                    # print(x)
                    f2.write(x)
        remove_dups(file2, file2)


def remove_dups(filename, out):
    with open(filename, "r") as f:
        unique = []
        read = f.readlines()
        for item in read:
            if item not in unique:
                unique.append(item)
    with open(out, "w") as f:
        for item in unique:
            f.write(item)


def json_gen():
    star_dir = r"/home/aeroali/AliBot/starkid_dnu"
    files = []

    for file in listdir(star_dir):
        files.append(join(star_dir, file))
    for file in files:
        if isfile(join(star_dir, file)) and "csv" in file:
            json_arr = []
            # print(file)
            file2 = str(file).split(".csv")[0]
            file2 += ".json"
            file2 = file2.replace("starkid_dnu", "starkids")
            # print(file.split("/")[1:][-1:][0])
            # print(file2.split("/")[1:][-1:][0])
            with open(file, "r") as f1, open(file2, "w") as f2:
                csv_r = csv.DictReader(f1)
                for row in csv_r:
                    json_arr.append(row)
                json_str = json.dumps(json_arr, indent=4)
                print(json_str)
                f2.write(json_str)


def json_gifs():
    star_dir = r"/home/aeroali/AliBot/starkid_dnu"
    json_dir = r"/home/aeroali/AliBot/starkids"
    files = []


    for file in listdir(star_dir):
        files.append(join(star_dir, file))
    for file in files:
        if isfile(join(star_dir, file)) and "csv" in file:
            json_arr = []
            # print(file)
            file2 = file.split(".csv")[0]
            file2 += ".json"
            file2 = file2.replace("starkid_dnu", "starkids")
            # print(file.split("/")[1:][-1:][0])
            # print(file2.split("/")[1:][-1:][0])
            with open(file, "r") as f1, open(file2, "w") as f2:
                csv_r = csv.DictReader(f1)
                for row in csv_r:
                    json_arr.append(row)
                json_str = json.dumps(json_arr, indent=4)
                f2.write(json_str)


def json_thanos_blame():
    star_dir = r"/home/aeroali/AliBot/starkids"
    files = []

    for file in listdir(star_dir):
        files.append(join(star_dir, file))
    for file in files:
        if isfile(join(star_dir, file)) and "json" in file and "thanos" not in file:
            print(file)
            file2 = file.split(".")[0] + "_thanos.json"
            with open(file, "r") as f1, open(file2, "w") as f2:
                json_arr = json.load(f1)
                for i in json_arr:
                    # print(i["gif"])
                    if i["gif"] == "​":
                        k = ["https://media.tenor.com/RHqI2d3jobsAAAAC/tgwdlm-lauren-lopez.gif", "https://media.tenor.com/fhKONBs-ln4AAAAd/honor-to-honor.gif"]
                        i["gif"] = random.choice(k)
                    if i["gif"] == "https://media.tenor.com/fhKONBs-ln4AAAAd/honor-to-honor.gif":
                        i["author"] = 158646501696864256
                    else:
                        i["author"] = "​"
                json_str = json.dumps(json_arr, indent=4)
                f2.write(json_str)


def json_thanos_show():
    star_dir = r"/home/aeroali/AliBot/starkids"
    files = []

    for file in listdir(star_dir):
        files.append(join(star_dir, file))
    for file in files:
        if isfile(join(star_dir, file)) and "json" in file and "thanos" in file:
            print(file)
            with open(file, "r") as f1:
                json_arr = json.load(f1)
                for i in json_arr:
                    print(i)


if __name__ == "__main__":
    # gen_csvs()
    json_gen()
    json_thanos_blame()
    # json_thanos_show()

