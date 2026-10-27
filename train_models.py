import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, KFold
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    confusion_matrix, ConfusionMatrixDisplay, roc_curve,
    mean_absolute_error, mean_squared_error, r2_score
)
import sys
sys.stdout.reconfigure(encoding='utf-8')
import json
import os
os.makedirs('images', exist_ok=True)

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

print("=" * 60)
print("[+] IPL MACHINE LEARNING PIPELINE: CLASSIFICATION & REGRESSION")
print("=" * 60)

matches_path = 'data/ipl_matches.csv' if os.path.exists('data/ipl_matches.csv') else 'ipl_matches.csv'
matches = pd.read_csv(matches_path)
print(f"Loaded {len(matches)} matches across seasons: {sorted(matches['season'].unique())}")

matches['team1_won'] = (matches['winner'] == matches['team1']).astype(int)
matches['toss_winner_is_team1'] = (matches['toss_winner'] == matches['team1']).astype(int)

all_teams_played = pd.concat([matches['team1'], matches['team2']]).value_counts()
all_teams_won = matches['winner'].value_counts()
team_win_pct = (all_teams_won / all_teams_played).to_dict()

matches['team1_win_pct'] = matches['team1'].map(team_win_pct)
matches['team2_win_pct'] = matches['team2'].map(team_win_pct)
matches['win_pct_diff'] = matches['team1_win_pct'] - matches['team2_win_pct']

cat_features = ['team1', 'team2', 'venue', 'toss_decision']
num_features = ['toss_winner_is_team1', 'win_pct_diff']
X_cols = cat_features + num_features
X = matches[X_cols]
y_class = matches['team1_won']

y_reg = matches['team1_score']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), cat_features),
        ('num', StandardScaler(), num_features)
    ]
)

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X, y_class, test_size=0.20, random_state=RANDOM_STATE, stratify=y_class
)
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X, y_reg, test_size=0.20, random_state=RANDOM_STATE
)

train_mask = matches['season'] < 2024
test_mask = matches['season'] == 2024
X_temp_train, X_temp_test = X[train_mask], X[test_mask]
y_temp_train, y_temp_test = y_class[train_mask], y_class[test_mask]

print(f"\n--- DATA SPLITS ---")
print(f"Random Train Set: {len(X_train_c)} matches | Test Set: {len(X_test_c)} matches (80/20)")
print(f"Temporal Train (2020-2023): {len(X_temp_train)} matches | Test (2024): {len(X_temp_test)} matches")

print("\n" + "=" * 60)
print("[+] SUPERVISED CLASSIFICATION: MATCH WINNER PREDICTION")
print("=" * 60)

classifiers = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    "Decision Tree": DecisionTreeClassifier(max_depth=5, min_samples_split=10, random_state=RANDOM_STATE),
    "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=6, random_state=RANDOM_STATE),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.08, max_depth=3, random_state=RANDOM_STATE)
}

cv_strat = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
clf_results = {}
fitted_pipelines = {}

for name, clf in classifiers.items():
    pipe = Pipeline([('prep', preprocessor), ('model', clf)])

    cv_scores = cross_val_score(pipe, X_train_c, y_train_c, cv=cv_strat, scoring='accuracy')

    pipe.fit(X_train_c, y_train_c)
    fitted_pipelines[name] = pipe

    y_pred = pipe.predict(X_test_c)
    y_prob = pipe.predict_proba(X_test_c)[:, 1] if hasattr(clf, 'predict_proba') else y_pred

    acc = accuracy_score(y_test_c, y_pred)
    prec = precision_score(y_test_c, y_pred, zero_division=0)
    rec = recall_score(y_test_c, y_pred, zero_division=0)
    f1 = f1_score(y_test_c, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test_c, y_prob)

    clf_results[name] = {
        'cv_mean': float(cv_scores.mean()),
        'cv_std': float(cv_scores.std()),
        'test_accuracy': float(acc),
        'precision': float(prec),
        'recall': float(rec),
        'f1_score': float(f1),
        'roc_auc': float(roc_auc),
        'y_pred': y_pred,
        'y_prob': y_prob
    }

    print(f"\n[{name}]")
    print(f"  5-Fold CV Accuracy: {cv_scores.mean():.3f} (±{cv_scores.std():.3f})")
    print(f"  Test Accuracy:      {acc:.3f}")
    print(f"  Precision:          {prec:.3f}")
    print(f"  Recall:             {rec:.3f}")
    print(f"  F1-Score:           {f1:.3f}")
    print(f"  ROC-AUC:            {roc_auc:.3f}")

