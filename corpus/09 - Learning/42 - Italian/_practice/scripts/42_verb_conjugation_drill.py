"""
42 — Italian Verb Conjugation Drill
-------------------------------------
Usage:
    python 42_verb_conjugation_drill.py --count 10 --seed 42 --tense present
    python 42_verb_conjugation_drill.py --count 8 --mode pp_aux
    python 42_verb_conjugation_drill.py --count 6 --mode congiuntivo
    python 42_verb_conjugation_drill.py --count 8 --mode pp_vs_imp

Modes:
    conjugation  — verb + tense + person → correct form
    pp_aux       — avere or essere as passato prossimo auxiliary?
    congiuntivo  — produce the correct congiuntivo form
    pp_vs_imp    — passato prossimo or imperfetto for context sentence
"""

import random
import argparse
from datetime import datetime

VERBS = {
    "parlare": {
        "present":     ["parlo", "parli", "parla", "parliamo", "parlate", "parlano"],
        "imperfetto":  ["parlavo", "parlavi", "parlava", "parlavamo", "parlavate", "parlavano"],
        "futuro":      ["parlerò", "parlerai", "parlerà", "parleremo", "parlerete", "parleranno"],
        "condizionale": ["parlerei", "parleresti", "parlerebbe", "parleremmo", "parlereste", "parlerebbero"],
        "cong_pres":   ["parli", "parli", "parli", "parliamo", "parliate", "parlino"],
        "cong_imp":    ["parlassi", "parlassi", "parlasse", "parlassimo", "parlaste", "parlassero"],
        "aux": "avere", "pp": "parlato",
    },
    "finire": {
        "present":     ["finisco", "finisci", "finisce", "finiamo", "finite", "finiscono"],
        "imperfetto":  ["finivo", "finivi", "finiva", "finivamo", "finivate", "finivano"],
        "futuro":      ["finirò", "finirai", "finirà", "finiremo", "finirete", "finiranno"],
        "condizionale": ["finirei", "finiresti", "finirebbe", "finiremmo", "finireste", "finirebbero"],
        "cong_pres":   ["finisca", "finisca", "finisca", "finiamo", "finiate", "finiscano"],
        "cong_imp":    ["finissi", "finissi", "finisse", "finissimo", "finiste", "finissero"],
        "aux": "avere", "pp": "finito",
    },
    "vedere": {
        "present":     ["vedo", "vedi", "vede", "vediamo", "vedete", "vedono"],
        "imperfetto":  ["vedevo", "vedevi", "vedeva", "vedevamo", "vedevate", "vedevano"],
        "futuro":      ["vedrò", "vedrai", "vedrà", "vedremo", "vedrete", "vedranno"],
        "condizionale": ["vedrei", "vedresti", "vedrebbe", "vedremmo", "vedreste", "vedrebbero"],
        "cong_pres":   ["veda", "veda", "veda", "vediamo", "vediate", "vedano"],
        "cong_imp":    ["vedessi", "vedessi", "vedesse", "vedessimo", "vedeste", "vedessero"],
        "aux": "avere", "pp": "visto",
    },
    "essere": {
        "present":     ["sono", "sei", "è", "siamo", "siete", "sono"],
        "imperfetto":  ["ero", "eri", "era", "eravamo", "eravate", "erano"],
        "futuro":      ["sarò", "sarai", "sarà", "saremo", "sarete", "saranno"],
        "condizionale": ["sarei", "saresti", "sarebbe", "saremmo", "sareste", "sarebbero"],
        "cong_pres":   ["sia", "sia", "sia", "siamo", "siate", "siano"],
        "cong_imp":    ["fossi", "fossi", "fosse", "fossimo", "foste", "fossero"],
        "aux": "essere", "pp": "stato",
    },
    "avere": {
        "present":     ["ho", "hai", "ha", "abbiamo", "avete", "hanno"],
        "imperfetto":  ["avevo", "avevi", "aveva", "avevamo", "avevate", "avevano"],
        "futuro":      ["avrò", "avrai", "avrà", "avremo", "avrete", "avranno"],
        "condizionale": ["avrei", "avresti", "avrebbe", "avremmo", "avreste", "avrebbero"],
        "cong_pres":   ["abbia", "abbia", "abbia", "abbiamo", "abbiate", "abbiano"],
        "cong_imp":    ["avessi", "avessi", "avesse", "avessimo", "aveste", "avessero"],
        "aux": "avere", "pp": "avuto",
    },
    "andare": {
        "present":     ["vado", "vai", "va", "andiamo", "andate", "vanno"],
        "imperfetto":  ["andavo", "andavi", "andava", "andavamo", "andavate", "andavano"],
        "futuro":      ["andrò", "andrai", "andrà", "andremo", "andrete", "andranno"],
        "condizionale": ["andrei", "andresti", "andrebbe", "andremmo", "andreste", "andrebbero"],
        "cong_pres":   ["vada", "vada", "vada", "andiamo", "andiate", "vadano"],
        "cong_imp":    ["andassi", "andassi", "andasse", "andassimo", "andaste", "andassero"],
        "aux": "essere", "pp": "andato",
    },
    "fare": {
        "present":     ["faccio", "fai", "fa", "facciamo", "fate", "fanno"],
        "imperfetto":  ["facevo", "facevi", "faceva", "facevamo", "facevate", "facevano"],
        "futuro":      ["farò", "farai", "farà", "faremo", "farete", "faranno"],
        "condizionale": ["farei", "faresti", "farebbe", "faremmo", "fareste", "farebbero"],
        "cong_pres":   ["faccia", "faccia", "faccia", "facciamo", "facciate", "facciano"],
        "cong_imp":    ["facessi", "facessi", "facesse", "facessimo", "faceste", "facessero"],
        "aux": "avere", "pp": "fatto",
    },
    "venire": {
        "present":     ["vengo", "vieni", "viene", "veniamo", "venite", "vengono"],
        "imperfetto":  ["venivo", "venivi", "veniva", "venivamo", "venivate", "venivano"],
        "futuro":      ["verrò", "verrai", "verrà", "verremo", "verrete", "verranno"],
        "condizionale": ["verrei", "verresti", "verrebbe", "verremmo", "verreste", "verrebbero"],
        "cong_pres":   ["venga", "venga", "venga", "veniamo", "veniate", "vengano"],
        "cong_imp":    ["venissi", "venissi", "venisse", "venissimo", "veniste", "venissero"],
        "aux": "essere", "pp": "venuto",
    },
    "volere": {
        "present":     ["voglio", "vuoi", "vuole", "vogliamo", "volete", "vogliono"],
        "imperfetto":  ["volevo", "volevi", "voleva", "volevamo", "volevate", "volevano"],
        "futuro":      ["vorrò", "vorrai", "vorrà", "vorremo", "vorrete", "vorranno"],
        "condizionale": ["vorrei", "vorresti", "vorrebbe", "vorremmo", "vorreste", "vorrebbero"],
        "cong_pres":   ["voglia", "voglia", "voglia", "vogliamo", "vogliate", "vogliano"],
        "cong_imp":    ["volessi", "volessi", "volesse", "volessimo", "voleste", "volessero"],
        "aux": "avere", "pp": "voluto",
    },
    "potere": {
        "present":     ["posso", "puoi", "può", "possiamo", "potete", "possono"],
        "imperfetto":  ["potevo", "potevi", "poteva", "potevamo", "potevate", "potevano"],
        "futuro":      ["potrò", "potrai", "potrà", "potremo", "potrete", "potranno"],
        "condizionale": ["potrei", "potresti", "potrebbe", "potremmo", "potreste", "potrebbero"],
        "cong_pres":   ["possa", "possa", "possa", "possiamo", "possiate", "possano"],
        "cong_imp":    ["potessi", "potessi", "potesse", "potessimo", "poteste", "potessero"],
        "aux": "avere", "pp": "potuto",
    },
    "dovere": {
        "present":     ["devo", "devi", "deve", "dobbiamo", "dovete", "devono"],
        "imperfetto":  ["dovevo", "dovevi", "doveva", "dovevamo", "dovevate", "dovevano"],
        "futuro":      ["dovrò", "dovrai", "dovrà", "dovremo", "dovrete", "dovranno"],
        "condizionale": ["dovrei", "dovresti", "dovrebbe", "dovremmo", "dovreste", "dovrebbero"],
        "cong_pres":   ["debba", "debba", "debba", "dobbiamo", "dobbiate", "debbano"],
        "cong_imp":    ["dovessi", "dovessi", "dovesse", "dovessimo", "doveste", "dovessero"],
        "aux": "avere", "pp": "dovuto",
    },
    "partire": {
        "present":     ["parto", "parti", "parte", "partiamo", "partite", "partono"],
        "imperfetto":  ["partivo", "partivi", "partiva", "partivamo", "partivate", "partivano"],
        "futuro":      ["partirò", "partirai", "partirà", "partiremo", "partirete", "partiranno"],
        "condizionale": ["partirei", "partiresti", "partirebbe", "partiremmo", "partireste", "partirebbero"],
        "cong_pres":   ["parta", "parta", "parta", "partiamo", "partiate", "partano"],
        "cong_imp":    ["partissi", "partissi", "partisse", "partissimo", "partiste", "partissero"],
        "aux": "essere", "pp": "partito",
    },
}

