"""
43.2 — Latin Declension Drill
------------------------------
Usage:
    python 43.2_declension_drill.py --count 10 --seed 42 --decl 1
    python 43.2_declension_drill.py --count 8 --mode parse --decl all
    python 43.2_declension_drill.py --count 6 --mode produce --decl 3

Modes:
    produce  — given a noun + case + number, produce the correct form
    parse    — given a Latin form, identify case/number/declension
"""

import random
import argparse
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# NOUN DATA  {nom_sg, gen_sg, gender, meaning, decl, paradigm}
# paradigm: [nom_sg, gen_sg, dat_sg, acc_sg, abl_sg, voc_sg,
#             nom_pl, gen_pl, dat_pl, acc_pl, abl_pl, voc_pl]
# ─────────────────────────────────────────────────────────────────────────────

NOUNS = {
    # 1st declension
    "puella": {
        "entry": "puella, puellae f.", "meaning": "girl", "decl": 1,
        "sg": {"nom": "puella", "gen": "puellae", "dat": "puellae",
               "acc": "puellam", "abl": "puellā", "voc": "puella"},
        "pl": {"nom": "puellae", "gen": "puellarum", "dat": "puellis",
               "acc": "puellas", "abl": "puellis", "voc": "puellae"},
    },
    "aqua": {
        "entry": "aqua, aquae f.", "meaning": "water", "decl": 1,
        "sg": {"nom": "aqua", "gen": "aquae", "dat": "aquae",
               "acc": "aquam", "abl": "aquā", "voc": "aqua"},
        "pl": {"nom": "aquae", "gen": "aquarum", "dat": "aquis",
               "acc": "aquas", "abl": "aquis", "voc": "aquae"},
    },
    "nauta": {
        "entry": "nauta, nautae m.", "meaning": "sailor", "decl": 1,
        "sg": {"nom": "nauta", "gen": "nautae", "dat": "nautae",
               "acc": "nautam", "abl": "nautā", "voc": "nauta"},
        "pl": {"nom": "nautae", "gen": "nautarum", "dat": "nautis",
               "acc": "nautas", "abl": "nautis", "voc": "nautae"},
    },
    # 2nd declension masculine
    "servus": {
        "entry": "servus, servī m.", "meaning": "slave", "decl": 2,
        "sg": {"nom": "servus", "gen": "servi", "dat": "servo",
               "acc": "servum", "abl": "servo", "voc": "serve"},
        "pl": {"nom": "servi", "gen": "servorum", "dat": "servis",
               "acc": "servos", "abl": "servis", "voc": "servi"},
    },
    "amicus": {
        "entry": "amicus, amicī m.", "meaning": "friend", "decl": 2,
        "sg": {"nom": "amicus", "gen": "amici", "dat": "amico",
               "acc": "amicum", "abl": "amico", "voc": "amice"},
        "pl": {"nom": "amici", "gen": "amicorum", "dat": "amicis",
               "acc": "amicos", "abl": "amicis", "voc": "amici"},
    },
    # 2nd declension neuter
    "bellum": {
        "entry": "bellum, bellī n.", "meaning": "war", "decl": 2,
        "sg": {"nom": "bellum", "gen": "belli", "dat": "bello",
               "acc": "bellum", "abl": "bello", "voc": "bellum"},
        "pl": {"nom": "bella", "gen": "bellorum", "dat": "bellis",
               "acc": "bella", "abl": "bellis", "voc": "bella"},
    },
    "verbum": {
        "entry": "verbum, verbī n.", "meaning": "word", "decl": 2,
        "sg": {"nom": "verbum", "gen": "verbi", "dat": "verbo",
               "acc": "verbum", "abl": "verbo", "voc": "verbum"},
        "pl": {"nom": "verba", "gen": "verborum", "dat": "verbis",
               "acc": "verba", "abl": "verbis", "voc": "verba"},
    },
    # 3rd declension
    "rex": {
        "entry": "rex, regis m.", "meaning": "king", "decl": 3,
        "sg": {"nom": "rex", "gen": "regis", "dat": "regi",
               "acc": "regem", "abl": "rege", "voc": "rex"},
        "pl": {"nom": "reges", "gen": "regum", "dat": "regibus",
               "acc": "reges", "abl": "regibus", "voc": "reges"},
    },
    "corpus": {
        "entry": "corpus, corporis n.", "meaning": "body", "decl": 3,
        "sg": {"nom": "corpus", "gen": "corporis", "dat": "corpori",
               "acc": "corpus", "abl": "corpore", "voc": "corpus"},
        "pl": {"nom": "corpora", "gen": "corporum", "dat": "corporibus",
               "acc": "corpora", "abl": "corporibus", "voc": "corpora"},
    },
    "miles": {
        "entry": "miles, militis m.", "meaning": "soldier", "decl": 3,
        "sg": {"nom": "miles", "gen": "militis", "dat": "militi",
               "acc": "militem", "abl": "milite", "voc": "miles"},
        "pl": {"nom": "milites", "gen": "militum", "dat": "militibus",
               "acc": "milites", "abl": "militibus", "voc": "milites"},
    },
    "urbs": {
        "entry": "urbs, urbis f.", "meaning": "city", "decl": 3,
        "sg": {"nom": "urbs", "gen": "urbis", "dat": "urbi",
               "acc": "urbem", "abl": "urbe", "voc": "urbs"},
        "pl": {"nom": "urbes", "gen": "urbium", "dat": "urbibus",
               "acc": "urbes", "abl": "urbibus", "voc": "urbes"},
    },
    # 4th declension
    "manus": {
        "entry": "manus, manūs f.", "meaning": "hand", "decl": 4,
        "sg": {"nom": "manus", "gen": "manus", "dat": "manui",
               "acc": "manum", "abl": "manu", "voc": "manus"},
        "pl": {"nom": "manus", "gen": "manuum", "dat": "manibus",
               "acc": "manus", "abl": "manibus", "voc": "manus"},
    },
    # 5th declension
    "res": {
        "entry": "rēs, reī f.", "meaning": "thing / affair", "decl": 5,
        "sg": {"nom": "res", "gen": "rei", "dat": "rei",
               "acc": "rem", "abl": "re", "voc": "res"},
        "pl": {"nom": "res", "gen": "rerum", "dat": "rebus",
               "acc": "res", "abl": "rebus", "voc": "res"},
    },
    "dies": {
        "entry": "diēs, diēī m./f.", "meaning": "day", "decl": 5,
        "sg": {"nom": "dies", "gen": "diei", "dat": "diei",
               "acc": "diem", "abl": "die", "voc": "dies"},
        "pl": {"nom": "dies", "gen": "dierum", "dat": "diebus",
               "acc": "dies", "abl": "diebus", "voc": "dies"},
    },
}

