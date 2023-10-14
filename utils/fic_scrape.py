import asyncio
import json
import traceback
from datetime import datetime

import aiofiles
import aiohttp as aiohttp
import bs4.element
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter


# Create shorthand method for conversion
def md(soup: BeautifulSoup, **options: dict):
    return MarkdownConverter(**options).convert_soup(soup)

def get_link(links: list, meta_dict: dict, key: str):
    if links is not None:
        for link in links:
            # print(link)
            if "book" in link.get("href"):
                fic_link = link.get("href").split("bookmarks")[0]
                if fic_link is not None:
                    meta_dict[key] = fic_link


async def download_fic(soup: BeautifulSoup, session: aiohttp.ClientSession, fic_id: str):
    halp = soup.find("li", {"class": "download"}).find_all("li")
    for li in halp:
        if "PDF" in li.text:
            url = "https://archiveofourown.org" + li.find("a").get("href")
            async with session.get(url) as resp:
                content = await resp.read()
                async with aiofiles.open(f"../pdf/{fic_id}.pdf", "wb") as f:
                    await f.write(content)


async def get_meta_fic(soup: BeautifulSoup, meta_dict: dict, session: aiohttp.ClientSession, fic_id):
    # main main_div
    main_div = soup.find("div", {"class": "wrapper", "id": "outer"})

    if soup.find("dt", {"class": "series"}) is not None:
        meta_dict["series"] = series_info(soup)

    # meta data
    main_meta_block = main_div.find("dl", {"class": "work meta group"})

    if main_meta_block is None:
        # print(soup.find("div",{"id":"inner","class":"wrapper"}))
        li = soup.find("div",{"id":"inner","class":"wrapper"}).find("ul",{"class":"actions", "role":"navigation"}).find("li")
        if "continue" in li.text.lower().strip():
            url = "https://archiveofourown.org" + li.find("a").get("href")
            await scrape(url, meta_dict, session, 0)
    elif main_meta_block is not None:
        meta_block = main_meta_block.find("dl")
        if meta_block is not None:
            links = meta_block.find_all("a")
            get_link(links, meta_dict, "fic link")
        tags_block = main_meta_block.find_all("dd")
        author_block = main_div.find("h3", {"class": "byline heading"})

        # meta_dict["rating"]

        meta_dict["authors"] = {}
        meta_dict["authors"] = authors(meta_dict["authors"], author_block)
        if len(author_block) == 0:
            meta_dict["authors"] = {0: {"author_name": "Anonymous",
                                        "author_link": "https://archiveofourown.org/collections/anonymous/profile"}}
        # print(meta_dict["authors"])

        fic_title = main_div.find("h2", {"class": "title heading"})  # fic title
        meta_dict["title"] = fic_title.text.strip()
        summary(meta_dict, main_div)

        class_list = []

        meta(meta_dict, meta_block, class_list)
        tags(meta_dict, tags_block, class_list)

        meta_dict["fic id"] = fic_id
        # await download_fic(soup, session, fic_id)
        # print(json.dumps(meta_dict, indent=4))
        print("meta acquired fic:", meta_dict["fic link"], meta_dict["title"])



def authors(author_dict: dict, author_block: bs4.element.Tag):
    # author info
    if author_block is not None:
        kount = 0
        all_authors = author_block.find_all("a", {"rel": "author"})
        for author in all_authors:
            author_dict[kount] = {}
            author_link = author.get("href")
            author_name = author.text
            if "users" in author_link:
                author_dict[kount]["author_name"] = author_name
                author_dict[kount]["author_link"] = author_link
            kount += 1
    return author_dict


def meta(meta_dict: dict, meta_block: bs4.element.Tag, class_list: list):
    kids = meta_block.find_all("dd")
    weans = meta_block.find_all("dt")
    for kid, wean in zip(kids, weans):
        class_list.append(kid['class'][0])
        # print(kid["class"][0],kid.text, wean.text, wean["class"][0])
        if kid['class'][0] != "status":
            # print([kid['class'][0]], kid.text)
            key = kid['class'][0]
        else:
            # print(wean.text.strip(":").lower(), kid.text)
            key = wean.text.strip(":").lower()
        meta_dict[key] = kid.text



def tags(meta_dict: dict, tags_block: bs4.element.ResultSet, class_list: list):
    for tag in tags_block:
        if tag.has_attr("class") and tag["class"][0] not in class_list and tag["class"][0] != "stats" and tag["class"][0] != "series":
            kid_text = []
            for kid in tag.find_all("a"):
                kid_text.append(kid.text)
            meta_dict[f"{tag['class'][0]}"] = kid_text
            if tag["class"][0] == "language":
                meta_dict[f"{tag['class'][0]}"] = tag.text.strip()


