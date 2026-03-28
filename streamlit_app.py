"""
Streamlit UI for the URL threat classifier — easy to screenshot from the browser.
Run: streamlit run streamlit_app.py
"""

import matplotlib.pyplot as plt
import streamlit as st
from sklearn.metrics import ConfusionMatrixDisplay

from threat_scanner import build_and_train_model, classify_url


@st.cache_resource(show_spinner="Training model (first load only; large CSV may take a few minutes)…")
def load_model():
    return build_and_train_model(verbose=False)


st.set_page_config(
    page_title="Phishing URL Scanner",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🛡️ Phishing URL Scanner")
st.caption("TF-IDF + logistic regression — same engine as `threat_scanner.py`")

with st.sidebar:
    st.markdown("### How to screenshot")
    st.markdown(
        "- Use **Win + Shift + S** (Snipping Tool) or **Print Screen**.\n"
        "- Or: browser **⋮ → Cast, save, share → Screenshot** (Edge/Chrome)."
    )
    st.divider()

try:
    model, vectorizer, accuracy, cm, class_labels = load_model()
except FileNotFoundError as e:
    st.error(
        f"Dataset missing. Place `phishing_site_urls.csv` next to the app. ({e})"
    )
    st.stop()

with st.sidebar:
    st.metric("Hold-out accuracy", f"{accuracy * 100:.2f}%")
    st.caption("Trained once and cached for this session.")

st.subheader("Hold-out confusion matrix")
st.caption(
    "20% test split (same seed as CLI). Rows: actual label · Columns: predicted label."
)
fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_labels).plot(
    ax=ax_cm,
    cmap="Blues",
    colorbar=True,
    values_format="d",
)
fig_cm.tight_layout()
st.pyplot(fig_cm)
plt.close(fig_cm)

st.divider()

url_input = st.text_input(
    "URL to analyze",
    placeholder="https://example.com/login",
    help="Paste a full or partial URL string.",
)

col_a, col_b = st.columns(2)
with col_a:
    analyze = st.button("Analyze URL", type="primary", use_container_width=True)
with col_b:
    example = st.button("Try example (safe)", use_container_width=True)

if example:
    target = "https://www.wikipedia.org/wiki/Main_Page"
elif analyze:
    target = (url_input or "").strip()
else:
    target = None

if analyze or example:
    if not target:
        st.warning("Enter a URL first.")
    else:
        r = classify_url(model, vectorizer, target)

        st.subheader("Result")
        st.code(target, language="text")

        c1, c2, c3 = st.columns(3)
        c1.metric("P (phishing)", f"{r['p_phish']:.1f}%")
        c2.metric("P (safe)", f"{r['p_safe']:.1f}%")
        c3.metric("Risk level", r["title"])

        st.progress(
            min(max(r["p_phish"] / 100.0, 0.0), 1.0),
            text=f"Phishing score: {r['p_phish']:.1f}%",
        )

        if r["risk"] == "critical":
            st.error(f"**{r['title']}** — {r['recommendation']}")
        elif r["risk"] == "elevated":
            st.warning(f"**{r['title']}** — {r['recommendation']}")
        else:
            st.success(f"**{r['title']}** — {r['recommendation']}")

st.divider()
st.caption(
    "Educational demo only — not a substitute for browser warnings, reputation feeds, or human review."
)
