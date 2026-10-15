import json, os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

NAVY, BLUE, LIGHT, BLACK = "#0B2E6F", "#1F5FBF", "#A9C4EE", "#000000"
plt.rcParams.update({"font.family": "serif", "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"], "font.size": 11, "axes.edgecolor": BLACK,
                     "axes.labelcolor": BLACK, "xtick.color": BLACK, "ytick.color": BLACK,
                     "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 220})
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
FIG = os.path.join(OUT, "figures"); os.makedirs(FIG, exist_ok=True)
R = json.load(open(os.path.join(OUT, "results.json")))

def label_bars(ax, bars, fmt):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), fmt(b.get_height()), ha="center", va="bottom", fontsize=10)

# Fig 1 - national trend (MHA, Rajya Sabha reply 12-03-2025): two panels, one axis each
yrs = ["2022", "2023", "2024"]; cases = [39925, 60676, 123672]; loss = [91.14, 339.03, 1935.51]
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
b = ax[0].bar(yrs, cases, color=BLUE, width=0.55); label_bars(ax[0], b, lambda v: f"{int(v):,}")
ax[0].set_title("Reported incidents", fontsize=11); ax[0].set_ylim(0, 140000)
b = ax[1].bar(yrs, loss, color=NAVY, width=0.55); label_bars(ax[1], b, lambda v: f"Rs {v:,.0f} cr")
ax[1].set_title("Amount defrauded (Rs crore)", fontsize=11); ax[1].set_ylim(0, 2200)
for a in ax: a.yaxis.grid(True, color=LIGHT, lw=0.6); a.set_axisbelow(True)
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig1_trend.png")); plt.close(fig)

# Fig 2 - attack chain
def chain(fname, stages, title_w=11.5, h=2.6):
    fig, ax = plt.subplots(figsize=(title_w, h)); ax.axis("off"); n = len(stages)
    w, gap = (0.98 - 0.02 * (n - 1)) / n, 0.02
    for i, (head, body) in enumerate(stages):
        x = 0.01 + i * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 0.08), w, 0.84, boxstyle="round,pad=0.005,rounding_size=0.02",
                                    fc="white", ec=NAVY, lw=1.4, transform=ax.transAxes))
        ax.add_patch(FancyBboxPatch((x, 0.70), w, 0.22, boxstyle="round,pad=0.005,rounding_size=0.02",
                                    fc=NAVY, ec=NAVY, lw=1.4, transform=ax.transAxes))
        ax.text(x + w / 2, 0.81, head, color="white", ha="center", va="center", fontsize=10, weight="bold", transform=ax.transAxes)
        ax.text(x + w / 2, 0.40, body, color=BLACK, ha="center", va="center", fontsize=8.8, transform=ax.transAxes, wrap=True)
        if i < n - 1:
            ax.annotate("", xy=(x + w + gap, 0.5), xytext=(x + w, 0.5), xycoords="axes fraction",
                        arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.2))
    fig.savefig(fname, bbox_inches="tight"); plt.close(fig)

chain(os.path.join(FIG, "fig2_attack_chain.png"), [
    ("1. Reconnaissance", "Leaked Aadhaar,\nphone and age data;\nelderly person\nliving alone"),
    ("2. Pretext call", "Spoofed or\ninternational call as\nTRAI / courier /\npolice official"),
    ("3. Escalation", "Hand-off to fake\nCBI / ED officer;\nmoney-laundering\nor drugs 'case'"),
    ("4. Isolation", "WhatsApp video\n'digital arrest';\nsecrecy oath; forged\ncourt documents"),
    ("5. Extraction", "FD / MF broken;\nRTGS to 'safe\nverification account'\nin instalments"),
    ("6. Laundering", "Mule accounts,\nlayering, cash-out,\ncrypto / overseas\ntransfer")])

