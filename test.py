import random
from os import listdir
from os.path import isfile, join, abspath, dirname

# gif = random.choice([x for x in open(
#     f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y) and 'gifs' in y)])}"
# ).read().splitlines()])
# gif = random.choice([x for x in open(
#     f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y) and 'gifs' in y)])}"
# ).read().splitlines()])
# print(gif)

# for i in range(20):
#     print("\nSK")
#     quote = random.choice([x for x in open(
#         f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y)) and 'quotes' in y])}"
#     ).read().splitlines()]).split("\n")[0]
#     if "\\n" in quote:
#         quote = quote.replace("\\n", "\n")
#     print(quote)
#
#     quote = random.choice([x for x in open(
#         f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y)) and 'quotes' in y])}"
#     ).read().splitlines()])
#     if "\\n" in quote:
#         quote = quote.replace("\\n", "\n")
#     print(quote)
#
#     quote = random.choice([x for x in open(
#         f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y))])}"
#     ).read().splitlines()])
#     if "\\n" in quote:
#         quote = quote.replace("\\n", "\n")
#     print(quote)
#
# gif = random.choice([x for x in open(
#         f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y) and 'gifs' in y)])}"
# ).read().splitlines()])

gifs = []
quotes = []
dir = f"{abspath(dirname(__file__))}/starkids"
for file in listdir(dir):
    if isfile(join(dir, file)):
        if "gif" in file:
            gifs.append(join(dir, file))
        if "quote" in file:
            quotes.append(join(dir, file))

with open(random.choice(gifs), "r") as f:
    gif = f.read().splitlines()

with open(random.choice(quotes), "r") as f:
    quote = f.read().splitlines()

print(random.choice(gif))
print(random.choice(quote))
