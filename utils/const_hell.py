# ToDo: Make pretty and readable

MAIN = """\
# Quick Overview

AO3 has two main filter sections when looking at works
1. "yes I want this shit in my fics"
2. "these tags suck and I don't want them cluttering up the results"

You can filter for:
- Ratings
- Warnings
- Relationship Categories  
- Fandoms
- Characters
- Relationships
- Additional Tags
- Crossover Status
- Completion Status
- Word Count
- Date Updated
- Keywords Within Fic Names, Author Names, Tags, Summary and Work Notes
- Language

For Fandoms, Characters, Relationships and Additional Tags the top 10 tags in each category are displayed. \
Others are available when typed into the `Other Tags` box.
"""

INTRO = """\
# AO3 Introduction

Archive Of Our Own (AO3) is a noncommercial and nonprofit central hosting place for fanworks. 
It is run by the Organization for Transformative Works (OTW). \
The OTW is a fan-run nonprofit dedicated to the preservation of fanworks.
"""

SORTING = """\
# Sorting

Options to sort the results descending by:
- Author
  - Alphabetical by author
- Title
  - Alphabetical by title
- Date Posted
  - Most recently started first
- Date Updated
  - Most recently updated (new chapter, edit, etc)
- Word Count
  - Highest word count first
- Hits
  - Highest read first
- Kudos
  - Highest kudosed fic first 
    - A kudos is equivalent to a like on social media or a favourite on fanfiction.net
- Comments
  - Highest commented fic first
- Bookmarks
  - Highest bookmarked fic first
"""

RATINGS = """\
# Ratings

- **G** (General Audiences)
  - For literally anyone
- **T** (Teen And Up Audiences)
  - Fics more mature than gen but not explicit
- **M** (Mature)
  - For bumping uglies and graphic violence but not as graphic as the Explicit rating
- **E** (Explicit) 
  - Full on bumping uglies and gratuitous murderous violence
- Some fics are also unrated and may contain anything from fluff to genocide
"""

WARNINGS = """\
# Warnings 
 
- Creator Chose Not To Use Archive Warnings
  - Any and all warnings could apply to the fic but the creator has chosen not to tag them
- Major Character Death
  - The content contains the death of a major character.
  - Whether or not a character counts as a major character is up to the creator's discretion.
- Rape/Non-Con
  - Fic contains rape and/or non consensual sexual activity
- Underage
  - The content contains graphic descriptions or depictions of sexual activity by characters under the age of eighteen.
- Graphic Depictions Of Violence
  - The content contains gory, graphic, explicitly described violence.
- No Archive Warnings Apply
  - No warnings apply to the fic
*Note: the default for posting is "Author Chose Not To Use Warnings"*
  """

CATEGORIES = """\
# Categories

- Relationship categories:
  - F/F
   - Female/Female relationships.
  - F/M
    - Female/Male relationships.
  - Gen
    - General: no romantic or sexual relationships, or relationships which aren't the main focus of the work.
  - M/M
    - Male/Male relationships.
  - Multi
    - More than one kind of relationship or a relationship with multiple partners.
  - Other
    - Relationships not covered by the other categories. 
*Note: Fics can be in any combo of categories including none*
"""

FANDOMS = """\
# Fandoms

This is the name of the fandom or fandoms of the results. \
This includes meta fandoms - a meta fandom is the overarching fandom of multiple fandoms eg:
- "Marvel" as the meta fandom for "Avengers", "Black Panther", "Spider-man", etc
- "TOLKIEN J. R. R. - Works & Related Fandoms" for all of J. R. R. Tolkien's works.
"""

CHARACTERS_AND_RELATIONSHIPS = """\
# Characters and Relationships

## Characters

Character tags specify one or more characters who appear in the work.


## Relationships 

Relationship tags specify which characters are involved in a romantic or platonic relationship in the work.
- `&` is for Platonic Relationships
- `/` is for Romantic and/or Sexual Relationships
"""

