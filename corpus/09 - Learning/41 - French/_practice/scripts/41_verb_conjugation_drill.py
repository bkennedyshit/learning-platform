"""
41 — French Verb Conjugation Drill
-----------------------------------
Generates randomized French verb conjugation exercises.
Usage:
    python 41_verb_conjugation_drill.py --count 10 --seed 42 --tense present
    python 41_verb_conjugation_drill.py --count 8 --seed 7 --tense all --verb aller
    python 41_verb_conjugation_drill.py --count 6 --mode si_clauses

Modes:
    conjugation  — verb + tense + person → produce the correct form
    si_clauses   — complete the si-clause sequence
    subjunctive  — give correct subjunctive form for a trigger phrase
    pc_vs_imp    — choose passé composé or imparfait for a context sentence
"""

import random
import argparse
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# VERB DATA
# ─────────────────────────────────────────────────────────────────────────────

VERBS = {
    # verb: {tense: [je, tu, il/elle, nous, vous, ils/elles]}
    "parler": {
        "present":    ["parle", "parles", "parle", "parlons", "parlez", "parlent"],
        "imparfait":  ["parlais", "parlais", "parlait", "parlions", "parliez", "parlaient"],
        "futur":      ["parlerai", "parleras", "parlera", "parlerons", "parlerez", "parleront"],
        "conditionnel": ["parlerais", "parlerais", "parlerait", "parlerions", "parleriez", "parleraient"],
        "subjonctif": ["parle", "parles", "parle", "parlions", "parliez", "parlent"],
        "passé_composé_aux": "avoir", "passé_composé_pp": "parlé",
    },
    "finir": {
        "present":    ["finis", "finis", "finit", "finissons", "finissez", "finissent"],
        "imparfait":  ["finissais", "finissais", "finissait", "finissions", "finissiez", "finissaient"],
        "futur":      ["finirai", "finiras", "finira", "finirons", "finirez", "finiront"],
        "conditionnel": ["finirais", "finirais", "finirait", "finirions", "finiriez", "finiraient"],
        "subjonctif": ["finisse", "finisses", "finisse", "finissions", "finissiez", "finissent"],
        "passé_composé_aux": "avoir", "passé_composé_pp": "fini",
    },
    "vendre": {
        "present":    ["vends", "vends", "vend", "vendons", "vendez", "vendent"],
        "imparfait":  ["vendais", "vendais", "vendait", "vendions", "vendiez", "vendaient"],
        "futur":      ["vendrai", "vendras", "vendra", "vendrons", "vendrez", "vendront"],
        "conditionnel": ["vendrais", "vendrais", "vendrait", "vendrions", "vendriez", "vendraient"],
        "subjonctif": ["vende", "vendes", "vende", "vendions", "vendiez", "vendent"],
        "passé_composé_aux": "avoir", "passé_composé_pp": "vendu",
    },
    "être": {
        "present":    ["suis", "es", "est", "sommes", "êtes", "sont"],
        "imparfait":  ["étais", "étais", "était", "étions", "étiez", "étaient"],
        "futur":      ["serai", "seras", "sera", "serons", "serez", "seront"],
        "conditionnel": ["serais", "serais", "serait", "serions", "seriez", "seraient"],
        "subjonctif": ["sois", "sois", "soit", "soyons", "soyez", "soient"],
        "passé_composé_aux": "avoir", "passé_composé_pp": "été",
    },
    "avoir": {
        "present":    ["ai", "as", "a", "avons", "avez", "ont"],
        "imparfait":  ["avais", "avais", "avait", "avions", "aviez", "avaient"],
        "futur":      ["aurai", "auras", "aura", "aurons", "aurez", "auront"],
        "conditionnel": ["aurais", "aurais", "aurait", "aurions", "auriez", "auraient"],
        "subjonctif": ["aie", "aies", "ait", "ayons", "ayez", "aient"],
        "passé_composé_aux": "avoir", "passé_composé_pp": "eu",
    },
    "aller": {
        "present":    ["vais", "vas", "va", "allons", "allez", "vont"],
        "imparfait":  ["allais", "allais", "allait", "allions", "alliez", "allaient"],
        "futur":      ["irai", "iras", "ira", "irons", "irez", "iront"],
        "conditionnel": ["irais", "irais", "irait", "irions", "iriez", "iraient"],
        "subjonctif": ["aille", "ailles", "aille", "allions", "alliez", "aillent"],
        "passé_composé_aux": "être", "passé_composé_pp": "allé",
    },
    "faire": {
        "present":    ["fais", "fais", "fait", "faisons", "faites", "font"],
        "imparfait":  ["faisais", "faisais", "faisait", "faisions", "faisiez", "faisaient"],
        "futur":      ["ferai", "feras", "fera", "ferons", "ferez", "feront"],
        "conditionnel": ["ferais", "ferais", "ferait", "ferions", "feriez", "feraient"],
        "subjonctif": ["fasse", "fasses", "fasse", "fassions", "fassiez", "fassent"],
        "passé_composé_aux": "avoir", "passé_composé_pp": "fait",
    },
    "venir": {
        "present":    ["viens", "viens", "vient", "venons", "venez", "viennent"],
        "imparfait":  ["venais", "venais", "venait", "venions", "veniez", "venaient"],
        "futur":      ["viendrai", "viendras", "viendra", "viendrons", "viendrez", "viendront"],
        "conditionnel": ["viendrais", "viendrais", "viendrait", "viendrions", "viendriez", "viendraient"],
        "subjonctif": ["vienne", "viennes", "vienne", "venions", "veniez", "viennent"],
        "passé_composé_aux": "être", "passé_composé_pp": "venu",
    },
    "prendre": {
        "present":    ["prends", "prends", "prend", "prenons", "prenez", "prennent"],
        "imparfait":  ["prenais", "prenais", "prenait", "prenions", "preniez", "prenaient"],
        "futur":      ["prendrai", "prendras", "prendra", "prendrons", "prendrez", "prendront"],
        "conditionnel": ["prendrais", "prendrais", "prendrait", "prendrions", "prendriez", "prendraient"],
        "subjonctif": ["prenne", "prennes", "prenne", "prenions", "preniez", "prennent"],
        "passé_composé_aux": "avoir", "passé_composé_pp": "pris",
    },
    "pouvoir": {
        "present":    ["peux", "peux", "peut", "pouvons", "pouvez", "peuvent"],
        "imparfait":  ["pouvais", "pouvais", "pouvait", "pouvions", "pouviez", "pouvaient"],
        "futur":      ["pourrai", "pourras", "pourra", "pourrons", "pourrez", "pourront"],
        "conditionnel": ["pourrais", "pourrais", "pourrait", "pourrions", "pourriez", "pourraient"],
        "subjonctif": ["puisse", "puisses", "puisse", "puissions", "puissiez", "puissent"],
        "passé_composé_aux": "avoir", "passé_composé_pp": "pu",
    },
    "vouloir": {
        "present":    ["veux", "veux", "veut", "voulons", "voulez", "veulent"],
        "imparfait":  ["voulais", "voulais", "voulait", "voulions", "vouliez", "voulaient"],
        "futur":      ["voudrai", "voudras", "voudra", "voudrons", "voudrez", "voudront"],
        "conditionnel": ["voudrais", "voudrais", "voudrait", "voudrions", "voudriez", "voudraient"],
        "subjonctif": ["veuille", "veuilles", "veuille", "voulions", "vouliez", "veuillent"],
        "passé_composé_aux": "avoir", "passé_composé_pp": "voulu",
    },
    "savoir": {
        "present":    ["sais", "sais", "sait", "savons", "savez", "savent"],
        "imparfait":  ["savais", "savais", "savait", "savions", "saviez", "savaient"],
        "futur":      ["saurai", "sauras", "saura", "saurons", "saurez", "sauront"],
        "conditionnel": ["saurais", "saurais", "saurait", "saurions", "sauriez", "sauraient"],
        "subjonctif": ["sache", "saches", "sache", "sachions", "sachiez", "sachent"],
        "passé_composé_aux": "avoir", "passé_composé_pp": "su",
    },
}

