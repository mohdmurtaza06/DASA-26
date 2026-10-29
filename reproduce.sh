#!/usr/bin/env bash
# One-command reproduction for the DASA'26 paper
# Tested on Python ≥ 3.10, TeX Live 2023+
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Step 1: Run canonical 800-run campaign ==="
cd "$SCRIPT_DIR/src"
python3 -I run_experiments.py

echo ""
echo "=== Step 2: Compute bootstrap CIs and sensitivity analysis ==="
python3 -I stats_analysis.py

echo ""
echo "=== Step 3: Generate figures ==="
python3 -I make_figures.py

echo ""
echo "=== Step 4: Compile LaTeX (2 passes) ==="
cd "$SCRIPT_DIR/tex"
pdflatex -interaction=nonstopmode main.tex > /dev/null
pdflatex -interaction=nonstopmode main.tex

echo ""
echo "=== Done. Outputs: ==="
echo "  results/raw_results.csv         (800 rows)"
echo "  results/results_summary.json    (means and CIs)"
echo "  results/stats_report.json       (bootstrap, paired, sensitivity)"
echo "  figures/pareto.pdf, bars.pdf    (publication figures)"
echo "  tex/main.pdf                    (compiled paper, ≤5 pages)"
