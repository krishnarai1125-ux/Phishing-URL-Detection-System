Phishing URL Detector (ML Project)

By: Krishna Rai

Reg No: 25BAI11298

This is a tool I put together to help identify if a website link is actually a phishing threat. Instead of just looking up a database of known bad sites, it uses Machine Learning (Logistic Regression) to analyze the URL's structure and predict if it’s dangerous.
What's in this repo?

    threat_scanner.py: This is the main script. It handles all the data loading, training, and has the command-line interface.

    streamlit_app.py: I built this to give the project a proper web UI. It shows the accuracy and a heatmap of the results.

    phishing_site_urls.csv.xz: This is the dataset. I used LZMA compression so the file stays under 7MB, otherwise GitHub wouldn't let me upload the full 30MB raw CSV.

Getting Started
1. Install what's needed

You'll need a few Python libraries to run this. Just run:
PowerShell

pip install -r requirements.txt

2. Running the Terminal Scanner

If you just want a quick check without opening a browser, use the CLI:
PowerShell

# To check one link
python threat_scanner.py "https://suspicious-site.com"

# To enter interactive mode (best for testing many links)
python threat_scanner.py

3. Running the Web Dashboard

To see the confusion matrix and the "Risk Tier" breakdown in your browser:
PowerShell

streamlit run streamlit_app.py

A few notes on how it works

    In-Memory Training: To keep things simple, the model trains from scratch every time you start the app. It takes about 20-30 seconds depending on your CPU, but it means you don't have to mess around with saving/loading .pkl files.

    The Math: I used TF-IDF to turn the URLs into numbers. It basically ignores common stuff like "www" and focuses on words that frequently show up in scams (like "login" or "verify").

    Compression: The code is set up to read the .xz file directly using Pandas, so there's no need to unzip anything yourself.

Krishna Rai | B.Tech CSE (AI/ML) | VIT Bhopal