def summary(meta_dict: dict, main_div: bs4.element.Tag):
    summary_var = main_div.find("div", {"class": "summary module"}).find_all("p")
    if summary_var is not None:
        summary_text = "\n\n".join((md(para) if "<br" in str(para) else para.text) for para in summary_var)
        meta_dict["Summary"] = summary_text
        meta_dict["summary length"] = len(summary_text)
    else:
        meta_dict["Summary"] = ""
        meta_dict["summary length"] = 0


def series_info(soup: BeautifulSoup):
    series_dict = []
    series = soup.find("dd", {"class": "series"})
    # print(series)
    series = series.find_all("span", {"class": "series"})
    # print(series)
    for s in series:
        # print(s)
        print(s.find("span", {"class":"position"}))
        s = s.find("span", {"class":"position"})
        print(s.text.replace(f"{s.find('a').text}",""),s.find("a").text, s.find("a").get("href"))
        sub_series = {"part":s.text.replace(f"{s.find('a').text}",""),"title":s.find("a").text,"link": s.find("a").get("href")}
        # print(json.dumps(sub_series, indent=4))
        series_dict.append(sub_series)
    # for s in series:
    #     print(s)
    #     # sub_series = {"part": s.find("span", {"class": "position"}).text, "title": s.find("a").text,
    #     #               "link": s.find("a").get("href")}
    #     # series_dict.append(sub_series)
    print(json.dumps(series_dict, indent=4))
    return series_dict


def get_meta_series(soup: BeautifulSoup, meta_dict: dict):
    # main div
    main_div = soup.find("div", {"class": "wrapper", "id": "outer"})
    series_title = main_div.find("h2").text.strip()
    meta_dict["series title"] = series_title

    series_meta = main_div.find("dl", {"class": "series meta group"})
    if series_meta is not None:
        children_dd = series_meta.find_all("dd")
        children_dt = series_meta.find_all("dt")
        k = 0
        for i in children_dd:
            meta_dict[children_dt[k].text.lower().strip(":")] = i.text
            k += 1
        links = series_meta.find_all("a")
        if links is not None:
            get_link(links, meta_dict, "series link")
        # Series Summary
        series_summary = series_meta.find("blockquote")
        if series_summary is not None:
            series_summary = series_summary.find_all("p")
            series_summary = "\n\n".join([md(child) if "<br" in str(child) else child.text for child in series_summary])

            meta_dict["series summary"] = series_summary
            meta_dict["summary length"] = len(series_summary)
        else:
            meta_dict["series summary"] = ""
            meta_dict["summary length"] = 0

        # series authors
        heading1 = main_div.find("dl", {"class": "series meta group"})
        authors_block = heading1.find_all("a", {"rel": "author"})
        # print(authors_block, len(authors_block))

        if len(authors_block) > 0:
            meta_dict["authors"] = {}
            meta_dict["authors"] = series_authors(meta_dict["authors"], authors_block)
        else:
            meta_dict["authors"] = {0:{"author_name": "Anonymous","author_link": "https://archiveofourown.org/collections/anonymous/profile"}}

        # series fics
        fics = main_div.find("ul", {"class": "series work index group"}).find_all("li", {"role": "article"})
        meta_dict["fics"] = []
        get_series_fic_meta(fics, meta_dict)

        # print(json.dumps(meta_dict, indent=4))  # print("meta acquired")
        print("meta acquired series", meta_dict["series link"], meta_dict["series title"])


def series_authors(authors_dict, authors_block):
    kount = 0
    for author in authors_block:
        authors_dict[kount] = {}
        author_link = author.get("href")
        author_name = author.text
        if "users" in author_link:
            authors_dict[kount]["author_name"] = author_name
            authors_dict[kount]["author_link"] = author_link
            kount += 1
    return authors_dict


