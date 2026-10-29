#!/bin/bash
set -e
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "Running experiments..."
python src/run_experiments.py
echo "Running stats analysis..."
python src/stats_analysis.py
echo "Generating figures..."
python src/make_figures.py
echo "Compiling paper..."
cd tex && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex
echo "Done. Outputs in results/, figures/, and tex/main.pdf"