print("\n" + "=" * 60)
print("[+] SUPERVISED REGRESSION: 1ST INNINGS SCORE PREDICTION")
print("=" * 60)

regressors = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0, random_state=RANDOM_STATE),
    "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=6, random_state=RANDOM_STATE)
}

cv_reg = KFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
reg_results = {}

for name, reg in regressors.items():
    pipe = Pipeline([('prep', preprocessor), ('model', reg)])

    cv_scores = -cross_val_score(pipe, X_train_r, y_train_r, cv=cv_reg, scoring='neg_root_mean_squared_error')

    pipe.fit(X_train_r, y_train_r)
    y_pred_r = pipe.predict(X_test_r)

    mae = mean_absolute_error(y_test_r, y_pred_r)
    mse = mean_squared_error(y_test_r, y_pred_r)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test_r, y_pred_r)

    reg_results[name] = {
        'cv_rmse': float(cv_scores.mean()),
        'mae': float(mae),
        'rmse': float(rmse),
        'r2': float(r2),
        'y_pred': y_pred_r
    }

    print(f"\n[{name}]")
    print(f"  5-Fold CV RMSE: {cv_scores.mean():.2f}")
    print(f"  Test MAE:       {mae:.2f} runs")
    print(f"  Test RMSE:      {rmse:.2f} runs")
    print(f"  Test R²:        {r2:.3f}")

best_rf = fitted_pipelines['Random Forest'].named_steps['model']
prep = fitted_pipelines['Random Forest'].named_steps['prep']

cat_cols = prep.named_transformers_['cat'].get_feature_names_out(cat_features).tolist()
all_features = cat_cols + num_features
importances = best_rf.feature_importances_

feat_imp_df = pd.DataFrame({'feature': all_features, 'importance': importances})
feat_imp_df = feat_imp_df.sort_values('importance', ascending=False).head(10)

print("\n" + "=" * 60)
print("[+] TOP 10 FEATURE IMPORTANCE (RANDOM FOREST)")
print("=" * 60)
for idx, row in feat_imp_df.iterrows():
    print(f"  {row['feature']:<35} : {row['importance']:.4f}")

fig, ax = plt.subplots(figsize=(6, 5))
cm = confusion_matrix(y_test_c, clf_results['Random Forest']['y_pred'])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Loss', 'Win'])
disp.plot(cmap='Blues', ax=ax, values_format='d')
ax.set_title('[Heatmap / Confusion Matrix] Random Forest (Test Set)', fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig('images/ml_confusion_matrix.png', dpi=150)
plt.close()
print("\nSaved ml_confusion_matrix.png")

fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#3b82f6', '#f5a623', '#22c55e', '#a855f7']
for (name, res), color in zip(clf_results.items(), colors):
    fpr, tpr, _ = roc_curve(y_test_c, res['y_prob'])
    ax.plot(fpr, tpr, color=color, lw=2.2, label=f"{name} (AUC = {res['roc_auc']:.2f})")
ax.plot([0, 1], [0, 1], color='gray', lw=1.5, linestyle='--', label='Random Guess (AUC = 0.50)')
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])
ax.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=12)
ax.set_ylabel('True Positive Rate (Sensitivity)', fontsize=12)
ax.set_title('[ROC Curves] Match Winner Classification (AUC Evaluation)', fontsize=14, fontweight='bold')
ax.legend(loc="lower right", fontsize=10)
plt.tight_layout()
plt.savefig('images/ml_roc_curve.png', dpi=150)
plt.close()
print("Saved ml_roc_curve.png")