def get_series_fic_meta(fics: bs4.element.ResultSet, meta_dict: dict):
    for fic in fics:
        fic_meta = {}

        num = fic.find("ul", {"class": "series"}).find("li").find("strong").text
        fic_meta[num] = {}

        fic_meta[num]["soup"] = str(fic)

        heading = fic.find("div", {"class": "header module"})
        if heading is not None:
            link = heading.find("a").get("href")
            title = heading.find("a").text
            if "works" in link:
                fic_meta[num]["title"] = title
                fic_meta[num]["link"] = link

            authors = heading.find_all("a", {"rel": "author"})
            fic_meta[num]["authors"] = {}
            count = 0
            for author in authors:
                fic_meta[num]["authors"][count] = {}
                author_link = author.get("href")
                author_name = author.text
                if "users" in author_link:
                    fic_meta[num]["authors"][count]["author_name"] = author_name
                    fic_meta[num]["authors"][count]["author_link"] = author_link
                    count += 1

        chapters = fic.find("dd", {"class": "chapters"})
        if chapters is not None:
            fic_meta[num]["chapters"] = chapters.text
            if str(fic_meta[num]["chapters"]).split("/")[0] == str(fic_meta[num]["chapters"]).split("/")[1]:
                fic_meta[num]["complete"] = "Yes"
            else:
                fic_meta[num]["complete"] = "No"

        fic_summary = fic.find_all("blockquote", {"class": "userstuff summary"})
        if fic_summary is not None:
            fic_summary = "\n\n".join([md(child) if "<br" in str(child) else child.text for child in fic_summary])
            fic_meta[num]["fic summary"] = fic_summary
            fic_meta[num]["fic summary len"] = len(fic_summary)
            # print(fic_summary)
        else:
            fic_meta[num]["fic summary"] = ""
            fic_meta[num]["fic summary len"] = 0

        fandoms = fic.find("h5", {"class": "fandoms heading"})
        if fandoms is not None:
            fic_fandoms = [fandom.text for fandom in fandoms.find_all("a")]
            if len(fic_fandoms) > 0:
                fic_meta[num]["fic fandoms"] = fic_fandoms

        # all tags - warnings, relationships, characters, freeform
        tags = fic.find("ul", {"class": "tags commas"}).find_all("li")
        for tag in tags:
            if tag.has_attr("class"):
                if tag["class"][0] not in fic_meta[num].keys():
                    fic_meta[num][tag["class"][0]] = [tag.text]
                else:
                    fic_meta[num][tag["class"][0]].append(tag.text)

        if len(fic_meta) > 0:
            meta_dict["fics"].append(fic_meta)


async def get_fics(soup: BeautifulSoup, meta_dict: dict, session: aiohttp.ClientSession, slep_len: int, url: str):
    meta_dict[str(url)] = []
    fic_list = soup.find("ol", {"class": "work index group"})
    fics = fic_list.find_all("li", {"role": "article"})
    a = 0
    for fic in fics:
        # print(fic.find("h4", {"class": "heading"}).find("a"))
        # print("aye")
        fic_dict = {"authors": []}
        main_info = fic.find("h4", {"class": "heading"}).find_all("a")
        for link in main_info:
            if "/works/" in link.get("href"):
                fic_dict["title"] = link.text
                fic_dict["fic link"] = link.get("href")
            if "/users/" in link.get("href"):
                author_info = {"link": link.get("href"), "author": link.text}
                fic_dict["authors"].append(author_info)
        summary = fic.find("blockquote", {"class": "userstuff summary"}).find_all("p")
        if summary is not None:
            summary_text = "\n\n".join((md(para) if "<br" in str(para) else para.text) for para in summary)
            fic_dict["Summary"] = summary_text
            print(summary_text)
        else:
            fic_dict["Summary"] = ""
        series_meta = fic.find("dl", {"class": "stats"})
        if series_meta is not None:
            children_dd = series_meta.find_all("dd")
            children_dt = series_meta.find_all("dt")
            k = 0
            for i in children_dd:
                fic_dict[children_dt[k].text.lower().strip(":")] = i.text
                k += 1
        a += 1
        # print(json.dumps(fic_dict, indent=4))
        print(fic_dict["fic link"])
        meta_dict[str(url)].append(fic_dict)
    # print(a)
    next_link = soup.find("ol", {"class": "pagination actions", "role": "navigation", "title": "pagination"})
    if next_link is not None or next_link:
        next_link = next_link.find("a", {"rel": "next"}).get("href")
        next_link = "https://archiveofourown.org" + next_link
        try:
            await scrape(next_link, meta_dict, session, slep_len)
        except Exception as E:
            traceback.print_exception(E)