PERSONS = ["io", "tu", "lui/lei", "noi", "voi", "loro"]
TENSES = ["present", "imperfetto", "futuro", "condizionale"]
TENSE_LABELS = {
    "present": "Presente",
    "imperfetto": "Imperfetto",
    "futuro": "Futuro semplice",
    "condizionale": "Condizionale presente",
    "cong_pres": "Congiuntivo presente",
    "cong_imp": "Congiuntivo imperfetto",
}

CONGIUNTIVO_TRIGGERS = [
    ("Penso che lui ___ stanco.", "essere", 2, "cong_pres", "credere/pensare — doubt"),
    ("Voglio che tu ___ qui.", "venire", 1, "cong_pres", "volere — will"),
    ("Benché ___ tardi, continuiamo.", "essere", 2, "cong_pres", "benché — concession"),
    ("È importante che voi ___ in tempo.", "arrivare (→ arriviate)", 4, "cong_pres", "impersonal — necessity"),
    ("Speravo che lui ___.", "venire", 2, "cong_imp", "past main → cong. imperfetto"),
    ("Prima che tu ___, voglio dirti una cosa.", "partire", 1, "cong_pres", "prima che — conjunction"),
    ("Sebbene ___ difficile, ci provo.", "essere", 2, "cong_pres", "sebbene — concession"),
    ("Ho paura che non ___ farcela.", "potere", 2, "cong_pres", "emotion — fear"),
]

