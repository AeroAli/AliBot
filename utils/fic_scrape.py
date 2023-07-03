import asyncio
import aiofiles
import aiocsv
import csv
import json
import os
import time
from datetime import datetime

import aiohttp as aiohttp
from bs4 import BeautifulSoup


async def get_meta(soup, meta_dict):
    # main div
    div = soup.find("div", {"class": "wrapper", "id": "outer"})

    # meta data
    dl = div.findChild("dl", {"class": "work meta group"})
    meta = dl.findChild("dl")

    summary = div.findChild("div", {"class": "summary module"}).findChild("p").text

    # author info
    h3 = div.findChild("h3", {"class": "byline heading"})
    link = h3.findChild("a")

    dd = dl.findChildren("dd")  # tags

    h2 = div.findChild("h2", {"class": "title heading"})  # fic title

    meta_dict["title"] = h2.text.strip()
    meta_dict["Author"] = link.text
    meta_dict["Author Link"] = link.get("href")
    meta_dict["Summary"] = summary

    class_list = []
    for child in meta.findChildren():
        try:
            if child["class"][0]:
                if str(child["class"][0]) not in class_list:
                    class_list.append(str(child["class"][0]))
                    # print(child["class"][0])
                else:
                    meta_dict[f"{child['class'][0]}"] = child.text
                    # print(child["class"][0], "\t", child.text)
        except Exception as err:
            # print(child)
            # print(err)
            meta_dict[f"bookmarks"] = child.text
            continue

    for tag in dd:
        # print(child.text)
        if tag.has_attr("class") and tag["class"][0] not in class_list and tag["class"][0] != "stats":
            kid_text = []
            for kid in tag.findChildren("a"):
                # print(kid["class"][0])
                if kid.text != "Next Work →" and kid.text != "← Previous Work":
                    # print(f"\t{kid.text}")
                    if "tag" not in kid.get("href"):
                        kid_text.append([kid.text, kid.get("href")])
                    else:
                        kid_text.append(kid.text)
            meta_dict[f"{tag['class'][0]}"] = kid_text
            if tag["class"][0] == "language":
                # print("\t",tag.text.strip())
                meta_dict[f"{tag['class'][0]}"] = tag.text.strip()

    # print(meta_dict)
    # print("meta acquired")


async def scrape(url, meta_dict):
    meta_dict[url] = {}
    meta = meta_dict[url]
    async with aiohttp.ClientSession() as session:
        if "arc" in url and "/works/" in url:
            try:
                # print("awaiting soup ", url_num)
                await asyncio.sleep(0.42069)
                async with session.get(url) as resp:
                    res = resp.status
                    if "login?restricted=true" not in str(resp):
                        if "429" in str(res):
                            print(f"is sleeping for {int(resp.headers['retry-after'])} seconds")
                            await asyncio.sleep(int(resp.headers["retry-after"]))
                            await scrape(url, meta_dict)

                        if "200" in str(res):
                            try:
                                html_text = await resp.text()
                                soup = BeautifulSoup(html_text, 'html.parser')
                                # print("soup acquired")  # , url)
                                await get_meta(soup, meta)
                            except Exception as e:
                                await asyncio.sleep(0.5)
                                now = datetime.now()
                                current_time = now.strftime("%H:%M:%S")
                                print("time: ", current_time, "url: ", url, "err: ", e)
                                try:
                                    x = 10
                                    print(f"sleeping for {x} seconds")
                                    await asyncio.sleep(x)
                                    html_text = await resp.text()
                                    soup = BeautifulSoup(html_text, 'html.parser')
                                    # print("soup acquired", url)
                                    await get_meta(soup, meta)
                                except Exception as uh:
                                    print("time: ", current_time, "url: ", url, "err: ", uh)
                                    # print(err_dict)
                                    if str(uh) == "'NoneType' object has no attribute 'findChild'" and "?view_adult=true" not in str(
                                            url):
                                        if "#" not in str(url) and "?" not in str(url):
                                            url = str(url) + "?view_adult=true"
                                        elif "#" not in str(url) and "?" in str(url):
                                            url = str(url).split("?")[0] + "?view_adult=true&"
                                        await scrape(url, meta_dict)

                    else:
                        meta["Private"] = "yes"
            except Exception as err:
                # print(err, url)
                try:
                    x = 10
                    print(f"sleeping for {x} seconds")
                    await asyncio.sleep(x)
                    await scrape(url, meta_dict)
                except Exception as er:
                    print(er, url)


async def main(fic):
    start_time = time.time()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    async with aiofiles.open("time.txt", "a") as t:
        await t.write(f"\n{now}, ")
    print(now)
    tasks = []
    print("getting fics")
    timings = {
        "start unix time": start_time,
        "start time": current_time
    }
    stuff = {
        "meta_list": [],
        "res_list": [],
        "url_dict": {}
    }

    url_num = 0


    j = fic.split("csv")
    outfile = j[0] + "json" + j[1].split("ao3")[0] + "meta.json"

    fandom = j[1].split("ao3")[0].split("\\")[-2]
    meta = []
    # print('open is assigned to %r' % open)
    if "\\" in fandom:
        metafandom = fandom.split("\\")[0]
        fandom = fandom.split("\\")[1]
        fandoms = {metafandom: fandom}
    else:
        fandoms = {fandom: ""}

    stuff["url_dict"][url_num] = [fandom, str(fic)]
    print(url_num)
    meta_dict = {}
    err_dict = {str(url_num): {}}

    await scrape(fic, meta_dict)

    err_dict[str(url_num)]["url"] = fic
    stuff["meta_list"].append({str(url_num): [{"fandoms": fandoms}, meta_dict]})
    meta.append({str(url_num): meta_dict})

    url_num += + 1

    async with aiofiles.open(outfile, "w") as f:
        j = json.dumps(meta, indent=4)
        await f.write(j)

    print('Saving the output of extracted information')
    await asyncio.gather(*tasks)

    async with aiofiles.open("stuff.json", "w", encoding="utf-8") as f:
        j = json.dumps(stuff, indent=4)
        await f.write(j)

    async with aiofiles.open("final.json", "w", encoding="utf-8") as f:
        j = json.dumps(stuff["meta_list"], indent=4)
        await f.write(j)
    async with aiofiles.open("res.json", "w", encoding="utf-8") as f:
        j = json.dumps(stuff["res_list"], indent=4)
        await f.write(j)

    end_time = time.time()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    time_difference = end_time - start_time
    print(f'Scraping time: {time_difference} seconds.')

    timings["end unix time"] = end_time
    timings["end time"] = current_time
    timings["length"] = time_difference
    async with aiofiles.open("time.txt", "a") as t:
        await t.write(f"{now}, {time_difference}")
    async with aiofiles.open("time.json", "w", encoding="utf-8") as f:
        j = json.dumps(timings, indent=4)
        await f.write(j)


asyncio.run(main(input("URL: ")))