async def scrape(url: str, meta_dict: dict, session: aiohttp.ClientSession, slep_len: int):
    meta_dict[url] = {}
    if "arc" in url.lower():
        fic_id = url.split("/")[-1].split("?")[0]
        print(fic_id)
        try:
            await asyncio.sleep(0.42069)
            async with session.get(url) as resp:
                res = resp.status
                # print(url, str(resp))
                if "login?restricted=true" not in str(resp):
                    # print("not res")
                    if "429" in str(res):
                        if slep_len < int(resp.headers['retry-after']):
                            slep_len = int(resp.headers['retry-after'])
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print(current_time)
                        print(f"\t{url} is sleeping for {int(resp.headers['retry-after'])} seconds")
                        await asyncio.sleep(int(resp.headers["retry-after"]))
                        await scrape(url, meta_dict, session, slep_len)
                    if res == 200:
                        try:
                            html_text = await resp.text()
                            soup = BeautifulSoup(html_text, 'html.parser')
                            if "/works/" in url:
                                await get_meta_fic(soup, meta_dict[url], session, fic_id)
                            if "/series/" in url:
                                get_meta_series(soup, meta_dict[url])
                            if "/tags/" in url or "/works" in url and "/works/" not in url:
                                await get_fics(soup, meta_dict, session, slep_len, url)
                        except Exception as e:
                            await asyncio.sleep(0.5)
                            now = datetime.now()
                            current_time = now.strftime("%H:%M:%S")
                            print("time: ", current_time, "url: ", url, "e: ")
                            traceback.print_exception(e)
                            # hopefully can be yeeted
                            # try:
                            #     html_text = await resp.text()
                            #     soup = BeautifulSoup(html_text, 'html.parser')
                            #     if "/works/" in url:
                            #         await get_meta_fic(soup, meta_dict[url], session, fic_id)
                            #     if "/series/" in url:
                            #         get_meta_series(soup, meta_dict[url])
                            #     if "/tags/" in url or "/works" in url and "/works/" not in url:
                            #         await get_fics(soup, meta_dict, session, slep_len, url)
                            #
                            # except Exception as uh:
                            #     now = datetime.now()
                            #     current_time = now.strftime("%H:%M:%S")
                            #     print("time: ", current_time, "url: ", url, "uh: ")
                            #     traceback.print_exception(uh)
                            #     if "'NoneType' object has no attribute 'find'" in str(uh) and "?view_adult=true" not in str(url):
                            #         # print(uh)
                            #         if "#" not in str(url) and "?" not in str(url):
                            #             # print(url)
                            #             new_url = str(url) + "?view_adult=true"
                            #             await scrape(new_url, meta_dict, session, slep_len)
                            #         elif "#" not in str(url) and "?" in str(url):
                            #             # print(url)
                            #             new_url = str(url).split("?")[0] + "?view_adult=true&" + str(url).split("?")[1]
                            #             await scrape(new_url, meta_dict, session, slep_len)

                    elif "302" in str(res):
                        # print(res)
                        meta_dict[url]["Private"] = "yes"
                        print(meta_dict)
                else:
                    # print("res")
                    meta_dict[url]["Private"] = "yes"
                    print(meta_dict)
        except Exception as err:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("time: ", current_time, "url: ", url, "err: ")
            traceback.print_exception(err)


async def main(fic: str, session: aiohttp.ClientSession):
    meta_dict = {}
    # print(fic)
    slep_len = 0
    await scrape(fic, meta_dict, session, slep_len)
    # print(json.dumps(meta_dict, indent=4))

    return meta_dict


async def run():
    # meta= {}
    # filename = r"D:\theka\Documents\GitHub\TestBot\utils\fic.html"
    # with open(filename, "r", encoding="utf-8") as text:
    #     soup = BeautifulSoup(text, 'html.parser')
    #     await get_meta_series(soup, meta)
    async with aiohttp.ClientSession() as session:
        met_list = []
        fics = [
            "https://archiveofourown.org/series/3422794", "https://archiveofourown.org/series/34897",
            "https://archiveofourown.org/series/1902145", "https://archiveofourown.org/series/31577",
            "https://archiveofourown.org/works/558985",  "https://archiveofourown.org/works/5119898",
            "https://archiveofourown.org/works/705037", "https://archiveofourown.org/works/24540286",
            "https://archiveofourown.org/works/26679994", "https://archiveofourown.org/works/23407009",
            "https://archiveofourown.org/works/28174143",  "https://archiveofourown.org/works/45513865",
            "https://archiveofourown.org/works/32489263", # M
            "https://archiveofourown.org/works/37624642", # Unrated
            "https://archiveofourown.org/works/49527631", # anon fic E
            "https://archiveofourown.org/series/3683536", # anon series E
            "https://archiveofourown.org/works/38372884" # ismenian
        ]
        for fic in fics:
            k = await main(fic, session)
            met_list.append(k)

    # print(json.dumps(met_list, indent=4))

    # async with aiofiles.open("fic_dump.json", "w") as f:
    #     j = json.dumps(met_list, indent=4)
    #     await f.write(j)


if __name__ == "__main__":
    asyncio.run(run())