PERSONS = ["je", "tu", "il/elle", "nous", "vous", "ils/elles"]
TENSES = ["present", "imparfait", "futur", "conditionnel", "subjonctif"]
TENSE_LABELS = {
    "present": "Présent",
    "imparfait": "Imparfait",
    "futur": "Futur simple",
    "conditionnel": "Conditionnel présent",
    "subjonctif": "Subjonctif présent",
}

SI_CLAUSES = [
    {
        "type": "Open (real)",
        "si_tense": "present", "main_tense": "futur",
        "example_si": "Si tu travailles dur", "example_main": "tu réussiras.",
        "cue": "Conjugate: si + [present] → [futur]",
    },
    {
        "type": "Hypothetical (unlikely)",
        "si_tense": "imparfait", "main_tense": "conditionnel",
        "example_si": "Si tu travaillais dur", "example_main": "tu réussirais.",
        "cue": "Conjugate: si + [imparfait] → [conditionnel]",
    },
    {
        "type": "Past contrary-to-fact",
        "si_tense": "plus-que-parfait", "main_tense": "conditionnel_passé",
        "example_si": "Si tu avais travaillé dur", "example_main": "tu aurais réussi.",
        "cue": "Conjugate: si + [plus-que-parfait] → [conditionnel passé]",
    },
]

