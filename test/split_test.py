# test / split_test.py 

import csv
import random


with open("gifs/hug_cog.csv", "r") as f:
    # rows = csv.DictReader(f)
    csv_rows = csv.reader(f, delimiter=",")
    
    rows = list(csv_rows)
    print(type(rows))

    baka = [row[2] for row in rows if row[1] == 'baka']
    bite = [row[2] for row in rows if row[1] == 'bite']
    boop = [row[2] for row in rows if row[1] == 'boop']
    cuddle = [row[2] for row in rows if row[1] == 'cuddle']
    hug = [row[2] for row in rows if row[1] == 'hug']
    kill = [row[2] for row in rows if row[1] == 'kill']
    kiss = [row[2] for row in rows if row[1] == 'kiss']
    nohorny = [row[2] for row in rows if row[1] == 'nohorny']
    pat = [row[2] for row in rows if row[1] == 'pat']
    punch = [row[2] for row in rows if row[1] == 'punch']
    sleep = [row[2] for row in rows if row[1] == 'sleep']
    scritch = [row[2] for row in rows if row[1] == 'scritch']
    slap = [row[2] for row in rows if row[1] == 'slap']
    sleep_me = [row[2] for row in rows if row[1] == 'sleep_me' or row[1] == 'sleep']
    nom = [row[2] for row in rows if row[1] == 'nom']
    sleep_u = [row[2] for row in rows if row[1] == 'sleep_u' or row[1] == 'sleep']
    tackle = [row[2] for row in rows if row[1] == 'tackle']
    squish = [row[2] for row in rows if row[1] == 'squish']
    favs = [row[2] for row in rows if row[1] == 'favs']
    rhea = [row[2] for row in rows if row[1] == 'rhea']


print(baka)
print(bite)
print(boop)
print(cuddle)
print(hug)
print(kill)
print(kiss)
print(nohorny)
print(pat)
print(punch)
print(sleep)
print(scritch)
print(slap)
print(sleep_me)
print(nom)
print(sleep_u)
print(tackle)
print(squish)
print(favs)
print(rhea)


# print(random.choice(baka))
# print(random.choice(bite))
# print(random.choice(boop))
# print(random.choice(cuddle))
# print(random.choice(hug))
# print(random.choice(kill))
# print(random.choice(kiss))
# print(random.choice(nohorny))
# print(random.choice(pat))
# print(random.choice(punch))
# print(random.choice(sleep))
# print(random.choice(scritch))
# print(random.choice(slap))
# print(random.choice(sleep_me))
# print(random.choice(nom))
# print(random.choice(sleep_u))
# print(random.choice(tackle))
# print(random.choice(squish))
# print(random.choice(favs))
# print(random.choice(rhea))
