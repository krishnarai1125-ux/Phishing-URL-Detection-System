Fake News Classification CLI

Developer: Krishna Rai

Registration: 25BAI11298

A command-line application for detecting fake news using machine learning. This tool uses TF-IDF features and a Logistic Regression classifier to evaluate text authenticity.
Installation & Setup

    Clone the repository:
    Bash

    git clone <your-repo-link>
    cd fake_news_project

    Install dependencies:
    Bash

    pip install -r requirements.txt

    Extract Dataset:
    The datasets are compressed to comply with repository size limits. Please extract data/datasets.zip into the data/ directory so that True.csv and Fake.csv are visible to the application.

Usage
Training the Model

Train the classifier on your local data to generate the necessary .joblib artifacts:
Bash

python main.py train

Making Predictions

To test a specific news headline:
Bash

python main.py predict --text "Your headline here"

Web Interface

For a visual experience, launch the Streamlit dashboard:
Bash

streamlit run streamlit_app.py