SUBJUNCTIVE_TRIGGERS = [
    ("Il faut que tu ___.", "venir", "viennes", "obligation"),
    ("Je veux qu'il ___.", "partir", "parte", "will"),
    ("Bien qu'elle ___ fatiguée, elle continue.", "être", "soit", "concessive"),
    ("Nous sommes contents que vous ___ là.", "être", "soyez", "emotion"),
    ("Je doute qu'il ___ la vérité.", "savoir", "sache", "doubt"),
    ("Il est important que vous ___ à l'heure.", "arriver", "arriviez", "impersonal"),
    ("Elle part avant que tu ne ___.", "arriver", "arrives", "conjunction"),
    ("Pour que nous ___ ensemble, venez vite.", "travailler", "travaillions", "purpose"),
    ("Je suis désolé qu'il ne ___ pas venu.", "être", "soit", "emotion"),
    ("Il est possible qu'ils ___ en retard.", "être", "soient", "impersonal"),
]

PC_IMP_SCENARIOS = [
    ("Hier, il ___ (faire) beau toute la journée.", "faisait", "imp", "Ongoing background condition — imparfait"),
    ("Soudain, il ___ (commencer) à pleuvoir.", "a commencé", "pc", "Sudden event — passé composé"),
    ("Quand j'étais enfant, je ___ (jouer) au foot tous les samedis.", "jouais", "imp", "Habitual past — imparfait"),
    ("Elle ___ (arriver) en retard trois fois ce mois-ci.", "est arrivée", "pc", "Counted/specific events — passé composé"),
    ("Il ___ (dormir) quand le téléphone a sonné.", "dormait", "imp", "Interrupted ongoing action — imparfait"),
    ("Nous ___ (manger) une pizza et ___ (rentrer) chez nous.", "avons mangé / sommes rentrés", "pc", "Sequence of completed events — passé composé"),
    ("Avant, elle ___ (habiter) à Paris.", "habitait", "imp", "State in past with no defined end — imparfait"),
    ("Ce matin, je ___ (se réveiller) à 7h.", "me suis réveillé(e)", "pc", "Specific completed event — passé composé"),
]


# ─────────────────────────────────────────────────────────────────────────────
# DRILL RUNNERS
# ─────────────────────────────────────────────────────────────────────────────

