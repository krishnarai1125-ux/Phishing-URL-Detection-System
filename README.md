# Phishing URL Threat Scanner

A small command-line tool that trains a **TF-IDF + logistic regression** classifier on labeled URLs, reports hold-out accuracy, and scores new URLs as phishing or safe with probability estimates.

## Requirements

- Python 3.10+ recommended (tested with Python 3.14)
- Dependencies: `pandas`, `scikit-learn`, `streamlit` (for the web UI)

## Setup

From the project folder:

```bash
pip install -r requirements.txt
```

On Windows, if `python` is not on your PATH, use the launcher:

```powershell
py -3 -m pip install -r requirements.txt
```

## Data

Place `phishing_site_urls.csv` in the same directory as `threat_scanner.py`. The file must include columns:

- `URL` — the URL string  
- `Label` — `bad` (phishing) or `good` (safe)

The script resolves this path from the script location, so you can run it from any working directory.

## Usage

**Interactive mode** (train, then prompt for URLs until you type `exit` or press Ctrl+C):

```bash
python threat_scanner.py
```

**Single URL** (train once, print one result, then exit):

```bash
python threat_scanner.py "https://example.com/some/path"
```

Windows example:

```powershell
py -3 threat_scanner.py "https://www.google.com"
```

### Web UI (Streamlit) — good for screenshots

From the project folder, start the app (it opens in your browser, usually at http://localhost:8501):

```powershell
py -3 -m streamlit run streamlit_app.py
```

The model trains **once** on first load (cached for the session). Use **Analyze URL** or **Try example (safe)** to fill the result panel, then capture the window with Snipping Tool (**Win + Shift + S**) or your browser’s screenshot feature. The page also shows a **hold-out confusion matrix** (same 80/20 split as the CLI).

## How it works

1. Load and label the CSV (`bad` → `PHISHING`, `good` → `SAFE`).  
2. Split 80% train / 20% test.  
3. Tokenize each URL on non-word characters, remove English stop words in the tokenizer, then apply TF-IDF.  
4. Train `LogisticRegression` and print validation accuracy.  
5. For each query URL, show estimated P(phishing), P(safe), and a simple risk tier (critical / elevated / minimal).  
6. After training, print a **confusion matrix** on the terminal (rows = true label, columns = predicted); Streamlit plots the same matrix as a heatmap.

Training time depends on dataset size; very large CSV files may take several minutes and significant RAM.

## Limitations

This is a **statistical URL-pattern** model, not a live browser or DNS check. It can misclassify novel or obfuscated URLs. Use as a helper signal alongside other security practices, not as the only control.
