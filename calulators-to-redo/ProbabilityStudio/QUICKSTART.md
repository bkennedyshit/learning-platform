---
date: 2026-05-26
title: "Quick Start Guide - Probability Studio"
tags: [learning, probabilitystudio]
status: reference
type: note
---

# Quick Start Guide - Probability Studio

## Installation & First Run

### Windows (Visual Studio)
```cmd
# With Qt installed and in PATH
mkdir build && cd build
cmake .. -G "Visual Studio 17 2022" -A x64
cmake --build . --config Release
cd Release
.\ProbabilityStudio.exe
```

### Linux/Mac
```bash
# Install Qt first: sudo apt-get install qt6-base-dev qt6-charts-dev
mkdir build && cd build
cmake ..
make -j4
./ProbabilityStudio
```

### Qt Creator (Recommended for beginners)
1. Install Qt Creator with Qt Charts module
2. File → Open → Select `ProbabilityStudio.pro` or `CMakeLists.txt`
3. Configure project (select Qt kit)
4. Click green "Run" button ▶

## 📖 Learning Path

### Beginner: Start with Confusion Matrix
**Goal**: Understand why accuracy is misleading

1. Open "Confusion Matrix" tab
2. Click "Examples:" dropdown → Select "Imbalanced Dataset"
   - Accuracy: 98.5% 😊
   - But look closer: Only 5 TP, 5 FN → Missed HALF the positives!
   - **Lesson**: Accuracy lies with imbalanced classes
3. Try "Medical Screening" example
   - High Recall (95%) - Critical: Don't miss diseases
   - Lower Precision - Accept some false alarms
4. Try "Spam Filter" example
   - High Precision (97%) - Don't flag real emails
   - Lower Recall - Some spam gets through
5. **Key Insight**: Different problems need different metrics!

### Intermediate: Cross-Entropy Deep Dive
**Goal**: Understand why we use this loss function

1. Open "Cross-Entropy Loss" tab
2. Mode: "Binary Classification"
3. Set True Label = 1.0 (positive class)
4. Slide Predicted Probability from 0.99 → 0.01
   - Watch loss explode as confidence is wrong
   - At p=0.99: Loss ≈ 0.01 (small penalty)
   - At p=0.01: Loss ≈ 4.6 (HUGE penalty)
5. **Why this matters**: Neural nets learn to avoid confident mistakes
6. Switch to "Categorical" mode
7. Set 3 classes: True [1.0, 0.0, 0.0], Predicted [0.7, 0.2, 0.1]
8. Observe: Only the true class contributes to loss
9. **Export** CSV to analyze further

### Advanced: Central Limit Theorem Proof
**Goal**: See CLT magic happen before your eyes

1. Open "Central Limit Theorem" tab
2. Source Distribution: "Exponential" (very non-normal, skewed)
3. Sample Size: 30
4. Number of Samples: 1000
5. Click "▶ Start Animation"
6. **Watch**: Despite exponential source, sample means form perfect bell curve!
7. Try reducing Sample Size to 5
   - Still approaches normal, but slower
8. Switch source to "Bimodal"
   - Even a weird two-humped distribution becomes normal!
9. **Key Insight**: This is WHY normal distributions are everywhere in nature!
10. Switch mode to "Law of Large Numbers"
11. Start animation
12. **Watch**: Running mean converges to true population mean
13. **This is why**: More data = better estimates

### Expert: Attention Mechanisms
**Goal**: Understand transformers' core operation

1. Open "Attention Weights" tab
2. Load example: "Question Answering"
3. Observe attention focused on "AI" token (score 4.5)
4. Temperature = 1.0 (default)
5. Slide temperature to 0.1
   - Attention becomes sharper (lower entropy)
   - Almost all weight on "AI"
   - This is "hard attention"
6. Slide temperature to 2.0
   - Attention becomes diffuse (higher entropy)
   - More uniform across tokens
   - This is "soft attention"
7. View: "Entropy vs Temperature" graph
   - See exact relationship
   - Low temp → Low entropy (focused)
   - High temp → High entropy (uniform)
8. **Key Insight**: Temperature controls attention sharpness!
9. Load example: "Multi-Modal: Image Regions"
   - See how model attends to salient objects
10. **This is how**: GPT, BERT, Vision Transformers work!

## 🎯 Common Use Cases

### A/B Testing ML Models
**Scenario**: Is your new model significantly better?

1. Hypothesis Testing tab
2. Test Type: "Two-Sample t-test"
3. Sample 1 (Old model): Mean=0.85, Std=0.05, n=100
4. Sample 2 (New model): Mean=0.87, Std=0.05, n=100
5. Significance level: 0.05
6. Click "Calculate Test"
7. Check p-value:
   - p < 0.05: **Significant improvement!** ✅
   - p ≥ 0.05: Not statistically significant ❌
8. Look at confidence interval
9. **Decision**: Reject H₀ = models are equally good

### Comparing Two Probability Distributions
**Scenario**: How different are two models' output distributions?

1. KL Divergence tab
2. Distribution P: Normal(0, 1) - Your reference model
3. Distribution Q: Normal(0.2, 1.2) - New model
4. Observe: D_KL(P||Q) = 0.0233 bits
5. Click "⇄ Swap P ↔ Q"
6. Observe: D_KL(Q||P) = 0.0267 bits (different!)
7. **Interpretation**: Q is slightly different from P
8. Try very different distributions
9. P: Exponential(1), Q: Normal(1, 1)
10. Much larger KL divergence!
11. **Application**: Model distillation, distribution matching

