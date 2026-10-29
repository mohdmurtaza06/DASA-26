"""Generate publication figures from results_summary.json + stats_report.json."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

COLORS = {
    "No defense":     "#e53935",
    "Immediate Q":    "#1e88e5",
    "Anomaly thresh.":"#43a047",
    "Topology":       "#fb8c00",
    "Recovery-aware": "#8e24aa",
}
ORDER = list(COLORS.keys())
SHORT = ["No defense","Immediate Q","Anomaly thresh.","Topology","Recovery-aware"]
KEYS  = ["no_defense","immediate","anomaly","topology","recovery_aware"]

os.makedirs("../figures", exist_ok=True)

with open("../results/results_summary.json") as f:
    s = json.load(f)["overall_by_policy"]

with open("../results/stats_report.json") as f:
    stats = json.load(f)

# Bootstrap half-widths (prefer these)
boot = stats["pooled_bootstrap"]

harm  = [boot[k]["harm_mean"] for k in KEYS]
h_ci  = [boot[k]["harm_bci"]  for k in KEYS]
task  = [boot[k]["task_mean"] for k in KEYS]
t_ci  = [boot[k]["task_bci"]  for k in KEYS]
cost  = [boot[k]["cost_mean"] for k in KEYS]
c_ci  = [boot[k]["cost_bci"]  for k in KEYS]
colors = [COLORS[n] for n in SHORT]

# ── BARS ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(10, 3.2))
x = np.arange(len(SHORT))
w = 0.62

for ax, vals, errs, title, ylabel in [
    (axes[0], harm, h_ci, "Harmful-action rate", ""),
    (axes[1], task, t_ci, "Task success", ""),
    (axes[2], cost, c_ci, "Cost / success", ""),
]:
    bars = ax.bar(x, vals, w, color=colors, zorder=2)
    ax.errorbar(x, vals, yerr=errs, fmt="none", ecolor="k", elinewidth=1.2, capsize=3, zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(SHORT, rotation=30, ha="right", fontsize=7.5)
    ax.set_title(title, fontsize=9)
    ax.grid(axis="y", lw=0.5, alpha=0.5, zorder=0)
    ax.spines[["top","right"]].set_visible(False)

fig.tight_layout(pad=0.8)
fig.savefig("../figures/bars.pdf", bbox_inches="tight", dpi=200)
fig.savefig("../figures/bars.png", bbox_inches="tight", dpi=200)
print("Wrote bars.pdf/png")

# ── PARETO ──────────────────────────────────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(4.5, 3.5))
for i, (name, key) in enumerate(zip(SHORT, KEYS)):
    h_val, h_e = harm[i], h_ci[i]
    t_val, t_e = task[i], t_ci[i]
    ax2.scatter(t_val, h_val, s=90, color=colors[i], zorder=3)
    ax2.errorbar(t_val, h_val,
                 xerr=t_e, yerr=h_e,
                 fmt="none", ecolor=colors[i], elinewidth=1.5, capsize=3, zorder=2, alpha=0.8)

# legend
patches = [mpatches.Patch(color=COLORS[n], label=n) for n in SHORT]
ax2.legend(handles=patches, fontsize=7.5, loc="upper left", framealpha=0.9)
ax2.set_xlabel("Task success rate", fontsize=9)
ax2.set_ylabel("Harmful-action rate", fontsize=9)
ax2.set_title("Security–Utility Trade-off", fontsize=10)
ax2.grid(lw=0.5, alpha=0.4)
ax2.spines[["top","right"]].set_visible(False)

fig2.tight_layout(pad=0.6)
fig2.savefig("../figures/pareto.pdf", bbox_inches="tight", dpi=200)
fig2.savefig("../figures/pareto.png", bbox_inches="tight", dpi=200)
print("Wrote pareto.pdf/png")
