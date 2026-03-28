Project Statement & Declaration

Project: Phishing URL Detection using Machine Learning

Developer: Krishna Rai

Reg No: 25BAI11298
1. Problem Statement

In today's digital landscape, phishing remains the most common entry point for cyberattacks. While blacklists are the traditional defense, they fail against new, "zero-day" URLs. My goal for this project was to move away from reactive security and build a proactive tool. This system uses the structural features of a URL—its tokens, length, and character distribution—to predict whether it is safe or malicious before it is ever reported to a central database.
2. Project Objectives

To successfully complete this project, I defined the following core milestones:

    Efficient Data Handling: Using LZMA (.xz) compression to manage a high-volume dataset within GitHub’s storage constraints.

    Feature Engineering: Implementing a custom tokenizer and TF-IDF vectorization to convert raw URL strings into weighted numerical features.

    Optimized Inference: Developing a Logistic Regression model that provides nearly instantaneous classification for a seamless user experience.

    Accessibility: Creating both a Command Line Interface (CLI) for technical audits and a Streamlit dashboard for general users.

3. Technical Approach

I chose a feature-based approach over a simple lookup system. By analyzing the "DNA" of the URL through TF-IDF, the model learns to identify high-risk tokens (like "secure-login" or "verify-bank") that are statistically common in phishing attempts. The choice of Logistic Regression ensures the tool remains lightweight enough to run on standard consumer hardware without the need for specialized GPUs.
4. Declaration of Originality

I, Krishna Rai, hereby declare that this project, titled "Phishing URL Threat Scanner," is my original work. It has been developed as part of my B.Tech CSE (AI/ML) curriculum. All external libraries used (such as Scikit-Learn, Pandas, and Streamlit) have been properly documented, and the core classification logic and implementation are my own.

Date: March 28, 2026

Candidate Signature: Krishna Rai

    Create a table of top 5 phishing indicato