PP_IMP_SCENARIOS = [
    ("Da bambino, ___ (giocare) a calcio ogni domenica.", "giocavo", "imp", "Habitual past — imperfetto"),
    ("Ieri, ___ (mangiare) una pizza fantastica.", "ho mangiato", "pp", "Specific completed event — passato prossimo"),
    ("___ (dormire) quando ha suonato il campanello.", "Dormivo", "imp", "Interrupted ongoing action — imperfetto"),
    ("L'anno scorso ___ (andare) a Roma tre volte.", "sono andato/a", "pp", "Counted events — passato prossimo"),
    ("Faceva freddo e ___ (essere) nuvoloso.", "era", "imp", "Background description — imperfetto"),
    ("Ho incontrato Marco mentre ___ (camminare) in centro.", "camminava", "imp", "Interrupted action — imperfetto"),
    ("Mi ___ (alzare) alle sei e ___ (uscire) subito.", "sono alzato/a / sono uscito/a", "pp", "Sequence of events — passato prossimo"),
    ("Da piccola, ___ (avere) paura del buio.", "aveva", "imp", "Ongoing past state — imperfetto"),
]


def run_conjugation_drill(count, seed, tense_filter):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 42 Italian Conjugation Drill — {timestamp}",
              f"Seed: {seed} | Count: {count} | Tense: {tense_filter}", ""]
    tense_pool = TENSES if tense_filter == "all" else [tense_filter]
    verb_pool = list(VERBS.keys())
    seen, unique = set(), []
    for _ in range(count * 8):
        v, t, p = random.choice(verb_pool), random.choice(tense_pool), random.randint(0, 5)
        key = (v, t, p)
        if key not in seen:
            seen.add(key)
            unique.append(key)
        if len(unique) == count:
            break
    for i, (verb, tense, pidx) in enumerate(unique, 1):
        correct = VERBS[verb][tense][pidx]
        label = TENSE_LABELS.get(tense, tense)
        output.append(f"## Q{i}. **{verb}** — {label} — **{PERSONS[pidx]}**")
        output.append("Answer: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**{PERSONS[pidx]} {correct}**")
        output.append("</details>")
        output.append("")
    print("\n".join(output))