def run_conjugation_drill(count, seed, tense_filter, verb_filter):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 41 French Conjugation Drill — {timestamp}",
              f"Seed: {seed} | Count: {count} | Tense: {tense_filter} | Verb: {verb_filter or 'random'}", ""]

    verb_pool = list(VERBS.keys())
    if verb_filter and verb_filter in VERBS:
        verb_pool = [verb_filter]

    tense_pool = TENSES if tense_filter == "all" else [tense_filter]

    questions = []
    for _ in range(count * 4):  # oversample to get count unique
        verb = random.choice(verb_pool)
        tense = random.choice(tense_pool)
        person_idx = random.randint(0, 5)
        questions.append((verb, tense, person_idx))

    # deduplicate
    seen = set()
    unique = []
    for q in questions:
        key = (q[0], q[1], q[2])
        if key not in seen:
            seen.add(key)
            unique.append(q)
        if len(unique) == count:
            break

    for i, (verb, tense, pidx) in enumerate(unique, 1):
        person = PERSONS[pidx]
        correct = VERBS[verb][tense][pidx]
        label = TENSE_LABELS.get(tense, tense)

        output.append(f"## Q{i}. **{verb}** — {label} — **{person}**")
        output.append("Answer: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**{person} {correct}**")
        if tense == "subjonctif":
            output.append(f"*Full form: que {person} {correct}*")
        output.append("</details>")
        output.append("")

    print("\n".join(output))


def run_si_clause_drill(count, seed):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 41 French Si-Clause Drill — {timestamp}", f"Seed: {seed} | Count: {count}", ""]

    samples = random.choices(SI_CLAUSES, k=count)
    for i, sc in enumerate(samples, 1):
        output.append(f"## Q{i}. Identify the condition type and complete: **{sc['example_si']}, ___**")
        output.append(f"Condition type: ___ | Si-clause tense: ___ | Main clause tense: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**Type:** {sc['type']}")
        output.append(f"**Si-clause tense:** {sc['si_tense']}")
        output.append(f"**Main clause tense:** {sc['main_tense']}")
        output.append(f"**Example:** {sc['example_si']}, {sc['example_main']}")
        output.append("</details>")
        output.append("")

    print("\n".join(output))


def run_subjunctive_drill(count, seed):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 41 French Subjunctive Drill — {timestamp}", f"Seed: {seed} | Count: {count}", ""]

    samples = random.sample(SUBJUNCTIVE_TRIGGERS, min(count, len(SUBJUNCTIVE_TRIGGERS)))
    for i, (sentence, verb, answer, category) in enumerate(samples, 1):
        output.append(f"## Q{i}. Fill in the blank (infinitive: *{verb}*):")
        output.append(f"**{sentence}**")
        output.append("Answer: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**{answer}** — Category: {category}")
        output.append(f"Full sentence: {sentence.replace('___', answer)}")
        output.append("</details>")
        output.append("")

    print("\n".join(output))


def run_pc_imp_drill(count, seed):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 41 French PC vs Imparfait Drill — {timestamp}", f"Seed: {seed} | Count: {count}", ""]

    samples = random.sample(PC_IMP_SCENARIOS, min(count, len(PC_IMP_SCENARIOS)))
    for i, (sentence, answer, tense_type, rule) in enumerate(samples, 1):
        output.append(f"## Q{i}. Choose the correct past tense:")
        output.append(f"**{sentence}**")
        output.append("PC or Imparfait? Answer: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**{'Passé composé' if tense_type == 'pc' else 'Imparfait'}:** {answer}")
        output.append(f"**Rule:** {rule}")
        output.append("</details>")
        output.append("")

    print("\n".join(output))


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="French verb drill generator")
    parser.add_argument("--count", type=int, default=8, help="Number of questions")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--tense", default="all",
                        choices=["all", "present", "imparfait", "futur", "conditionnel", "subjonctif"],
                        help="Tense filter for conjugation drill")
    parser.add_argument("--verb", default=None, help="Focus on one verb (e.g. être, faire)")
    parser.add_argument("--mode", default="conjugation",
                        choices=["conjugation", "si_clauses", "subjunctive", "pc_vs_imp"],
                        help="Drill mode")
    args = parser.parse_args()

    if args.mode == "conjugation":
        run_conjugation_drill(args.count, args.seed, args.tense, args.verb)
    elif args.mode == "si_clauses":
        run_si_clause_drill(args.count, args.seed)
    elif args.mode == "subjunctive":
        run_subjunctive_drill(args.count, args.seed)
    elif args.mode == "pc_vs_imp":
        run_pc_imp_drill(args.count, args.seed)
