"""
43.4 — Latin Verb Conjugation Drill
--------------------------------------
Usage:
    python 43.4_verb_conjugation_drill.py --count 10 --seed 42 --tense present
    python 43.4_verb_conjugation_drill.py --count 8 --mode parse
    python 43.4_verb_conjugation_drill.py --count 6 --mode principal_parts
    python 43.4_verb_conjugation_drill.py --count 8 --mode indirect_statement

Modes:
    conjugation       — verb + tense + voice + person → correct form
    parse             — given a Latin verb form, parse it fully
    principal_parts   — given infinitive, supply all 4 principal parts
    indirect_statement — translate an English indirect statement into Latin
"""

import random
import argparse
from datetime import datetime

VERBS = {
    "amare": {
        "pp": ("amo", "amare", "amavi", "amatum"),
        "meaning": "to love",
        "conj": 1,
        "present_act":  ["amo", "amas", "amat", "amamus", "amatis", "amant"],
        "present_pass": ["amor", "amaris", "amatur", "amamur", "amamini", "amantur"],
        "impf_act":     ["amabam", "amabas", "amabat", "amabamus", "amabatis", "amabant"],
        "impf_pass":    ["amabar", "amabaris", "amabatur", "amabamur", "amabamini", "amabantur"],
        "fut_act":      ["amabo", "amabis", "amabit", "amabimus", "amabitis", "amabunt"],
        "fut_pass":     ["amabor", "amaberis", "amabitur", "amabimur", "amabimini", "amabuntur"],
        "perf_act":     ["amavi", "amavisti", "amavit", "amavimus", "amavistis", "amaverunt"],
    },
    "monere": {
        "pp": ("moneo", "monere", "monui", "monitum"),
        "meaning": "to warn",
        "conj": 2,
        "present_act":  ["moneo", "mones", "monet", "monemus", "monetis", "monent"],
        "present_pass": ["moneor", "moneris", "monetur", "monemur", "monemini", "monentur"],
        "impf_act":     ["monebam", "monebas", "monebat", "monebamus", "monebatis", "monebant"],
        "impf_pass":    ["monebar", "monebaris", "monebatur", "monebamur", "monebamini", "monebantur"],
        "fut_act":      ["monebo", "monebis", "monebit", "monebimus", "monebitis", "monebunt"],
        "fut_pass":     ["monebor", "moneberis", "monebitur", "monebimur", "monebimini", "monebuntur"],
        "perf_act":     ["monui", "monuisti", "monuit", "monuimus", "monuistis", "monuerunt"],
    },
    "agere": {
        "pp": ("ago", "agere", "egi", "actum"),
        "meaning": "to drive / do",
        "conj": 3,
        "present_act":  ["ago", "agis", "agit", "agimus", "agitis", "agunt"],
        "present_pass": ["agor", "ageris", "agitur", "agimur", "agimini", "aguntur"],
        "impf_act":     ["agebam", "agebas", "agebat", "agebamus", "agebatis", "agebant"],
        "impf_pass":    ["agebar", "agebaris", "agebatur", "agebamur", "agebamini", "agebantur"],
        "fut_act":      ["agam", "ages", "aget", "agemus", "agetis", "agent"],
        "fut_pass":     ["agar", "ageris", "agetur", "agemur", "agemini", "agentur"],
        "perf_act":     ["egi", "egisti", "egit", "egimus", "egistis", "egerunt"],
    },
    "audire": {
        "pp": ("audio", "audire", "audivi", "auditum"),
        "meaning": "to hear",
        "conj": 4,
        "present_act":  ["audio", "audis", "audit", "audimus", "auditis", "audiunt"],
        "present_pass": ["audior", "audiris", "auditur", "audimur", "audimini", "audiuntur"],
        "impf_act":     ["audiebam", "audiebas", "audiebat", "audiebamus", "audiebatis", "audiebant"],
        "impf_pass":    ["audiebar", "audiebaris", "audiebatur", "audiebamur", "audiebamini", "audiebantur"],
        "fut_act":      ["audiam", "audies", "audiet", "audiemus", "audietis", "audient"],
        "fut_pass":     ["audiar", "audieris", "audietur", "audiemur", "audiemini", "audientur"],
        "perf_act":     ["audivi", "audivisti", "audivit", "audivimus", "audivistis", "audiverunt"],
    },
    "esse": {
        "pp": ("sum", "esse", "fui", "futurum"),
        "meaning": "to be",
        "conj": "irreg",
        "present_act":  ["sum", "es", "est", "sumus", "estis", "sunt"],
        "present_pass": ["N/A"] * 6,
        "impf_act":     ["eram", "eras", "erat", "eramus", "eratis", "erant"],
        "impf_pass":    ["N/A"] * 6,
        "fut_act":      ["ero", "eris", "erit", "erimus", "eritis", "erunt"],
        "fut_pass":     ["N/A"] * 6,
        "perf_act":     ["fui", "fuisti", "fuit", "fuimus", "fuistis", "fuerunt"],
    },
}

PERSONS_LATIN = ["ego (1st sg.)", "tu (2nd sg.)", "is/ea (3rd sg.)",
                 "nos (1st pl.)", "vos (2nd pl.)", "ei/eae (3rd pl.)"]
