"""
40.2 Skeletal System Drill
--------------------------
Generates randomized bone identification and landmark drills.
Usage: python 40.2_skeletal_drill.py --count 10 --seed 42 --region upper_limb
"""

import random
import argparse
from datetime import datetime

BONES = {
    "skull": [
        ("Frontal", "Supraorbital foramen; forms forehead and roof of orbit"),
        ("Parietal (x2)", "Coronal, sagittal, lambdoid sutures"),
        ("Temporal (x2)", "External acoustic meatus, mastoid process, styloid process"),
        ("Occipital", "Foramen magnum, occipital condyles"),
        ("Sphenoid", "Sella turcica (pituitary), greater/lesser wings, pterygoid processes"),
        ("Ethmoid", "Cribriform plate (CN I), crista galli"),
    ],
    "upper_limb": [
        ("Clavicle", "S-shaped; most commonly fractured bone; only bony axial-appendicular link"),
        ("Scapula", "Glenoid cavity (shoulder socket); acromion; coracoid process; spine"),
        ("Humerus", "Greater/lesser tubercles; surgical neck (axillary nerve); medial/lateral epicondyles"),
        ("Radius", "Head (proximal); radial tuberosity; styloid process (distal)"),
        ("Ulna", "Olecranon (proximal); trochlear notch; styloid process (distal)"),
        ("Scaphoid", "Most commonly fractured carpal; anatomical snuffbox; AVN risk"),
        ("Lunate", "Proximal row, 2nd from lateral; lunate dislocation = median nerve compression"),
    ],
    "lower_limb": [
        ("Femur", "Head, neck (126° angle); greater/lesser trochanter; linea aspera; condyles"),
        ("Patella", "Largest sesamoid bone; in quadriceps tendon"),
        ("Tibia", "Tibial plateau; tibial tuberosity; medial malleolus; weight-bearing"),
        ("Fibula", "Lateral malleolus; minimal weight-bearing; most fractured in ankle injuries"),
        ("Calcaneus", "Largest tarsal; Achilles tendon insertion"),
        ("Talus", "Articulates with tibia and fibula (mortise joint)"),
    ],
    "vertebral_column": [
        ("Atlas (C1)", "No vertebral body; ring-shaped; holds skull; dens of axis pivots here"),
        ("Axis (C2)", "Has dens (odontoid process); pivot joint with atlas"),
        ("C7", "Vertebra prominens — largest cervical spinous process, easily palpable"),
        ("T4/T5", "Level of sternal angle; tracheal bifurcation (carina)"),
        ("L4", "Level of iliac crests; aortic bifurcation; LP landmark"),
        ("Sacrum", "5 fused vertebrae; SI joint with ilium; sacral foramina"),
    ],
}

JOINT_QUESTIONS = [
    ("Glenohumeral (shoulder)", "Ball-and-socket", "3", "Flexion/extension, abduction/adduction, rotation"),
    ("Hip (coxal)", "Ball-and-socket", "3", "Flexion/extension, abduction/adduction, rotation"),
    ("Elbow (humeroulnar)", "Hinge", "1", "Flexion/extension only"),
    ("Knee (tibiofemoral)", "Hinge (modified)", "1+", "Primarily flexion/extension; slight rotation when flexed"),
    ("Wrist (radiocarpal)", "Condyloid", "2", "Flexion/extension, abduction/adduction"),
    ("1st CMC (thumb)", "Saddle", "2", "Flexion/extension, abduction/adduction, opposition"),
    ("Atlantoaxial (C1-C2)", "Pivot", "1", "Rotation only (head shaking 'no')"),
    ("Pubic symphysis", "Cartilaginous (fibrocartilage)", "Slight", "Amphiarthrosis; slight movement"),
    ("Skull sutures", "Fibrous", "None", "Synarthrosis"),
]


def run_drill(count: int, seed: int, region: str):
    random.seed(seed)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    output = [f"# 40.2 Skeletal Drill — {timestamp}", f"Seed: {seed} | Count: {count} | Region: {region}", ""]
    
    if region == "joints":
        questions = random.sample(JOINT_QUESTIONS, min(count, len(JOINT_QUESTIONS)))
        for i, (joint, jtype, dof, movement) in enumerate(questions, 1):
            output.append(f"## Q{i}. Classify the **{joint}** joint")
            output.append("- Structural type: ___")
            output.append("- Degrees of freedom: ___")
            output.append("- Movement(s): ___")
            output.append("")
            output.append("<details>")
            output.append("<summary>Show Answer</summary>")
            output.append("")
            output.append(f"- **Structural type:** {jtype}")
            output.append(f"- **Degrees of freedom:** {dof}")
            output.append(f"- **Movements:** {movement}")
            output.append("</details>")
            output.append("")
    else:
        pool = BONES.get(region, [b for bones in BONES.values() for b in bones])
        questions = random.sample(pool, min(count, len(pool)))
        for i, (bone, landmark) in enumerate(questions, 1):
            output.append(f"## Q{i}. Name the key landmark(s) on the **{bone}**")
            output.append("Answer: ___")
            output.append("")
            output.append("<details>")
            output.append("<summary>Show Answer</summary>")
            output.append("")
            output.append(f"**{bone}:** {landmark}")
            output.append("</details>")
            output.append("")
    
    print("\n".join(output))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Skeletal system drill generator")
    parser.add_argument("--count", type=int, default=8, help="Number of questions")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    parser.add_argument("--region", default="all",
                        choices=["skull", "upper_limb", "lower_limb", "vertebral_column", "joints", "all"],
                        help="Body region to focus on")
    args = parser.parse_args()
    run_drill(args.count, args.seed, args.region)
