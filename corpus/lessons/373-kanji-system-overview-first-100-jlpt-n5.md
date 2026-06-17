---
title: "37.3 — Kanji: System Overview & First 100 (JLPT N5)"
subject: "Japanese"
catalog: advanced
audience_tier: higher-education
chapter: "37.3"
type: chapter
objectives:
  - "Understand the concepts"
  - "Apply the theory"
open_source: true
---

*Back to [Subject_Plan](Subject_Plan) | Part of [Learning Index](00---09---Learning-Index)*

# 37.3 — Kanji: System Overview & First 100 (JLPT N5)

> *"Kanji are not obstacles to reading Japanese. They ARE reading Japanese — and once you stop fighting them and start treating them as a database, they become one of the most powerful features of the language."*

English speakers fear kanji. This is the wrong frame. Kanji are a structured system: every character has radicals (components), readings, and meanings that form patterns. The system is learnable. The first 100 kanji (JLPT N5) are among the most frequent characters in all Japanese text — master them and you've unlocked a huge percentage of daily written Japanese.

---

## 🎯 Learning Objectives

By the end of this chapter you will be able to:

1. Explain the radical system and use radicals to analyze and memorize kanji structure.
2. Distinguish on'yomi (Chinese-derived reading) from kun'yomi (native Japanese reading) and know when to use each.
3. Look up any kanji by radical, stroke count, or reading using Jisho.org.
4. Recognize, read, and use the first 100 JLPT N5 kanji with their primary readings and vocabulary.
5. Navigate the vault's `_kanji/` database.

---

## 📚 1. The Kanji System — Axioms

### Axiom 1: Kanji are logograms
Each kanji represents a **meaning** (and sound), not just a sound. 日 means "sun/day" and is read differently in different contexts. This is why kanji can't be learned by phonetic drilling alone.

### Axiom 2: Every kanji has radicals
**Radicals** (部首, bushu) are the component building blocks of kanji. Every kanji is composed of one or more radicals. The radical determines how kanji are organized in dictionaries.

Examples:
- 語 (language) = 言 (speech radical) + 吾 (phonetic component)
- 明 (bright) = 日 (sun) + 月 (moon) — sun + moon = bright
- 森 (forest) = 木 (tree) × 3 — three trees = forest
- 休 (rest) = 人 (person) + 木 (tree) — person leaning against tree = rest

> Radicals give you a framework for **mnemonics and visual memory**. When you see an unfamiliar kanji, you can often guess the meaning from the radicals.

### Axiom 3: Kanji have (usually) two types of readings

| Reading type | Name | Origin | When used |
|-------------|------|--------|----------|
| **On'yomi** | 音読み | Chinese-derived pronunciation | Usually in compound words (jukugo) with other kanji |
| **Kun'yomi** | 訓読み | Native Japanese pronunciation | Usually when kanji stands alone or with hiragana endings |

**Example — 日 (sun/day):**
- On'yomi: ニチ (nichi), ジツ (jitsu)
  - 日本 (Nihon = Japan) — compound word, on'yomi
  - 日曜日 (Nichiyōbi = Sunday) — on'yomi
- Kun'yomi: ひ (hi), か (ka)
  - 日 (hi = sun/day when standing alone)
  - 一日 (tsuitachi = first day of month) — kun'yomi

> **The practical rule:** Kanji in compound words (two+ kanji together) → usually on'yomi. Kanji followed by hiragana (okurigana) or standing alone → usually kun'yomi. There are exceptions, but this rule covers ~80% of cases.

### Axiom 4: Kanji + hiragana = okurigana
Hiragana attached to a kanji (okurigana) completes the word — it often carries the grammatical ending:
- 食べる (taberu = to eat) — 食 is the kanji, べる is okurigana
- 大きい (ookii = big) — 大 is kanji, きい is okurigana
- 書く (kaku = to write) — 書 is kanji, く is okurigana

---

## 📚 2. How to Look Up Kanji