TENSES_VOICES = [
    ("present_act", "Present Active"),
    ("present_pass", "Present Passive"),
    ("impf_act", "Imperfect Active"),
    ("impf_pass", "Imperfect Passive"),
    ("fut_act", "Future Active"),
    ("fut_pass", "Future Passive"),
    ("perf_act", "Perfect Active"),
]

INDIRECT_STATEMENTS = [
    {
        "english": "He says that the girl is good.",
        "latin": "Dicit puellam bonam esse.",
        "note": "Present infinitive esse — simultaneous with dicit; puellam = acc. subject; bonam agrees with puellam (f. acc. sg.)",
    },
    {
        "english": "I think that Caesar has conquered.",
        "latin": "Puto Caesarem vicisse.",
        "note": "Perfect infinitive vicisse — prior to puto; Caesarem = acc. subject",
    },
    {
        "english": "She says that the soldiers will come.",
        "latin": "Dicit milites venturos esse.",
        "note": "Future active infinitive venturos esse — subsequent to dicit; milites = acc. subject (m. pl.); venturos agrees",
    },
    {
        "english": "I knew that you were a good man.",
        "latin": "Sciebam te esse virum bonum.",
        "note": "Present infinitive esse — simultaneous with sciebam (secondary sequence); te = acc. subject",
    },
    {
        "english": "He says that he himself is tired. (reflexive)",
        "latin": "Dicit se esse fessum.",
        "note": "Reflexive se (not eum) because acc. subject refers back to main subject; fessum agrees with se (m. acc. sg.)",
    },
]


def run_conjugation_drill(count, seed, tense_voice):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 43.4 Latin Verb Conjugation Drill — {timestamp}",
              f"Seed: {seed} | Count: {count} | Tense/Voice: {tense_voice}", ""]
    tv_pool = TENSES_VOICES if tense_voice == "all" else [(t, l) for t, l in TENSES_VOICES if t == tense_voice]
    verb_pool = list(VERBS.keys())
    seen, unique = set(), []
    for _ in range(count * 10):
        verb = random.choice(verb_pool)
        tv_key, tv_label = random.choice(tv_pool)
        pidx = random.randint(0, 5)
        form = VERBS[verb][tv_key][pidx]
        if form == "N/A":
            continue
        key = (verb, tv_key, pidx)
        if key not in seen:
            seen.add(key)
            unique.append((verb, tv_key, tv_label, pidx, form))
        if len(unique) == count:
            break
    for i, (verb, tv_key, tv_label, pidx, correct) in enumerate(unique, 1):
        pp = VERBS[verb]["pp"]
        meaning = VERBS[verb]["meaning"]
        person = PERSONS_LATIN[pidx]
        output.append(f"## Q{i}. *{pp[0]}, {pp[1]}* ({meaning})")
        output.append(f"**{tv_label}** — **{person}**")
        output.append("Answer: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**{correct}**")
        output.append("</details>")
        output.append("")
    print("\n".join(output))


def run_principal_parts_drill(count, seed):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 43.4 Latin Principal Parts Drill — {timestamp}",
              f"Seed: {seed} | Count: {count}", ""]
    verb_pool = random.sample(list(VERBS.keys()), min(count, len(VERBS)))
    for i, verb in enumerate(verb_pool, 1):
        pp = VERBS[verb]["pp"]
        meaning = VERBS[verb]["meaning"]
        output.append(f"## Q{i}. Give all 4 principal parts of: *{pp[1]}* ({meaning})")
        output.append("1st: ___ | 2nd: ___ | 3rd: ___ | 4th: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**{pp[0]}, {pp[1]}, {pp[2]}, {pp[3]}**")
        output.append("</details>")
        output.append("")
    print("\n".join(output))


def run_indirect_statement_drill(count, seed):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 43.5 Latin Indirect Statement Drill — {timestamp}",
              f"Seed: {seed} | Count: {count}", ""]
    samples = random.sample(INDIRECT_STATEMENTS, min(count, len(INDIRECT_STATEMENTS)))
    for i, item in enumerate(samples, 1):
        output.append(f"## Q{i}. Translate into Latin (using accusative + infinitive):")
        output.append(f"**\"{item['english']}\"**")
        output.append("Latin: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**{item['latin']}**")
        output.append(f"*Note: {item['note']}*")
        output.append("</details>")
        output.append("")
    print("\n".join(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Latin verb conjugation drill generator")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--tense", default="all",
                        choices=["all", "present_act", "present_pass",
                                 "impf_act", "impf_pass", "fut_act", "fut_pass", "perf_act"])
    parser.add_argument("--mode", default="conjugation",
                        choices=["conjugation", "principal_parts", "indirect_statement"])
    args = parser.parse_args()
    if args.mode == "conjugation":
        run_conjugation_drill(args.count, args.seed, args.tense)
    elif args.mode == "principal_parts":
        run_principal_parts_drill(args.count, args.seed)
    elif args.mode == "indirect_statement":
        run_indirect_statement_drill(args.count, args.seed)
