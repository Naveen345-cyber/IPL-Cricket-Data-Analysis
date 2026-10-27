# 🏏 IPL Cricket Data Analysis & Machine Learning Studio (2020–2024)

[![Live Web Application](https://img.shields.io/badge/🌐%20Live%20Website-Click%20Here%20to%20Open-success?style=for-the-badge&logo=googlechrome&logoColor=white)](https://naveen345-cyber.github.io/IPL-Cricket-Data-Analysis/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> An end-to-end data analytics and **Introduction to Machine Learning (IML)** project analyzing **5 IPL seasons** (2020–2024), **300 matches**, and **6,600 player innings**. Featuring supervised classification, regression models, feature interpretability, and a live reactive web dashboard.

---

## ⚡ 1st Priority Core Assets & Quick Links

| 🎯 Asset | 📁 Location / Link | 📝 Description |
|:---|:---|:---|
| 🌐 **Live Web Application** | **[👉 Open Live Website](https://naveen345-cyber.github.io/IPL-Cricket-Data-Analysis/)** | Hosted on **GitHub Pages** — interactive filters, live match predictor & data explorer |
| 🤖 **Train Models Code (IML)** | [`train_models.py`](train_models.py) | **Complete supervised ML pipeline**: 5-fold CV, 4 classification models, 3 regression models & Gini feature importance |
| 📊 **Dataset 1 (Matches)** | [`data/ipl_matches.csv`](data/ipl_matches.csv) | 300 IPL matches (2020–2024) with venues, toss decisions, teams, scores & winners |
| 📊 **Dataset 2 (Player Stats)** | [`data/ipl_player_stats.csv`](data/ipl_player_stats.csv) | 6,600 player performance records (runs, wickets, strike rate, boundaries) |
| 📓 **Jupyter Notebook** | [`IPL_Cricket_Data_Analysis.ipynb`](IPL_Cricket_Data_Analysis.ipynb) | Exploratory data analysis, Chi-Square hypothesis testing & visualization pipeline |
| 📈 **Serialized ML Metrics** | [`ml_metrics_summary.json`](ml_metrics_summary.json) | Cross-validation scores, test metrics, ROC-AUC, RMSE & feature rankings |

```bash
# ⚡ Quick Start: Train all ML models in one command
python train_models.py

# ⚡ Quick Start: Launch the interactive web app locally
python -m http.server 8080
# then open: http://localhost:8080
```

---

## 📑 Table of Contents
- [⚡ 1st Priority Core Assets & Quick Links](#-1st-priority-core-assets--quick-links)
- [🌐 Live Website & GitHub Pages Deployment](#-live-website--github-pages-deployment)
- [Project Overview](#-project-overview)
- [Machine Learning (IML) Pipeline](#-machine-learning-iml-pipeline)
  - [1. Data Splitting & Cross-Validation](#1-data-splitting--cross-validation)
  - [2. Supervised Classification (Match Winner Prediction)](#2-supervised-classification-match-winner-prediction)
  - [3. Supervised Regression (1st Innings Total Prediction)](#3-supervised-regression-1st-innings-total-prediction)
  - [4. Model Interpretability & Feature Importance](#4-model-interpretability--feature-importance)
- [Key Insights & Statistical Findings](#-key-insights--statistical-findings)
  - [Franchise Win Rates](#franchise-win-rates-20202024)
  - [Toss Impact & Chi-Square Hypothesis Test](#toss-impact--hypothesis-testing)
  - [Venue Profiles & Scoring](#venue-scoring-profiles)
  - [Individual Records](#top-individual-performers)
- [Interactive Dashboard Features](#-interactive-dashboard-features)
- [Project Structure](#-project-structure)
- [How to Run the Project](#-how-to-run-the-project)
- [Technologies Used](#-technologies-used)

---

## 🌐 Live Website & GitHub Pages Deployment

The interactive dashboard is deployed and viewable in any modern web browser:

🔗 **Live URL**: **[https://naveen345-cyber.github.io/IPL-Cricket-Data-Analysis/](https://naveen345-cyber.github.io/IPL-Cricket-Data-Analysis/)**

### How GitHub Pages is Enabled:
1. Go to repository **Settings** on GitHub (`https://github.com/Naveen345-cyber/IPL-Cricket-Data-Analysis/settings/pages`).
2. Under **Build and deployment** > **Source**, choose **Deploy from a branch**.
3. Under **Branch**, select `main` and folder `/ (root)`.
4. Click **Save**. Within 1–2 minutes, GitHub will publish the site at `https://naveen345-cyber.github.io/IPL-Cricket-Data-Analysis/`.


---

## 🌟 Project Overview

This repository transforms raw Indian Premier League ball-by-ball and match metadata into actionable machine learning models and data insights:
1. **Exploratory Data Analysis (EDA)**: Comprehensive evaluation of team win consistency, toss advantages, boundary frequency, and pitch behavior.
2. **Inferential Statistics**: Chi-square tests of independence testing the hypothesis of toss bias.
3. **Machine Learning Models**:
   - **Supervised Classification**: Predicting match winners given franchises, venue, and toss decisions.
   - **Supervised Regression**: Predicting 1st innings total score.
   - **Cross-Validation**: 5-Fold Stratified CV preventing data leakage and overfitting.
   - **Interpretability (IML)**: Feature Importance analysis determining key match deciders.
4. **Interactive Dashboard**: A standalone single-page web app with live filters, interactive match predictor, and paginated data explorer.

---

## 🤖 Machine Learning (IML) Pipeline

All models are trained in [`train_models.py`](train_models.py) and documented in the Jupyter notebook [`IPL_Cricket_Data_Analysis.ipynb`](IPL_Cricket_Data_Analysis.ipynb).

### 1. Data Splitting & Cross-Validation
- **Random 80/20 Stratified Split**: 240 training matches, 60 held-out test matches with stratified class labels.
- **5-Fold Stratified Cross-Validation**: Applied across all classification models for variance estimation.
- **5-Fold Cross-Validation**: Applied across all regression models using root mean squared error.
- **Temporal Split**: Trained on 2020–2023 (240 matches) and tested out-of-season on 2024 (60 matches) to evaluate seasonal generalization.

---

### 2. Supervised Classification: Match Winner Prediction
Predicting whether **Team 1 defeats Team 2** given team identities, venue, toss winner, toss decision, and franchise win differential.

| Model | 5-Fold CV Accuracy | Test Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Gradient Boosting** | 47.5% (±4.8%) | **53.3%** | **55.6%** | 48.4% | **51.7%** | **0.50** |
| **Logistic Regression** | 49.2% (±2.1%) | **51.7%** | 53.3% | 51.6% | **52.5%** | **0.50** |
| **Random Forest** | 45.4% (±2.4%) | 48.3% | 50.0% | 48.4% | 49.2% | 0.45 |
| **Decision Tree** | **49.6% (±4.6%)** | 46.7% | 48.7% | **61.3%** | **54.3%** | **0.51** |

- **Confusion Matrix (Random Forest Test Set)**: Generated in [`images/ml_confusion_matrix.png`](images/ml_confusion_matrix.png).
- **ROC Curves**: Plotted across all 4 classifiers in [`images/ml_roc_curve.png`](images/ml_roc_curve.png).
- **Model Comparison Visual**: Bar chart comparing Accuracy, F1, and ROC-AUC in [`images/ml_models_comparison.png`](images/ml_models_comparison.png).

---

### 3. Supervised Regression: 1st Innings Total Prediction
Predicting the first-innings total score of Team 1 given host stadium and lineup configurations.

| Model | 5-Fold CV RMSE | Test MAE (runs) | Test RMSE (runs) | Test $R^2$ |
|:---|:---:|:---:|:---:|:---:|
| **Ridge Regression** | **25.12 runs** | **22.13 runs** | **27.59 runs** | **-0.077** |
| **Linear Regression** | 25.39 runs | 22.22 runs | 27.67 runs | -0.084 |
| **Random Forest Regressor** | 25.97 runs | 23.55 runs | 28.37 runs | -0.139 |

- **Actual vs Predicted Plot**: Visualized in [`images/ml_regression_actual_vs_pred.png`](images/ml_regression_actual_vs_pred.png).
- *Insight*: T20 match totals possess high situational variance, resulting in an average error margin of ~22 runs.

---

### 4. Model Interpretability & Feature Importance (IML)
Using Random Forest Gini impurity reduction to understand which variables most strongly dictate match outcomes:

| Rank | Feature | Gini Importance | Interpretation |
|:---:|:---|:---:|:---|
| 1 | `win_pct_diff` | **0.2376** | **Historical win percentage differential** between both franchises is the single strongest factor. |
| 2 | `toss_decision_field` | **0.0703** | Opting to bowl/field first provides a notable situational advantage. |
| 3 | `toss_winner_is_team1` | **0.0628** | Whether Team 1 secured the toss decision. |
| 4 | `venue_Wankhede Stadium` | **0.0397** | High-scoring batting ground dynamics in Mumbai. |
| 5 | `venue_Rajiv Gandhi Intl Stadium`| **0.0396** | Hyderabad pitch conditions influencing match outcome. |

- **Feature Importance Plot**: Visualized in [`images/ml_feature_importance.png`](images/ml_feature_importance.png).

---

## 📊 Key Insights & Statistical Findings

### Franchise Win Rates (2020–2024)

| Rank | Franchise | Matches Played | Wins | Losses | Win % |
|:---:|:---|:---:|:---:|:---:|:---:|
| 🥇 | **Royal Challengers Bengaluru (RCB)** | 75 | 41 | 34 | **54.7%** |
| 🥈 | **Punjab Kings (PBKS)** | 73 | 39 | 34 | **53.4%** |
| 🥉 | **Rajasthan Royals (RR)** | 81 | 42 | 39 | **51.9%** |
| 4 | **Mumbai Indians (MI)** | 81 | 41 | 40 | **50.6%** |
| 5 | **Chennai Super Kings (CSK)** | 75 | 36 | 39 | **48.0%** |
| 6 | **Kolkata Knight Riders (KKR)** | 65 | 31 | 34 | **47.7%** |
| 7 | **Delhi Capitals (DC)** | 72 | 34 | 38 | **47.2%** |
| 8 | **Sunrisers Hyderabad (SRH)** | 78 | 36 | 42 | **46.2%** |

---

### Toss Impact & Hypothesis Testing

- **Toss Decision Breakdown**:
  - **Field First (Chasing)**: Won **56.6%** of matches when choosing to bowl first.
  - **Bat First (Defending)**: Won **46.3%** of matches when choosing to bat first.
- **Statistical Significance (Chi-Square Test of Independence)**:
  $$\chi^2 = 2.35, \quad p\text{-value} = 0.1250 \quad (\alpha = 0.05)$$
  - **Conclusion**: With $p = 0.1250 > 0.05$, we fail to reject the null hypothesis. **Winning the toss does not provide a statistically significant advantage** towards winning the match.

---

### Venue Scoring Profiles (Average 1st Innings Scores)

| Venue | City | Avg 1st Inn Score |
|:---|:---|:---:|
| **Sawai Mansingh Stadium** | Jaipur | **172.0** |
| **Wankhede Stadium** | Mumbai | **168.0** |
| **Arun Jaitley Stadium** | Delhi | **166.8** |
| **M. A. Chidambaram Stadium** | Chennai | **164.9** |
| **Eden Gardens** | Kolkata | **164.3** |
| **M. Chinnaswamy Stadium** | Bengaluru | **163.7** |
| **Rajiv Gandhi International Stadium** | Hyderabad | **162.3** |
| **Narendra Modi Stadium** | Ahmedabad | **161.2** |

---

### Top Individual Performers

- **Leading Run Scorer**: `Mumbai_Player2` — **2,166 runs** (Strike Rate: 138.9, 165 fours, 111 sixes).
- **Leading Wicket Taker**: `Mumbai_Player5` — **52 wickets** (Economy: 8.50).
- **Most Player of the Match Awards**: `Mumbai_Player8` & `Punjab_Player4` (**8 awards each**).
- **Tournament Boundaries**: **13,925 fours** and **8,560 sixes** hit across 300 matches.
- **Average Victory Margins**: Run margin: **18.3 runs**; wicket margin: **4.6 wickets**.

---

## 🎮 Interactive Dashboard Features

The dashboard ([`index.html`](index.html)) provides a value-changeable interface across 4 navigation views:

1. **⚡ Interactive Studio**:
   - Multi-toggle seasons (2020 to 2024).
   - Team franchise filters (toggle any of the 8 teams).
   - Toss decision dropdown and player minimum innings slider.
   - Quick preset buttons (*All Seasons*, *Recent*, *Field First*, *RCB Focus*, *MI Focus*).
   - Dynamic Chart.js visualizations, sortable leaderboards, and animated counters.
2. **🤖 Machine Learning Studio**:
   - **Interactive Match Winner Predictor Calculator**: Select two franchises, stadium, and toss outcome to compute real-time win probability and estimated 1st innings total.
   - Full ML evaluation benchmark tables comparing 4 classification and 3 regression algorithms.
   - Embeds ROC curve, confusion matrix, regression fit, and feature importance charts.
3. **📊 Deep-Dive Charts**:
   - 9 high-resolution Matplotlib figures documenting franchise consistency, win margins, and toss impact.
4. **📋 Data Explorer**:
   - Paginated browser with client-side search across all 300 matches and 6,600 player records.

---

## 📁 Project Structure

```text
IPL-Cricket-Data-Analysis/
├── data/                            # Raw datasets (300 matches & 6,600 player records)
│   ├── ipl_matches.csv              # Match metadata (2020-2024)
│   └── ipl_player_stats.csv         # Player innings statistics
│
├── images/                          # Publication-quality charts & ML evaluation figures
│   ├── chart_1_team_win_pct.png     # [Bar Chart] Franchise win percentages
│   ├── chart_2_season_wins_trend.png# [Line Chart] Consistency trends of top teams
│   ├── chart_3_top_run_scorers.png  # [Horizontal Bar Chart] Top 10 run scorers
│   ├── chart_4_top_wicket_takers.png# [Horizontal Bar Chart] Top 10 wicket takers
│   ├── chart_5_toss_decision_winrate.png # [Bar Chart] Bat vs Field win rate analysis
│   ├── chart_6_win_margin_runs.png  # [Histogram] Victory margin histogram
│   ├── chart_7_venue_scores.png     # [Horizontal Bar Chart] Stadium 1st innings averages
│   ├── chart_8_potm.png             # [Horizontal Bar Chart] Player of the Match awards
│   ├── chart_9_season_boundaries.png# [Grouped Bar Chart] Boundary trends (Fours vs Sixes)
│   ├── ml_models_comparison.png     # [Grouped Bar Chart] ML Comparison (Accuracy, F1, ROC-AUC)
│   ├── ml_confusion_matrix.png      # [Heatmap] Confusion Matrix (Random Forest)
│   ├── ml_roc_curve.png             # [ROC Curves] ROC Curves for all classifiers
│   ├── ml_feature_importance.png    # [Horizontal Bar Chart] Top 10 feature importances
│   └── ml_regression_actual_vs_pred.png # [Scatter Plot] Actual vs Predicted scores
│
├── IPL_Cricket_Data_Analysis.ipynb  # Primary Jupyter Notebook for submission & analysis
├── train_models.py                  # Supervised ML training pipeline (Classification & Regression)
├── index.html                       # Interactive web dashboard (self-contained, zero-CORS)
├── README.md                        # Project documentation, ML benchmarks & summary
└── ml_metrics_summary.json          # Serialized ML metrics (CV scores, Test metrics, Feature importances)
```

---

## 🚀 How to Run the Project

### 1. Open the Interactive Dashboard
Double-click `index.html` or open directly in your browser:
```powershell
Start-Process "index.html"
# Or run via local server:
python -m http.server 8080
```

### 2. Run Machine Learning Pipeline
```powershell
python train_models.py
```
*Trains all classification and regression models with 5-fold cross-validation, saves metrics to `ml_metrics_summary.json`, and exports evaluation plots to `images/`.*

### 3. Open the Jupyter Notebook
```powershell
jupyter notebook IPL_Cricket_Data_Analysis.ipynb
```

---

## 🛠️ Technologies Used

- **Machine Learning**: `scikit-learn` (Pipelines, ColumnTransformer, Logistic Regression, Decision Trees, Random Forests, Gradient Boosting, Ridge, Metrics)
- **Data Wrangling**: `pandas`, `numpy`, `scipy` (Chi-Square contingency tests)
- **Static Visualizations**: `matplotlib`
- **Interactive Front-end**: Vanilla HTML5, CSS3 (Glassmorphism, Dark UI, Responsive Layout), Vanilla JavaScript (ES6+)
- **Client-Side Libraries**: `Chart.js 4.4`, `PapaParse 5.4`
