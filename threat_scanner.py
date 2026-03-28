import pandas as pd
import re
import sys
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

class Log:
    OK = '\033[92m'
    WARN = '\033[93m'
    CRIT = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def print_header():
    print(f"{Log.BOLD}")
    print("-" * 50)
    print(" URL Threat Classification Engine v1.0")
    print(" Uses TF-IDF & Logistic Regression")
    print("-" * 50)
    print(f"{Log.RESET}")

def tokenize_url(url):
    """Splits URL string into tokens; drops English stop words (custom analyzer)."""
    raw = [t for t in re.split(r"\W+", str(url).lower()) if t]
    return [t for t in raw if t not in ENGLISH_STOP_WORDS]


SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_PATH = SCRIPT_DIR / "phishing_site_urls.csv"

def build_and_train_model(*, verbose: bool = True):
    if verbose:
        print_header()

    if not DATASET_PATH.exists():
        if verbose:
            print(
                f"{Log.CRIT}[ERROR] Dataset not found at {DATASET_PATH}.{Log.RESET}"
            )
        raise FileNotFoundError(str(DATASET_PATH))

    if verbose:
        print(f"[INFO] Ingesting dataset: {DATASET_PATH.name}...")
    df = pd.read_csv(DATASET_PATH)

    df["Label"] = df["Label"].map({"bad": "PHISHING", "good": "SAFE"})
    df.rename(columns={"URL": "url", "Label": "label"}, inplace=True)

    if verbose:
        print("[INFO] Performing train/test split (80/20)...")
    x_train, x_test, y_train, y_test = train_test_split(
        df["url"], df["label"], test_size=0.2, random_state=42
    )

    if verbose:
        print(
            "[INFO] Extracting features via TF-IDF Vectorization... "
            "(This may take a moment)"
        )
    vectorizer = TfidfVectorizer(analyzer=tokenize_url)
    tfidf_train = vectorizer.fit_transform(x_train)
    tfidf_test = vectorizer.transform(x_test)

    if verbose:
        print("[INFO] Fitting Logistic Regression classifier...")
    model = LogisticRegression(max_iter=2000)
    model.fit(tfidf_train, y_train)

    if verbose:
        print("[INFO] Validating model accuracy...")
    predictions = model.predict(tfidf_test)
    score = accuracy_score(y_test, predictions)
    labels = list(model.classes_)
    cm = confusion_matrix(y_test, predictions, labels=labels)

    if verbose:
        print(
            f"{Log.OK}[SUCCESS] Model trained. "
            f"Validation Accuracy: {score * 100:.2f}%{Log.RESET}\n"
        )
        print("[INFO] Confusion matrix — rows: true label, columns: predicted")
        print(pd.DataFrame(cm, index=labels, columns=labels).to_string())
        print()

    return model, vectorizer, float(score), cm, labels


def classify_url(model, vectorizer, target_url):
    """Return scores and labels for a single URL (for CLI, Streamlit, APIs)."""
    classes = list(model.classes_)
    idx_phish = classes.index("PHISHING")
    idx_safe = classes.index("SAFE")

    vec_input = vectorizer.transform([target_url])
    probabilities = model.predict_proba(vec_input)[0]

    p_phish = float(probabilities[idx_phish] * 100)
    p_safe = float(probabilities[idx_safe] * 100)

    if p_phish >= 75.0:
        risk = "critical"
        title = "CRITICAL RISK"
        rec = "Block immediately. Matches known phishing signatures."
    elif p_phish >= 30.0:
        risk = "elevated"
        title = "ELEVATED RISK"
        rec = "Proceed with caution. URL exhibits suspicious token patterns."
    else:
        risk = "minimal"
        title = "MINIMAL RISK"
        rec = "URL syntax is consistent with safe domains."

    return {
        "p_phish": p_phish,
        "p_safe": p_safe,
        "risk": risk,
        "title": title,
        "recommendation": rec,
    }


def print_classification(model, vectorizer, target_url):
    r = classify_url(model, vectorizer, target_url)
    if r["risk"] == "critical":
        status = f"{Log.CRIT}{r['title']}{Log.RESET}"
    elif r["risk"] == "elevated":
        status = f"{Log.WARN}{r['title']}{Log.RESET}"
    else:
        status = f"{Log.OK}{r['title']}{Log.RESET}"

    print("-" * 50)
    print(f" Classification : {status}")
    print(f" P(Phishing)    : {r['p_phish']:.2f}%")
    print(f" P(Safe)        : {r['p_safe']:.2f}%")
    print(f" Recommendation : {r['recommendation']}")
    print("-" * 50 + "\n")


def run_scanner(model, vectorizer):
    print(f"{Log.BOLD}--- Interactive Analysis Mode ---{Log.RESET}")
    print("Enter a URL to analyze. Type 'exit' to terminate.\n")

    while True:
        try:
            target_url = input("target_url> ")
        except KeyboardInterrupt:
            print("\nTerminating process.")
            break

        if target_url.lower() in ["exit", "quit"]:
            print("Terminating process.")
            break

        if not target_url.strip():
            continue

        print_classification(model, vectorizer, target_url)


if __name__ == "__main__":
    try:
        trained_model, trained_vectorizer, _acc, _cm, _labels = build_and_train_model()
    except FileNotFoundError:
        sys.exit(1)
    if len(sys.argv) > 1:
        url_arg = " ".join(sys.argv[1:]).strip()
        if url_arg:
            print_classification(trained_model, trained_vectorizer, url_arg)
    else:
        run_scanner(trained_model, trained_vectorizer)
