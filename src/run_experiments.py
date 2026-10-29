"""
Canonical experimental campaign for the Recovery-Aware Containment paper.

This script is the single source of truth. It produces exactly the 800-run
evaluation reported in the paper:

  5 policies × 4 attack types × 40 seeds = 800 runs
  Seeds: 5000 .. 5039
  Detection sensitivity = 0.70, FPR = 0.08, propagation = 0.35
  No benign condition, no sensitivity sweep.

Usage:
  cd src && python3 run_experiments.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
import json
import time
from simulation import run_trial

POLICIES = ["no_defense", "immediate", "anomaly", "topology", "recovery_aware"]
ATTACKS = ["prompt_injection", "memory_poison", "intermittent", "collusion"]
N_SEEDS = 40
SEED_BASE = 5000          # seeds 5000 .. 5039
SENS = 0.70
FPR = 0.08
PROP = 0.35

def main():
    os.makedirs("../results", exist_ok=True)
    start = time.time()
    results = []

    print("=== Canonical campaign: 5 policies × 4 attacks × 40 seeds = 800 runs ===")
    print(f"Seeds: {SEED_BASE} .. {SEED_BASE + N_SEEDS - 1}")
    print(f"Config: sens={SENS}, fpr={FPR}, prop={PROP}")

    for policy in POLICIES:
        for attack in ATTACKS:
            for s in range(N_SEEDS):
                seed = SEED_BASE + s
                r = run_trial(seed, policy, attack, SENS, FPR, PROP)
                results.append(r)
        print(f"  finished policy={policy}  (running total {len(results)})")

    assert len(results) == 800, f"Expected 800 rows, got {len(results)}"

    df = pd.DataFrame(results)
    out_csv = "../results/raw_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv}  rows={len(df)}")

    def ci95(series):
        return float(1.96 * series.std(ddof=1) / np.sqrt(len(series)))

    overall = {}
    for policy in POLICIES:
        sub = df[df.policy == policy]
        assert len(sub) == 160
        overall[policy] = {
            "n": int(len(sub)),
            "harmful_mean": float(sub.harmful_action_rate.mean()),
            "harmful_ci": ci95(sub.harmful_action_rate),
            "prop_mean": float(sub.propagation_rate.mean()),
            "prop_ci": ci95(sub.propagation_rate),
            "task_mean": float(sub.task_success.mean()),
            "task_ci": ci95(sub.task_success),
            "cost_mean": float(sub.cost_per_success.mean()),
            "cost_ci": ci95(sub.cost_per_success),
            "fqr_step_mean": float(sub.false_quarantines.mean() / 40.0),
            "rollback_mean": float(sub.rollback_count.mean()),
        }

    summary = {
        "overall_by_policy": overall,
        "n_seeds": N_SEEDS,
        "seed_base": SEED_BASE,
        "seed_range": [SEED_BASE, SEED_BASE + N_SEEDS - 1],
        "n_attacks": len(ATTACKS),
        "attacks": ATTACKS,
        "policies": POLICIES,
        "runs_per_policy": 160,
        "total_attack_runs": 800,
        "detection_sensitivity": SENS,
        "false_positive_rate": FPR,
        "propagation_prob": PROP,
        "aggregation": "mean over 160 independent runs (4 attacks × 40 seeds)",
        "ci": "95% CI = 1.96 * sample_std / sqrt(n), n=160 run-level observations",
        "runtime_sec": time.time() - start,
    }

    with open("../results/results_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\n=== OVERALL (160 runs/policy) ===")
    for p, v in overall.items():
        print(f"{p:18s} harm={v['harmful_mean']:.4f}±{v['harmful_ci']:.4f}  "
              f"task={v['task_mean']:.4f}±{v['task_ci']:.4f}  "
              f"cost={v['cost_mean']:.1f}±{v['cost_ci']:.1f}")

    print(f"\nDone in {time.time()-start:.1f}s. Total rows: {len(df)}")
    return df, summary

if __name__ == "__main__":
    main()