def run_pp_aux_drill(count, seed):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 42 Italian Passato Prossimo Auxiliary Drill — {timestamp}",
              f"Seed: {seed} | Count: {count}", ""]
    verbs = random.sample(list(VERBS.keys()), min(count, len(VERBS)))
    for i, verb in enumerate(verbs, 1):
        aux = VERBS[verb]["aux"]
        pp = VERBS[verb]["pp"]
        output.append(f"## Q{i}. **{verb}** — Which auxiliary? avere or essere?")
        output.append("Auxiliary: ___ | Past participle: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**Auxiliary:** {aux}")
        output.append(f"**Past participle:** {pp}")
        output.append(f"**Example (io, m.):** {'sono' if aux == 'essere' else 'ho'} {pp}{'(o)' if aux == 'essere' else ''}")
        output.append("</details>")
        output.append("")
    print("\n".join(output))


def run_congiuntivo_drill(count, seed):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 42 Italian Congiuntivo Drill — {timestamp}",
              f"Seed: {seed} | Count: {count}", ""]
    samples = random.sample(CONGIUNTIVO_TRIGGERS, min(count, len(CONGIUNTIVO_TRIGGERS)))
    for i, (sentence, verb, pidx, tense_key, category) in enumerate(samples, 1):
        correct = VERBS.get(verb.split(" ")[0], {}).get(tense_key, ["?"] * 6)[pidx] if "→" not in verb else verb.split("→")[1].strip().rstrip(")")
        output.append(f"## Q{i}. Fill in the blank (verb: *{verb.split(' ')[0]}*, {PERSONS[pidx]}):")
        output.append(f"**{sentence}**")
        output.append("Answer: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**{correct}** — Category: {category}")
        output.append("</details>")
        output.append("")
    print("\n".join(output))


def run_pp_imp_drill(count, seed):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    output = [f"# 42 Italian Passato Prossimo vs Imperfetto Drill — {timestamp}",
              f"Seed: {seed} | Count: {count}", ""]
    samples = random.sample(PP_IMP_SCENARIOS, min(count, len(PP_IMP_SCENARIOS)))
    for i, (sentence, answer, tense_type, rule) in enumerate(samples, 1):
        output.append(f"## Q{i}. Choose the correct past tense:")
        output.append(f"**{sentence}**")
        output.append("PP or Imperfetto? Answer: ___")
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"**{'Passato prossimo' if tense_type == 'pp' else 'Imperfetto'}:** {answer}")
        output.append(f"**Rule:** {rule}")
        output.append("</details>")
        output.append("")
    print("\n".join(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Italian verb drill generator")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--tense", default="all",
                        choices=["all", "present", "imperfetto", "futuro", "condizionale"])
    parser.add_argument("--mode", default="conjugation",
                        choices=["conjugation", "pp_aux", "congiuntivo", "pp_vs_imp"])
    args = parser.parse_args()
    if args.mode == "conjugation":
        run_conjugation_drill(args.count, args.seed, args.tense)
    elif args.mode == "pp_aux":
        run_pp_aux_drill(args.count, args.seed)
    elif args.mode == "congiuntivo":
        run_congiuntivo_drill(args.count, args.seed)
    elif args.mode == "pp_vs_imp":
        run_pp_imp_drill(args.count, args.seed)