### Optimizing Classification Threshold
**Scenario**: Balance precision and recall

1. Confusion Matrix tab
2. Start with TP=85, FP=15, FN=15, TN=85
   - Precision: 85/100 = 0.85
   - Recall: 85/100 = 0.85
   - F1: 0.85 (balanced)
3. Simulate lowering threshold (more aggressive):
   - TP=95, FP=30, FN=5, TN=70
   - Precision drops: 95/125 = 0.76
   - Recall improves: 95/100 = 0.95
   - F1: 0.84 (slight drop due to imbalance)
4. Simulate raising threshold (more conservative):
   - TP=70, FP=5, FN=30, TN=95
   - Precision improves: 70/75 = 0.93
   - Recall drops: 70/100 = 0.70
   - F1: 0.80
5. **Choose**: Based on your application needs!

## 🔬 Experimental Exploration

### Discover Softmax Temperature Effect
1. Attention tab
2. Create custom tokens: ["A", "B", "C", "D"]
3. Scores: [5.0, 1.0, 1.0, 1.0]
4. Temperature = 1.0
   - A gets ~88% attention
   - Others share ~12%
5. Temperature = 0.1
   - A gets ~99.9% attention (almost one-hot)
6. Temperature = 10.0
   - A gets ~42% attention (much more uniform)
7. **Experiment**: What temperature makes distribution most uniform?
8. Answer: τ → ∞ gives uniform distribution

### Verify Cross-Entropy vs MSE
**Question**: Why use cross-entropy for classification?

1. Cross-Entropy tab
2. Binary mode
3. True label = 1.0
4. Predicted = 0.1
5. Cross-Entropy Loss = 2.30
6. Manual calculation of MSE: (1 - 0.1)² = 0.81
7. **Compare**: CE penalizes more heavily (2.30 vs 0.81)
8. Try predicted = 0.01
9. CE Loss = 4.61 (explodes!)
10. MSE = 0.98 (only slightly worse)
11. **Conclusion**: CE provides stronger gradients when very wrong!

## 💾 Exporting Data

All widgets support CSV export:

1. Set up your scenario
2. Click "Export Data" / "Export Metrics" / "Export Weights"
3. Save CSV file
4. Open in Excel, Python pandas, or R for analysis

Example Python workflow:
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load exported attention weights
df = pd.read_csv('attention_weights.csv')
plt.bar(df['Token'], df['Attention Weight'])
plt.title('Attention Distribution')
plt.show()
```

## 🎓 Teaching Tips

### For Instructors

**Lesson 1: Classification Metrics**
- Start with Confusion Matrix
- Show "Perfect Classifier" example
- Then "Imbalanced Dataset" to shake assumptions
- Discuss precision-recall trade-off
- **Homework**: Students generate their own scenarios

**Lesson 2: Loss Functions**
- Demonstrate Cross-Entropy behavior
- Compare different predicted probabilities
- Discuss gradient implications
- **Exercise**: Plot loss surface for categorical case

**Lesson 3: Distribution Theory**
- Use CLT visualizer with different sources
- Show convergence speed vs sample size
- Connect to LLN
- **Assignment**: Verify CLT with student's own data

**Lesson 4: Hypothesis Testing**
- Live A/B testing demonstration
- Show type I/II error trade-offs
- Discuss p-value interpretation
- **Warning**: p-hacking demonstration (adjust until p < 0.05)

### For Self-Learners

1. **Explore freely** - No wrong answers
2. **Start simple** - Default values are reasonable
3. **Go extreme** - Try edge cases
4. **Compare** - Note relationships between metrics
5. **Export & analyze** - Extend learning in Python/R
6. **Read explanations** - They explain the "why"

## 🐛 Troubleshooting

**Qt Charts not found**
```bash
# Ubuntu/Debian
sudo apt-get install libqt6charts6-dev

# Fedora
sudo dnf install qt6-qtcharts-devel

# macOS
brew install qt6
```

**Application crashes on animation**
- Reduce sample count
- Lower animation speed (modify timer interval in code)

**Values seem wrong**
- Check scaling factors (e.g., √d_k in attention)
- Verify temperature setting
- Reset to defaults

## 📚 Further Reading

After using Probability Studio, deepen understanding:

- **Cross-Entropy**: "Information Theory" by Cover & Thomas
- **KL Divergence**: "Pattern Recognition and Machine Learning" by Bishop
- **CLT**: "Statistical Inference" by Casella & Berger  
- **Hypothesis Testing**: "Statistical Methods" by Freedman et al.
- **Confusion Matrix**: "Evaluation Metrics for ML" papers
- **Attention**: "Attention Is All You Need" (Vaswani et al., 2017)

## 🎯 Next Steps

After mastering Probability Studio:

1. **Implement**: Code these from scratch in Python/NumPy
2. **Apply**: Use in your ML projects
3. **Extend**: Add ROC curves, Bayesian inference, etc.
4. **Contribute**: Share improvements
5. **Teach**: Help others understand!

---

**Happy Exploring! 🚀**

*"The best way to understand is to play."*

---

## Related Notes
- [[BUILD]] - Shared probabilitystudio/learning focus
- [[DELIVERY_SUMMARY]] - Shared probabilitystudio/learning focus
- [[IMPLEMENTATION_COMPLETE]] - Shared probabilitystudio/learning focus
- [[PROJECT_OVERVIEW]] - Shared probabilitystudio/learning focus
- [[SVG Design for learning]] - Related learning topic
