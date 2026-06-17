"""
40.4 Cranial Nerve Drill
------------------------
Drills all 12 cranial nerves: name, number, type, function, clinical palsy.
Usage: python 40.4_cranial_nerve_drill.py --count 6 --seed 42 --mode function
"""

import random
import argparse
from datetime import datetime

CRANIAL_NERVES = [
    {
        "number": "I", "name": "Olfactory", "type": "Sensory",
        "function": "Smell (olfaction)",
        "clinical": "Anosmia (loss of smell); cribriform plate fracture; olfactory groove meningioma",
        "test": "Ask patient to identify common odors with eyes closed"
    },
    {
        "number": "II", "name": "Optic", "type": "Sensory",
        "function": "Vision",
        "clinical": "Visual field defects (hemianopias); optic neuritis (MS); papilledema (↑ICP)",
        "test": "Snellen chart; confrontational visual fields; fundoscopy"
    },
    {
        "number": "III", "name": "Oculomotor", "type": "Motor",
        "function": "4 of 6 extraocular muscles (SR, IR, MR, IO), levator palpebrae (eyelid), pupil constriction (PS)",
        "clinical": "CN III palsy: 'down and out' eye, ptosis, dilated unreactive pupil. Cause: PComm aneurysm (surgical emergency) or uncal herniation",
        "test": "Pupil reactivity; H-pattern eye movement test"
    },
    {
        "number": "IV", "name": "Trochlear", "type": "Motor",
        "function": "Superior oblique muscle → infraduction of adducted eye (looking down and in)",
        "clinical": "Vertical diplopia; patient tilts head contralaterally to compensate. Longest intracranial course → most vulnerable to TBI",
        "test": "Cover test; ask patient to look down and in"
    },
    {
        "number": "V", "name": "Trigeminal", "type": "Both",
        "function": "Face sensation (V1 ophthalmic, V2 maxillary, V3 mandibular); motor to muscles of mastication (V3 only)",
        "clinical": "Trigeminal neuralgia (tic douloureux); jaw deviates toward weak side (pterygoids); corneal reflex afferent limb (V1)",
        "test": "Light touch 3 divisions; corneal reflex; jaw clench/open against resistance"
    },
    {
        "number": "VI", "name": "Abducens", "type": "Motor",
        "function": "Lateral rectus (LR6) → abduction (eye looks laterally)",
        "clinical": "CN VI palsy: eye cannot abduct → horizontal diplopia on lateral gaze; 'false localizing sign' with ↑ICP",
        "test": "Ask patient to look laterally (abduct eye)"
    },
    {
        "number": "VII", "name": "Facial", "type": "Both",
        "function": "Muscles of facial expression; taste anterior 2/3 tongue (chorda tympani); lacrimation and salivation (submandibular/sublingual via chorda tympani; lacrimal via greater petrosal)",
        "clinical": "Bell's palsy (LMN): entire ipsilateral face paralyzed including forehead. UMN stroke: contralateral lower face only (forehead spared). Parotid tumor → LMN palsy.",
        "test": "Raise eyebrows, close eyes tight, smile, puff cheeks; taste testing"
    },
    {
        "number": "VIII", "name": "Vestibulocochlear", "type": "Sensory",
        "function": "Hearing (cochlear division); balance and head position (vestibular division)",
        "clinical": "Sensorineural hearing loss; vertigo; acoustic neuroma (schwannoma of CN VIII at CPA) → unilateral SNHL + tinnitus",
        "test": "Rinne's test (bone vs. air conduction); Weber's test; Dix-Hallpike for BPPV"
    },
    {
        "number": "IX", "name": "Glossopharyngeal", "type": "Both",
        "function": "Taste posterior 1/3 tongue; sensation from pharynx, middle ear, carotid body/sinus; parotid gland (via Jacobson's nerve)",
        "clinical": "Gag reflex (afferent limb, CN IX; efferent CN X); glossopharyngeal neuralgia",
        "test": "Gag reflex; touch posterior pharyngeal wall"
    },
    {
        "number": "X", "name": "Vagus", "type": "Both",
        "function": "Parasympathetic to thoracic + abdominal viscera; motor to pharynx/larynx; visceral sensation; taste epiglottis",
        "clinical": "Uvula deviates AWAY from lesion side; hoarseness (recurrent laryngeal nerve injury — during thyroid surgery); unilateral palatal droop",
        "test": "Say 'Ahh' — uvula position; voice quality; gag reflex efferent limb"
    },
    {
        "number": "XI", "name": "Accessory", "type": "Motor",
        "function": "Sternocleidomastoid (ipsilateral head rotation, i.e., turns head to opposite side) and trapezius (shoulder shrug)",
        "clinical": "Shoulder drop; inability to shrug ipsilateral shoulder or turn head against resistance. Injured during posterior triangle neck surgery.",
        "test": "Shrug shoulders against resistance; turn head against resistance"
    },
    {
        "number": "XII", "name": "Hypoglossal", "type": "Motor",
        "function": "All intrinsic and most extrinsic tongue muscles (except palatoglossus — CN X)",
        "clinical": "LMN lesion: tongue deviates TOWARD side of lesion (weak side pushes less). UMN lesion: tongue deviates AWAY from lesion. Fasciculations in LMN lesion.",
        "test": "Protrude tongue; note deviation"
    },
]

MODES = ["function", "clinical", "name_from_number", "number_from_name", "full"]


def run_drill(count: int, seed: int, mode: str):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    sample = random.sample(CRANIAL_NERVES, min(count, 12))
    
    output = [f"# 40.4 Cranial Nerve Drill — {timestamp}", f"Seed: {seed} | Count: {count} | Mode: {mode}", ""]
    
    for i, cn in enumerate(sample, 1):
        if mode == "name_from_number":
            output.append(f"## Q{i}. What is cranial nerve **{cn['number']}**?")
            output.append("Name: ___ | Type: ___ | Function: ___")
        elif mode == "number_from_name":
            output.append(f"## Q{i}. What number is the **{cn['name']}** nerve?")
            output.append("Number: ___ | Type: ___ | Function: ___")
        elif mode == "function":
            output.append(f"## Q{i}. CN {cn['number']} — {cn['name']}: Describe its function")
            output.append("Function: ___")
        elif mode == "clinical":
            output.append(f"## Q{i}. CN {cn['number']} — {cn['name']}: What are the clinical palsy signs?")
            output.append("Clinical: ___")
        else:  # full
            output.append(f"## Q{i}. CN {cn['number']}: Name, type, function, clinical palsy, and clinical test")
            output.append("Name: ___ | Type: ___ | Function: ___ | Clinical: ___ | Test: ___")
        
        output.append("")
        output.append("<details>")
        output.append("<summary>Show Answer</summary>")
        output.append("")
        output.append(f"- **CN {cn['number']} — {cn['name']}**")
        output.append(f"- **Type:** {cn['type']}")
        output.append(f"- **Function:** {cn['function']}")
        output.append(f"- **Clinical:** {cn['clinical']}")
        output.append(f"- **Test:** {cn['test']}")
        output.append("</details>")
        output.append("")
    
    print("\n".join(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cranial nerve drill generator")
    parser.add_argument("--count", type=int, default=6, help="Number of nerves to drill")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--mode", default="full", choices=MODES, help="Drill mode")
    args = parser.parse_args()
    run_drill(args.count, args.seed, args.mode)
