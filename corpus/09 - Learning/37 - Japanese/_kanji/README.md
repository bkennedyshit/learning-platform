---
date: 2026-05-24
title: "Kanji Database — Method Documentation"
tags: [japanese, kanji, database, method-doc]
type: method-doc
status: planning
---

# Kanji Database — Method

This folder is the **vault-native kanji database**. Each `.md` file is a single kanji's master note (filename = the kanji character itself, e.g., `人.md`). Stroke-order SVGs live centrally at `09 - Learning/_svgs/kanji-<strokes>-<kanji>.svg`.

For the full philosophy and chapter outline see [[../Subject_Plan|18 - Japanese Subject Plan §6]].

## Bootstrap workflow (when you're ready)

```bash
cd "18 - Japanese"
python _practice/scripts/bootstrap_kanji_db.py --jlpt N5
# Generates ~100 .md files in _kanji/ + ~100 SVGs in _svgs/
# Pre-fills frontmatter (readings, meaning, JLPT, freq, strokes) from KANJIDIC2
# Pre-fills vocabulary tables from JMdict
# Leaves mnemonic + example sentences as TODO for hand-curation
```

## Frontmatter schema

```yaml
---
kanji: 人                              # the kanji character
jlpt: N5                               # N5 | N4 | N3 | N2 | N1
frequency: 5                           # rank in newspaper-frequency list (1 = most frequent)
strokes: 2                             # stroke count
radicals: [人]                         # one or more radicals
on_yomi: [ジン, ニン]                  # Chinese-derived readings
kun_yomi: [ひと, -り, -と]             # native Japanese readings
meanings: [person, people, human, man] # primary English meanings
tags: [japanese, kanji, jlpt-n5, frequency-top-10]
---
```

## Index files

- `_index_n5.md` — master table for all N5 kanji
- `_index_n4.md`, `_index_n3.md`, etc. — per JLPT level
- `_index_by_radical.md` — group kanji by radical (e.g., all 木-radical kanji together)
- `_index_by_frequency.md` — top 1000 most-frequent kanji

These can be regenerated from the per-kanji files using `_practice/scripts/regenerate_kanji_indexes.py` (planned).

## Dataview queries (in Obsidian)

If the Dataview plugin is enabled, you can query the kanji database from any note:

````markdown
```dataview
TABLE
  jlpt as "JLPT",
  frequency as "Freq",
  on_yomi as "On'yomi",
  kun_yomi as "Kun'yomi",
  meanings as "Meaning"
FROM "09 - Learning/18 - Japanese/_kanji"
WHERE jlpt = "N5"
SORT frequency ASC
LIMIT 20
```
````

## Cross-references

Within a chapter, vocabulary, or sentence note, link directly to kanji:

```markdown
The kanji [[人]] (person) appears in [[一人]] (alone), [[大人]] (adult), 
and [[日本人]] (Japanese person). Compare the visually-similar [[入]] 
(enter) — note the second stroke is shorter and lifts off rather than 
extending all the way down.
```

## SR drill integration

```bash
python _practice/scripts/18.3_kanji_drill.py --jlpt N5 --count 20 --seed 42
# Output: _practice/18.3_kanji_drills.md
# Tagged #review/japanese/kanji/N5 for Obsidian SR plugin
```

The drill picks 20 random N5 kanji, reads their frontmatter, and emits markdown SR cards (kanji on front, readings + meaning + vocabulary on back).

## Sources & licensing

- **KANJIDIC2** — © James Breen. Used under [Group License](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project). Attribution required for any redistribution.
- **KanjiVG** — © Ulrich Apel. CC BY-SA 3.0. Stroke-order SVGs.
- **JMdict** — © James Breen. Used under Group License.

These three datasets together cover all kanji in the JIS X 0208 standard (~6,000 characters) and the major vocabulary databases — far more than a learner ever needs (typical adult literacy = ~2,500 kanji).

## Status

- [ ] Bootstrap script written
- [ ] N5 database populated (~100 kanji)
- [ ] N4 database populated (~300 cumulative)
- [ ] N3 database populated (~650 cumulative)
- [ ] Drill script integrated with Obsidian SR plugin
- [ ] Master indexes generated (`_index_n5.md`, etc.)

The bootstrap script is the unblocker — once that's run, the rest is hand-curation (mnemonics, example sentences, mistake-tracking).
