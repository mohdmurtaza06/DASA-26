# Recovery-Aware Containment Policies for LLM Multi-Agent Systems under Uncertain Compromise

**Author:** Mohammed Murtaza Tajammul, Muffakham Jah College of Engineering and Technology, Hyderabad, India  
**Contact:** murtazamohd006@gmail.com  
**Conference:** DASA'26 (International Hybrid Conference on Decision Aid Sciences and Applications, Dec 27–29, 2026, Bangkok)

---

## Quick start — reproduce everything in one command

```bash
bash reproduce.sh
```

Expected output: 800-row CSV, summary JSON, stats report, two figures (PDF+PNG), and compiled paper PDF.

---

## Directory layout

```
FINAL_DASA26_SOURCE/
├── src/
│   ├── simulation.py          # Core simulator (deterministic, seeded)
│   ├── run_experiments.py     # Canonical 800-run campaign (single source of truth)
│   ├── stats_analysis.py      # Bootstrap CIs, paired diffs, sensitivity sweep
│   └── make_figures.py        # Generate pareto.pdf and bars.pdf
├── tex/
│   ├── main.tex               # Final LaTeX source
│   └── IEEEtran.cls           # IEEE conference template class
├── results/                   # Generated outputs (created by reproduce.sh)
│   ├── raw_results.csv        # 800 run-level rows
│   ├── results_summary.json   # Means and 95% bootstrap CIs by policy
│   └── stats_report.json      # Paired bootstrap, per-attack, sensitivity
├── figures/                   # Generated figures (created by reproduce.sh)
│   ├── pareto.pdf / .png
│   └── bars.pdf / .png
├── reproduce.sh               # One-command reproduction script
├── requirements.txt
├── README.md                  # This file
├── validation_report.md
└── reproducibility_report.md
```

---

## Requirements

- Python ≥ 3.10
- numpy, pandas, matplotlib  
- LaTeX: texlive-publishers (IEEEtran), texlive-science, texlive-base
- pdflatex (any recent TeX Live)

Install Python dependencies:
```bash
pip install -r requirements.txt
```

---

## Canonical campaign parameters

| Parameter | Value |
|-----------|-------|
| Policies | no_defense, immediate, anomaly, topology, recovery_aware |
| Attack types | prompt_injection, memory_poison, intermittent, collusion |
| Seeds | 5000–5039 (40 per cell) |
| Total runs | 800 (5 × 4 × 40) |
| Detection sensitivity | 0.70 |
| False-positive rate | 0.08 |
| Propagation probability | 0.35 |
| Horizon | 40 steps |
| Agents | 5 |

---

## Expected table values (pooled means ± 95% bootstrap CI)

| Policy | Harmful rate | Task success | Cost/success |
|--------|-------------|--------------|--------------|
| No defense | 3.475 ± 0.192 | 1.000 ± 0.000 | 139.0 ± 7.8 |
| Immediate | 0.018 ± 0.005 | 0.838 ± 0.039 | 4.3 ± 1.0 |
| Anomaly | 0.121 ± 0.027 | 0.713 ± 0.046 | 17.8 ± 3.3 |
| Topology | 1.343 ± 0.078 | 0.934 ± 0.012 | 71.2 ± 4.1 |
| Recovery-aware | 0.080 ± 0.010 | 0.448 ± 0.033 | 215.6 ± 13.4 |

---

## Notes

- Bootstrap CIs use B=5000 resamples, seed fixed at 2024.
- Paired bootstrap over 160 matched (seed, attack) pairs confirms RA−Immediate task-success gap = −0.390 (95% CI [−0.435, −0.344]).
- Sensitivity sweep (FPR 0.04–0.24) and propagation probability sweep (0.20–0.65) are in `stats_report.json`.
- No benign (no-attack) condition; no sensitivity sweep in the main campaign.