### By radical (Jisho.org)
1. Go to [Jisho.org](https://jisho.org/)
2. Click the radical lookup button (#)
3. Select the radicals you can identify in the character
4. Jisho narrows down the candidates

### By stroke count
Count the strokes carefully (there are rules about stroke order — practice these).

### By reading
If you know the pronunciation, just type it in romaji at Jisho.

### By drawing (phone)
Google Translate's camera mode, or apps like Kanji Study, let you draw the character and get a match.

---

## 📚 3. The Vault Kanji Database — `_kanji/`

This vault maintains a **first-class kanji database** in `37 - Japanese/_kanji/`. See [Subject_Plan#6. THE KANJI METHOD](Subject_Plan#6.-THE-KANJI-METHOD) for full documentation.

Each kanji note contains:
- Frontmatter: JLPT level, frequency, stroke count, radicals, on/kun readings
- Stroke order SVG embedded from `09 - Learning/_svgs/`
- High-frequency vocabulary table
- Example sentences
- Mnemonic (hand-curated)
- Cross-links to related kanji

**To navigate:** In Obsidian, type `[[` and start typing a kanji character (e.g., `[[人`) to jump to its note.

---

## 📚 4. The First 100 JLPT N5 Kanji — Master Table

These 100 kanji appear in virtually all N5 study materials and cover a large portion of everyday Japanese text. Learn them with the vault's `_kanji/` notes.

| Kanji | On'yomi | Kun'yomi | Core meaning | Key vocabulary |
|-------|--------|---------|-------------|---------------|
| 日 | ニチ、ジツ | ひ、か | sun, day | 日本 (Nihon), 毎日 (mainichi), 今日 (kyou) |
| 一 | イチ | ひと(つ) | one | 一つ (hitotsu), 一日 (ichinichi) |
| 国 | コク | くに | country | 日本国 (Nihonkoku), 外国 (gaikoku) |
| 人 | ジン、ニン | ひと | person | 人 (hito), 日本人 (Nihonjin), 一人 (hitori) |
| 年 | ネン | とし | year | 今年 (kotoshi), 毎年 (maitoshi) |
| 大 | ダイ、タイ | おお(きい) | big, large | 大学 (daigaku), 大きい (ookii) |
| 十 | ジュウ | とお | ten | 十 (juu), 十分 (juppun) |
| 二 | ニ | ふた(つ) | two | 二つ (futatsu), 二人 (futari) |
| 本 | ホン | もと | book, origin | 日本 (Nihon), 本 (hon = book) |
| 中 | チュウ | なか | middle, inside | 中国 (Chuugoku), 中 (naka) |
| 長 | チョウ | なが(い) | long, leader | 長い (nagai), 社長 (shachou) |
| 出 | シュツ | で(る)、だ(す) | exit, come out | 出口 (deguchi), 出る (deru) |
| 三 | サン | み(つ)、みっ(つ) | three | 三つ (mittsu), 三日 (mikkа) |
| 時 | ジ | とき | time, hour | 時間 (jikan), 何時 (nanji) |
| 行 | コウ、ギョウ | い(く)、おこな(う) | go, conduct | 行く (iku), 銀行 (ginkou) |
| 見 | ケン | み(る)、み(せる) | see, show | 見る (miru), 見せる (miseru) |
| 子 | シ、ス | こ | child | 子供 (kodomo), 女子 (joshi) |
| 分 | ブン、フン | わ(かる)、わ(ける) | minute, divide, understand | 分かる (wakaru), 三分 (sanpun) |
| 四 | シ | よ(つ)、よっ(つ)、よん | four | 四つ (yottsu), 四月 (shigatsu) |
| 何 | カ | なに、なん | what | 何 (nani), 何時 (nanji) |
| 先 | セン | さき | ahead, previous | 先生 (sensei), 先 (saki) |
| 生 | セイ、ショウ | い(きる)、う(まれる)、なま | life, live, raw | 先生 (sensei), 学生 (gakusei), 生まれる (umareru) |
| 五 | ゴ | いつ(つ) | five | 五つ (itsutsu), 五月 (gogatsu) |
| 間 | カン、ケン | あいだ、ま | interval, between | 時間 (jikan), 間 (aida) |
| 上 | ジョウ | うえ、うわ、かみ、あ(げる) | above, up | 上 (ue), 上げる (ageru) |
| 東 | トウ | ひがし | east | 東京 (Toukyou), 東 (higashi) |
| 四 | already listed | | | |
| 高 | コウ | たか(い) | tall, high, expensive | 高い (takai), 高校 (koukou) |
| 前 | ゼン | まえ | before, front | 前 (mae), 名前 (namae) |
| 本 | already listed | | | |
| 女 | ジョ、ニョ | おんな | woman | 女 (onna), 女性 (josei) |
| 山 | サン | やま | mountain | 山 (yama), 富士山 (Fujisan) |
| 川 | セン | かわ | river | 川 (kawa), 小川 (ogawa) |
| 土 | ド、ト | つち | earth, soil | 土曜日 (doyoubi), 土 (tsuchi) |
| 八 | ハチ | や(つ)、やっ(つ)、よう | eight | 八つ (yattsu), 八月 (hachigatsu) |
| 六 | ロク | む(つ)、むっ(つ) | six | 六つ (muttsu), 六月 (rokugatsu) |
| 円 | エン | まる(い) | circle, yen | 百円 (hyakuen), 丸い (marui) |
| 学 | ガク | まな(ぶ) | study, learn | 学校 (gakkou), 学生 (gakusei), 学ぶ (manabu) |
| 金 | キン、コン | かね、かな | gold, money | お金 (okane), 金曜日 (kinyoubi) |
| 月 | ゲツ、ガツ | つき | moon, month | 月曜日 (getsuyoubi), 月 (tsuki) |
| 語 | ゴ | かた(る) | language, word | 日本語 (Nihongo), 英語 (eigo) |
| 火 | カ | ひ | fire | 火曜日 (kayoubi), 火 (hi) |
| 水 | スイ | みず | water | 水曜日 (suiyoubi), 水 (mizu) |
| 木 | モク、ボク | き、こ | tree, wood | 木曜日 (mokuyoubi), 木 (ki) |

*(Remaining N5 kanji covered in `_kanji/_index_n5.md` — the full 100-kanji table with all readings and vocabulary)*

---

## 🛠️ 5. Learning Strategy

### The Wanikani Method (recommended for beginners)
[Wanikani](https://www.wanikani.com/) teaches kanji through radicals → kanji → vocabulary in a structured SRS. Free for the first 3 levels (~60 kanji). Highly recommended for establishing the radical-based mnemonic habit.

### The Anki Method
Import a JLPT N5 kanji deck. Each card: kanji on front, readings + meanings + example vocabulary on back. Supplement with vault kanji notes.

### The Vault Method
The `_kanji/` database (see [Subject_Plan#6](Subject_Plan#6)) is the native vault approach. Each kanji is a searchable note with cross-links. Best for integrating kanji with your other vault notes.

---

## ⚠️ 6. Common Errors

| Error | Notes |
|-------|-------|
| Using on'yomi where kun'yomi is needed | 食 as a standalone word is た (from 食べる), not ショク. Context determines reading. |
| Ignoring radicals | Treating each kanji as a unique shape to memorize rather than a combination of known components — makes memory load exponentially harder. |
| Skipping vocabulary | Learning kanji readings in isolation without vocabulary. Always learn kanji through words you'll actually use. |
| Confusing similar kanji | 土/士, 己/已/巳, 犬/太, 刀/力 — use radical analysis to distinguish. |

---

## 🧮 7. Hands-On Lab

**Drill:** Run `18.3_kanji_drill.py --level n5 --mode recognition --count 20`.

**Vault navigation:** Open `_kanji/人.md`, `_kanji/日.md`, and `_kanji/本.md`. For each, learn all vocabulary in the table and write 2 example sentences using the vocabulary.

---

## 🔗 8. Cross-links & Further Reading

### Internal Links
- Previous: [37.2 - Katakana — Loanwords & Foreign Names](37.2---Katakana-—-Loanwords-&-Foreign-Names)
- Next: [37.4 - Particles & Basic Sentence Structure](37.4---Particles-&-Basic-Sentence-Structure)
- Kanji database: [README](README)

### External Resources
- [Wanikani](https://www.wanikani.com/) — structured kanji SRS (free first 3 levels)
- [Jisho.org](https://jisho.org/) — kanji dictionary with radical lookup
- [Kanji.koohii.com](https://kanji.koohii.com/) — community mnemonics (RTK-based)
- [KANJIDIC2](http://nihongo.monash.edu/kanjidic2/index.html) — machine-readable kanji database (used by bootstrap script)
- [KanjiVG](https://kanjivg.tagaini.net/) — stroke order SVGs (used by vault)