ADDITIONAL = """\
# Additional Tags

Additional (or freeform) tags cover any details not specified by other categories, \
including any warnings for content not covered by the Archive Warnings. \
Useful additional tags indicate things like genre of the work, \
fandom concepts contained in the work, the community the work was created for, \
when the work takes place in relation to the source material, or fandom-specific locations or concepts. 

*Note: Some creators use the tag "Dead Dove: Do Not Eat" or "DD:DNE" as a warning that this fic is clearly labelled, \
tagged and fully warned for, so if you open it you know what you are getting.
Others use it to say that there is potentially upsetting or distressing content within the fic but are not specifying what \
said content is.
See [Dead Dove: Do Not Eat - Fanlore](https://fanlore.org/wiki/Dead_Dove:_Do_Not_Eat) for more information and history of the tag.
Either way be aware that stories tagged with this are not for those faint of heart.*
"""

OTHER = """\
# Other Tags

You can type a tag into the `any other tags` box and it'll hopefully appear.
It can be filtered in or out that way if it's not in the top 10 they display in the other filtering options. 
"""

CROSSOVER = """\
# Crossovers

Fics can be in multiple fandoms

- Include Crossovers 
- Exclude Crossovers
  - This does not exclude sub fandoms of filtered fandoms
- Show Only Crossovers 

*Note: Default when filtering is Include Crossovers*
"""

COMPLETION = """\
# Completion Status

- All Works
  - Includes both complete and incomplete works
- Complete Works
  - Works marked as complete only
- Works in Progress
  - Works that are not marked as complete 

*Note: Default when filtering is All Works*
"""

WORD_COUNT = """\
# Word Count 

Number range you want your fic length to fall between.
"""

UPDATED = """\
# Date Updated 

Date range the fics were updated in.
"""

SEARCH = """\
# Search Within Results 

Can be used to find or exclude certain key words from fics 
- Hit the `?` for more info on that as they explain it really well ~~or go to the last page of this embed~~
- You can use it to exclude authors
  - See attached for me excluding Matt's fics cause he sucks <a:PatDHehe:954431171247370240>
"""

LANGUAGE = """\
# Language
 
Drop down menu of literally every language on the site.
This is great for finding fics in a particular language.
"""


ANY_FIELD = """\
# Work Search: Any Field

Searches all the fields associated with a work in the database, including summary, notes and tags, but not the full work text.

The characters `:` and `@` have special meanings. Leave them out of your search or you will get unexpected results. 
Like in the Title and Author/Artist field, you can use the following operators to combine your search terms:

- `*`: any characters
 ​ ​ ​ ​ ​ ​ `book*` will find "book" and "books" and "booking".
- ` ` (space): acts like **AND** for search terms in the same field of the work
 ​ ​ ​ ​ ​ ​ `Harry Potter` will find "Harry Potter" and "Harry James Potter" in any field, but it won't find works by a creator named "Harry" with the character tag "Sherman Potter".
- `AND`: searches for works which have both terms in any field
 ​ ​ ​ ​ ​ ​ `Harry AND Potter` will find works by a creator named "Harry" with the character tag "Sherman Potter".
- `||`: **OR** (not exclusive)
 ​ ​ ​ ​ ​ ​ `Harry || Potter` will find "Harry", "Harry Potter", and "Potter".
- `""`: words in exact sequence
 ​ ​ ​ ​ ​ ​ `"Harry Lockhart"` will find "Harry Lockhart" but not "Harry Potter/Gilderoy Lockhart".
- `-`: NOT
 ​ ​ ​ ​ ​ ​ `Harry -Lockhart` will find "Harry Potter" but not "Harry Lockhart" or "Gilderoy Lockhart/Harry Potter".

## Examples

- `"Fandom X" "F/F" -Explicit`
 ​ ​ ​  ​ ​ ​ will return all works from "Fandom X" tagged as "F/F", and exclude those tagged "Explicit"
- `"Character A" OR "Character B" -"Character Death"`
 ​ ​ ​ ​ ​ ​  will return all works including Character A or Character B (or both), and no works tagged with "Character Death" in either the Warnings or the Additional tags
- `"Character A/Character B" Underage Mature OR Explicit`
 ​ ​ ​  ​ ​ ​ will return all works for this pairing that include an Underage warning and are either rated Mature or Explicit
"""