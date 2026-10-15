"""
DA-Shield interactive demo - Group 31, Cyber Security Case Study
Pune Digital Arrest Scam (January 2025)

A menu-driven console program that lets you try both DA-Shield modules:
  1. Module A - check whether a WhatsApp/SMS message looks like a digital-arrest script
  2. Module B - score a bank transfer by a senior citizen (Allow / Verify / Hold)
  3. Module C - replay the reconstructed Pune case through Module B
  4. Run the full evaluation and print the results tables

Run:  python src/dashield_demo.py      (or double-click DA-Shield-Demo.exe)
"""
import sys
import dashield_prototype as dp

LINE = "-" * 72


def ask(prompt, default=None):
    try:
        val = input(prompt).strip()
    except EOFError:
        return default
    return val if val else default


def ask_yes(prompt):
    return (ask(prompt + " (y/n): ", "n") or "n").lower().startswith("y")


def ask_num(prompt, default):
    raw = ask(f"{prompt} [{default}]: ", str(default))
    try:
        return float(str(raw).replace(",", ""))
    except ValueError:
        print("  Not a number, using", default)
        return float(default)


def train_detector():
    print("Training the Module A message detector on the synthetic corpus...")
    corpus = dp.build_corpus()
    model = dp.make_lr().fit([r[0] for r in corpus], [r[1] for r in corpus])
    print(f"Done. Trained on {len(corpus)} messages.\n")
    return model


def check_message(model):
    print(LINE)
    print("MODULE A - Scam-script detector")
    print("Paste or type a message (press Enter on an empty line to go back).")
    while True:
        text = ask("\nMessage: ")
        if not text:
            return
        p = float(model.predict_proba([text])[0, 1])
        if p >= 0.5:
            print(f"  Scam probability: {p:.2f}  ->  WARNING: this looks like a digital-arrest scam script.")
            print("  Real police never arrest anyone on a video call. Do not transfer money. Call family or 1930.")
        else:
            print(f"  Scam probability: {p:.2f}  ->  No digital-arrest pattern detected.")


def score_transfer():
    print(LINE)
    print("MODULE B - Elderly transaction risk engine")
    print("Answer each question (press Enter to accept the value in brackets).\n")
    tx = {
        "age": ask_num("Customer age", 78),
        "amount": ask_num("Transfer amount in Rs", 2500000),
        "avg_90d": ask_num("Customer's average monthly outflow (last 90 days) in Rs", 40000),
        "new_payee": ask_yes("Is the payee newly added?"),
        "payee_acct_age_days": ask_num("Age of payee's bank account in days", 40),
        "liquidated_48h": ask_yes("Was a fixed deposit or mutual fund broken in the last 48 hours?"),
        "high_value_72h": ask_num("Number of high-value transfers in the last 72 hours, including this one", 1),
        "on_call_at_branch": ask_yes("Did staff see the customer on a call or being coached?"),
    }
    score, fired = dp.risk_score(tx)
    print(f"\n  Risk score: {score} / 100")
    print("  Signals that fired:", ", ".join(k for k, v in fired.items() if v) or "none")
    print("  Decision:", dp.action(score))


def replay_case():
    print(LINE)
    print("MODULE C - Replay of the reconstructed Pune case (illustrative schedule, total Rs 4.37 crore)\n")
    print(f"{'Step':<6}{'Day':<6}{'Amount (lakh)':<16}{'Cumulative':<13}{'Score':<8}Decision")
    for r in dp.replay_case():
        print(f"{r['step']:<6}{r['day']:<6}{r['amount_lakh']:<16.0f}{r['cumulative_lakh']:<13.0f}{r['score']:<8}{r['action']}")
    print("\nThe very first transfer is held, so a family member is called before any money leaves.")


def full_evaluation():
    print(LINE)
    print("Running the full evaluation (takes a few seconds)...\n")
    dp.random.seed(dp.SEED); dp.np.random.seed(dp.SEED)  # same starting point as the report run
    summary, _ = dp.leave_family_out(dp.build_corpus())
    print("Module A - leave-family-out results")
    print(f"{'Model':<32}{'Precision':<11}{'Recall':<9}{'F1':<7}")
    for m, r in summary.items():
        print(f"{m:<32}{r['precision']:<11.3f}{r['recall']:<9.3f}{r['f1']:<7.3f}")
    res, _, _ = dp.evaluate_engine(dp.simulate_population())
    h = res["HOLD (>=60)"]
    print(f"\nModule B - {res['n_tx']:,} simulated transfers ({res['n_fraud_tx']} fraudulent)")
    print(f"  Scam transfers held: {h['recall']*100:.1f}%   Genuine transfers delayed: {h['fpr']*100:.2f}%")
    print(f"  Scams stopped at the first instalment: {res['stopped_at_first_installment']} of {res['campaigns']}")


def main():
    print("=" * 72)
    print(" DA-Shield demo  |  Group 31  |  Pune Digital Arrest Scam case study")
    print("=" * 72 + "\n")
    model = train_detector()
    actions = {"1": lambda: check_message(model), "2": score_transfer, "3": replay_case, "4": full_evaluation}
    while True:
        print(LINE)
        print("1. Check a message (Module A)")
        print("2. Score a bank transfer (Module B)")
        print("3. Replay the Pune case (Module C)")
        print("4. Run the full evaluation")
        print("5. Exit")
        choice = ask("Choose 1-5: ", "5")
        if choice in actions:
            actions[choice]()
        else:
            print("Remember: there is no such thing as 'digital arrest'. Report fraud on 1930.")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    if getattr(sys, "frozen", False):  # keep the window open when run as an .exe
        ask("\nPress Enter to close...")