chain(os.path.join(FIG, "fig3_dashield.png"), [
    ("Layer 1: Telecom", "Spoof-call blocking\n'International call'\nlabel; Chakshu\nreporting"),
    ("Layer 2: Messaging", "Module A: on-device\nscript detector for\nWhatsApp / SMS /\ncall transcripts"),
    ("Layer 3: Banking", "Module B: elderly\ntransaction risk\nengine; 24 h hold +\ntrusted contact"),
    ("Layer 4: Response", "1930 golden-hour\nreporting; CFCFRMS\nlien on mule\naccounts"),
    ("Layer 5: Awareness", "Family protocol;\n'no digital arrest\nin law' messaging;\nbranch scripts")], title_w=10.5)

# Fig 4 - Module A results (leave-family-out)
mA = R["module_a"]; models = list(mA); mets = ["precision", "recall", "f1"]
x = np.arange(len(mets)); w = 0.26; fills = [(LIGHT, None), (BLUE, None), (NAVY, None)]
fig, ax = plt.subplots(figsize=(7.5, 3.6))
for i, m in enumerate(models):
    vals = [mA[m][k] for k in mets]
    bars = ax.bar(x + (i - 1) * w, vals, w - 0.02, color=fills[i][0], edgecolor=BLACK, lw=0.6,
                  hatch="///" if i == 0 else None, label=m)
    label_bars(ax, bars, lambda v: f"{v:.2f}")
ax.set_xticks(x, ["Precision", "Recall", "F1-score"]); ax.set_ylim(0, 1.12); ax.set_ylabel("Score")
ax.yaxis.grid(True, color=LIGHT, lw=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False, loc="upper center", ncol=3, fontsize=9, bbox_to_anchor=(0.5, 1.13))
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig4_moduleA.png")); plt.close(fig)

# Fig 5 - Module B score distribution
s, y = np.load(os.path.join(OUT, "engine_scores.npy")); bins = np.arange(-2.5, 103, 5)
fig, ax = plt.subplots(figsize=(7.5, 3.4))
ax.hist(s[y == 0], bins=bins, color=LIGHT, edgecolor=BLACK, lw=0.4, label="Legitimate (elderly customers)")
ax.hist(s[y == 1], bins=bins, color=NAVY, edgecolor=BLACK, lw=0.4, alpha=0.9, label="Digital-arrest instalments")
ax.set_yscale("log"); ax.set_xlabel("Risk score (0-100)"); ax.set_ylabel("Transactions (log scale)")
for thr, name in [(40, "VERIFY"), (60, "HOLD")]:
    ax.axvline(thr, color=BLACK, ls="--", lw=1); ax.text(thr + 1, ax.get_ylim()[1] * 0.5, name, fontsize=9)
ax.legend(frameon=False, fontsize=9, loc="upper right"); fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig5_moduleB.png")); plt.close(fig)

# Fig 6 - case replay
C = R["module_c"]; days = [0] + [c["day"] for c in C]; cum = [0] + [c["cumulative_lakh"] for c in C]
held = [0] + [C[0]["amount_lakh"] * 0] * len(C)
fig, ax = plt.subplots(figsize=(7.5, 3.3))
ax.step(days, cum, where="post", color=NAVY, lw=2, label="Without DA-Shield (reconstructed)")
ax.step(days, held, where="post", color=BLUE, lw=2, ls="--", label="With DA-Shield: first transfer held")
ax.fill_between(days, held, cum, step="post", color=LIGHT, alpha=0.5)
ax.text(days[-1] - 0.2, cum[-1] + 12, "Rs 437 lakh", ha="right", fontsize=10)
for d, c in zip(days[1:], C):
    ax.plot(d, c["cumulative_lakh"], "o", color=NAVY, ms=5)
ax.set_xlabel("Day of the scam"); ax.set_ylabel("Cumulative loss (Rs lakh)"); ax.set_ylim(0, 500)
ax.yaxis.grid(True, color=LIGHT, lw=0.6); ax.set_axisbelow(True); ax.legend(frameon=False, fontsize=9, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fig6_case_replay.png")); plt.close(fig)
print("ok")