fig, ax = plt.subplots(figsize=(10, 6))
clean_names = [f.replace('team1_', 'T1: ').replace('team2_', 'T2: ').replace('venue_', 'Venue: ').replace('toss_decision_', 'Toss: ') for f in feat_imp_df['feature']]
bars = ax.barh(clean_names[::-1], feat_imp_df['importance'][::-1], color='#3b82f6')
ax.set_xlabel('Feature Importance Gini Index', fontsize=12)
ax.set_title('[Horizontal Bar Chart] Top 10 Feature Importances (Random Forest)', fontsize=14, fontweight='bold')
for bar, val in zip(bars, feat_imp_df['importance'][::-1]):
    ax.text(bar.get_width() + 0.003, bar.get_y() + bar.get_height()/2, f'{val:.3f}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('images/ml_feature_importance.png', dpi=150)
plt.close()
print("Saved ml_feature_importance.png")

fig, ax = plt.subplots(figsize=(9, 5))
names = list(clf_results.keys())
accs = [clf_results[n]['test_accuracy'] * 100 for n in names]
f1s = [clf_results[n]['f1_score'] * 100 for n in names]
aucs = [clf_results[n]['roc_auc'] * 100 for n in names]

x = np.arange(len(names))
width = 0.25
ax.bar(x - width, accs, width=width, label='Accuracy %', color='#3b82f6')
ax.bar(x, f1s, width=width, label='F1-Score %', color='#22c55e')
ax.bar(x + width, aucs, width=width, label='ROC-AUC %', color='#f5a623')
ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=11)
ax.set_ylabel('Score (%)', fontsize=12)
ax.set_ylim(0, 100)
ax.set_title('[Grouped Bar Chart] Classification Models Comparison (Test Set)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
for i in range(len(names)):
    ax.text(i - width, accs[i] + 1.5, f"{accs[i]:.1f}%", ha='center', fontsize=8)
    ax.text(i, f1s[i] + 1.5, f"{f1s[i]:.1f}%", ha='center', fontsize=8)
    ax.text(i + width, aucs[i] + 1.5, f"{aucs[i]:.1f}%", ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('images/ml_models_comparison.png', dpi=150)
plt.close()
print("Saved ml_models_comparison.png")

fig, ax = plt.subplots(figsize=(8, 6))
best_reg_name = "Ridge Regression"
y_pred_reg = reg_results[best_reg_name]['y_pred']
ax.scatter(y_test_r, y_pred_reg, color='#a855f7', alpha=0.75, edgecolors='k', s=60, label='Predicted Matches')
min_val = min(y_test_r.min(), y_pred_reg.min()) - 5
max_val = max(y_test_r.max(), y_pred_reg.max()) + 5
ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction (y=x)')
ax.set_xlabel('Actual 1st Innings Score', fontsize=12)
ax.set_ylabel('Predicted Score (Ridge)', fontsize=12)
ax.set_title(f'[Scatter Plot] Actual vs Predicted 1st Innings Score (MAE={reg_results[best_reg_name]["mae"]:.1f} runs)', fontsize=13, fontweight='bold')
ax.legend(fontsize=11)
plt.tight_layout()
plt.savefig('images/ml_regression_actual_vs_pred.png', dpi=150)
plt.close()
print("Saved ml_regression_actual_vs_pred.png")

metrics_summary = {
    "classification": {
        name: {
            "cv_mean": res["cv_mean"],
            "cv_std": res["cv_std"],
            "test_accuracy": res["test_accuracy"],
            "precision": res["precision"],
            "recall": res["recall"],
            "f1_score": res["f1_score"],
            "roc_auc": res["roc_auc"]
        } for name, res in clf_results.items()
    },
    "regression": {
        name: {
            "cv_rmse": res["cv_rmse"],
            "mae": res["mae"],
            "rmse": res["rmse"],
            "r2": res["r2"]
        } for name, res in reg_results.items()
    },
    "top_features": feat_imp_df.to_dict(orient='records')
}

with open("ml_metrics_summary.json", "w", encoding="utf-8") as f:
    json.dump(metrics_summary, f, indent=2)
print("Saved ml_metrics_summary.json")

print("\n" + "=" * 60)
print("[+] ALL MACHINE LEARNING PIPELINES COMPLETED SUCCESSFULLY!")
print("=" * 60)
