# DA-Shield: Detecting and Stopping Digital Arrest Fraud

**Cyber Security Case Study (Batch 2023-27, Semester VII) - Group 31**
Department of Electronics & Telecommunication Engineering | Faculty: Dr. Mangal Singh

**Topic:** Pune Digital Arrest Scam (January 2025) targeting a 78-year-old woman, resulting in Rs. 4.37 crore loss through WhatsApp and phone impersonation.

**GitHub repository:** https://github.com/flasharav/G31-DA-Shield

| PRN | Student Name |
|---|---|
| 23070123002 | Aamir Ayaan Quraishi |
| 23070123026 | Arav Upadhyay |
| 23070123122 | Shivendra Dwivedi |
| 23070123164 | Pranjal Panwar |

---

## 1. What this project does

In a "digital arrest" scam, fraudsters impersonate police or CBI/ED officers, keep the victim on a WhatsApp video call and persuade them to transfer their savings. There is no such thing as a digital arrest in Indian law.

We reconstructed the Pune case as a six-stage attack chain and proposed **DA-Shield**, a five-layer defence (telecom, messaging, banking, response, awareness). This repository contains the working prototype of the two layers we built and tested:

| Module | What it does | Method |
|---|---|---|
| **A - Scam-script detector** | Reads a WhatsApp/SMS message and says whether it looks like a digital-arrest script | TF-IDF (word + character n-grams) with logistic regression, compared with Naive Bayes and a keyword-rule baseline |
| **B - Elderly transaction risk engine** | Scores each high-value transfer by a customer aged 60+ and decides Allow / Verify / Hold 24 h with a call to a trusted family contact | Explainable weighted rules (7 signals, score out of 100), compared with a random forest |
| **C - Case replay** | Runs a reconstructed timeline of the Rs. 4.37 crore Pune case through Module B | Uses Module B |

## 2. Folder structure

```
G31-DA-Shield/
|-- README.md                  <- this file (how to run the project)
|-- requirements.txt           <- Python libraries needed
|-- run_windows.bat            <- one-click run on Windows
|-- run_mac_linux.sh           <- one-click run on macOS / Linux
|-- build_exe_windows.bat      <- builds the .exe on a Windows PC
|-- src/
|   |-- dashield_prototype.py  <- data generation, Modules A, B, C and full evaluation
|   |-- make_figures.py        <- draws the figures used in the report
|   `-- dashield_demo.py       <- interactive menu demo (this is what the .exe runs)
|-- outputs/
|   |-- results.json           <- every number reported in the report
|   |-- engine_scores.npy      <- Module B scores (used for Fig. 5)
|   `-- figures/               <- fig1 to fig6 (PNG)
|-- exe/
|   `-- DA-Shield-Demo.exe     <- ready-to-run Windows program (see section 5)
|-- docs/
|   |-- G31.pdf                <- case study report
|   `-- G31_Presentation.pptx  <- presentation used in the video
`-- .github/workflows/
    `-- build-exe.yml          <- builds the Windows .exe automatically on GitHub
```

## 3. Requirements

- Python 3.10 or newer (tested on Python 3.13) - download from https://www.python.org/downloads/ and tick **"Add python.exe to PATH"** during installation on Windows.
- Libraries: `numpy`, `scikit-learn`, `matplotlib` (installed automatically by the run scripts). Tested with numpy 2.5, scikit-learn 1.9 and matplotlib 3.11.

## 4. How to run

### Option A - one click
- **Windows:** double-click `run_windows.bat`
- **macOS / Linux:** open Terminal in this folder and run `bash run_mac_linux.sh`

The script installs the libraries, runs the full evaluation, redraws the figures and then opens the interactive demo.

### Option B - step by step (any operating system)
Open a terminal / command prompt **in this folder** and run:

```bash
pip install -r requirements.txt          # 1. install libraries (use pip3 on macOS)
python src/dashield_prototype.py         # 2. run Modules A, B, C; writes outputs/results.json
python src/make_figures.py               # 3. draw figures into outputs/figures/
python src/dashield_demo.py              # 4. open the interactive demo
```
(On macOS use `python3` instead of `python`.)

### Option C - the .exe (Windows, no Python needed)
Double-click `exe/DA-Shield-Demo.exe`. It may take 10 to 20 seconds to start the first time. If Windows SmartScreen shows a warning, click **More info -> Run anyway** (the program is unsigned because it is a student project).

### Using the demo
```
1. Check a message (Module A)       -> type any WhatsApp/SMS text, get a scam probability
2. Score a bank transfer (Module B) -> answer 8 questions, get the risk score and decision
3. Replay the Pune case (Module C)  -> see each of the 6 transfers being held
4. Run the full evaluation          -> prints the results tables from the report
5. Exit
```
Example message to try: `You are under digital arrest. Stay on video call, do not tell anyone, transfer your FD to the RBI safe account.`

## 5. Building the .exe yourself

- **On GitHub (no Windows PC needed):** open the **Actions** tab of this repository -> **Build Windows exe** -> **Run workflow**. After 3 to 5 minutes, open the finished run and download the **DA-Shield-Demo-windows** artifact.
- **On a Windows PC:** double-click `build_exe_windows.bat`. The program appears in the `exe` folder.

## 6. Expected results

Running `src/dashield_prototype.py` uses a fixed random seed (31), so it reproduces the report's numbers exactly:

| Module A (leave-family-out, 980 test predictions) | Precision | Recall | F1 |
|---|---|---|---|
| Keyword-rule baseline | 0.789 | 0.573 | 0.664 |
| TF-IDF + Naive Bayes | 0.715 | 0.998 | 0.833 |
| **TF-IDF + Logistic Regression** | **0.751** | **0.955** | **0.841** |

| Module B (22,605 simulated transfers, 793 fraudulent) | Value |
|---|---|
| Scam transfers held (score 60+) | 95.0% |
| Genuine transfers delayed | 1.07% |
| Scam campaigns stopped at the first instalment | 122 of 150 |
| Pune case replay | all 6 transfers held, including the first (Rs. 25 lakh) |

## 7. Methodology in brief

1. **Attack reconstruction:** the Pune case was broken into six stages (reconnaissance, pretext call, escalation, isolation, extraction, laundering) using official data and comparable Pune cases.
2. **Synthetic data:** no public dataset of Indian digital-arrest messages exists, so `dashield_prototype.py` generates 910 messages from 13 families (6 scam types and 7 normal types, including real police warnings as hard negatives) and 22,605 transfers from 4,000 genuine senior customers and 150 scam campaigns. No real personal or banking data is used.
3. **Module A evaluation:** leave-family-out cross-validation. In each of 7 rounds, one whole scam family and one whole normal family are hidden from training, so every test message is a script the model has never seen.
4. **Module B evaluation:** precision, recall and false-positive rate at the Verify (40) and Hold (60) thresholds, campaign-level stopping, and comparison with a random forest on customers held out from training.
5. **Case replay:** a reconstructed six-transfer schedule totalling Rs. 4.37 crore is scored transfer by transfer.

Full details are in `docs/G31.pdf`.

## 8. Limitations

The data is synthetic and the case timeline is reconstructed from comparable cases, so real-world performance will be lower than reported. Module A reads text only, not voice calls.

---
*If you receive a "digital arrest" call: hang up, call your family, and report it on the National Cyber Crime Helpline **1930** or at https://cybercrime.gov.in.*