CASES = ["nom", "gen", "dat", "acc", "abl", "voc"]
CASE_NAMES = {
    "nom": "Nominative", "gen": "Genitive", "dat": "Dative",
    "acc": "Accusative", "abl": "Ablative", "voc": "Vocative"
}
CASE_FUNCTIONS = {
    "nom": "subject of verb",
    "gen": "possession / 'of'",
    "dat": "indirect object / 'to, for'",
    "acc": "direct object / object of motion-toward prepositions",
    "abl": "means, agent, manner, place / 'by, with, from, in'",
    "voc": "direct address",
}


def filter_nouns(decl_filter):
    if decl_filter == "all":
        return list(NOUNS.keys())
    return [k for k, v in NOUNS.items() if v["decl"] == int(decl_filter)]


def run_produce_drill(count, seed, decl_filter):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    noun_pool = filter_nouns(decl_filter)
    if not noun_pool:
        print(f"No nouns found for declension {decl_filter}.")
        return
    output = [f"# 43.2 Latin Declension Drill — Produce Form — {timestamp}",
              f"Seed: {seed} | Count: {count} | Declension: {decl_filter}", ""]

    seen, unique = set(), []
    for _ in range(count * 10):
        noun = random.choice(noun_pool)
        number = random.choice(["sg", "pl"])
        case = random.choice(CASES)
        key = (noun, number, case)
        if key not in seen:
            seen.add(key)
            unique.append(key)
        if len(unique) == count:
            break

    for i, (noun, number, case) in enumerate(unique, 1):
        correct = NOUNS[noun][number][case]
        entry = NOUNS[noun]["entry"]
        meaning = NOUNS[noun]["meaning"]
        case_label = CASE_NAMES[case]
        num_label = "Singular" if number == "sg" else "Plural"
        output.append(f"## Q{i}. *{entry}* ({meaning})")
        output.append(f"**{case_label} {num_label}** → ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**{correct}**")
        output.append(f"Function: {CASE_FUNCTIONS[case]}")
        output.append("</details>")
        output.append("")
    print("\n".join(output))


def run_parse_drill(count, seed, decl_filter):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    noun_pool = filter_nouns(decl_filter)
    if not noun_pool:
        print(f"No nouns found for declension {decl_filter}.")
        return
    output = [f"# 43.2 Latin Declension Drill — Parse Form — {timestamp}",
              f"Seed: {seed} | Count: {count} | Declension: {decl_filter}", ""]

    seen, unique = set(), []
    for _ in range(count * 10):
        noun = random.choice(noun_pool)
        number = random.choice(["sg", "pl"])
        case = random.choice(CASES)
        form = NOUNS[noun][number][case]
        key = (noun, number, case)
        if key not in seen:
            seen.add(key)
            unique.append((noun, number, case, form))
        if len(unique) == count:
            break

    for i, (noun, number, case, form) in enumerate(unique, 1):
        entry = NOUNS[noun]["entry"]
        meaning = NOUNS[noun]["meaning"]
        decl = NOUNS[noun]["decl"]
        output.append(f"## Q{i}. Parse **{form}** (from *{entry}* — {meaning})")
        output.append("Case: ___ | Number: ___ | Declension: ___ | Function: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**Case:** {CASE_NAMES[case]}")
        output.append(f"**Number:** {'Singular' if number == 'sg' else 'Plural'}")
        output.append(f"**Declension:** {decl}")
        output.append(f"**Function:** {CASE_FUNCTIONS[case]}")

        # note ambiguous forms
        ambiguous = []
        for c2 in CASES:
            for n2 in ["sg", "pl"]:
                if NOUNS[noun][n2][c2] == form and (c2 != case or n2 != number):
                    ambiguous.append(f"{CASE_NAMES[c2]} {n2}")
        if ambiguous:
            output.append(f"*Note: also could be {', '.join(ambiguous)} (ambiguous ending — context determines)*")
        output.append("</details>")
        output.append("")
    print("\n".join(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Latin declension drill generator")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--decl", default="all",
                        choices=["all", "1", "2", "3", "4", "5"])
    parser.add_argument("--mode", default="produce",
                        choices=["produce", "parse"])
    args = parser.parse_args()
    if args.mode == "produce":
        run_produce_drill(args.count, args.seed, args.decl)
    elif args.mode == "parse":
        run_parse_drill(args.count, args.seed, args.decl)
