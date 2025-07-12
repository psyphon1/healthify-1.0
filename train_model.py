# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
import pickle

df = pd.read_csv('diabetes.csv')
for col in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
    df[col] = df[col].replace(0, df[col].mean())
df = df.drop_duplicates()

# Feature engineering (expand as needed)
df['High_BMI'] = (df['BMI'] > 30).astype(int)
df['High_Glucose'] = (df['Glucose'] > 125).astype(int)
df['Is_Older'] = (df['Age'] > 50).astype(int)

X = df.drop('Outcome', axis=1)
y = df['Outcome']

sm = SMOTE(random_state=42)
X_bal, y_bal = sm.fit_resample(X, y)
X_train, X_test, y_train, y_test = train_test_split(X_bal, y_bal, test_size=0.2, random_state=42, stratify=y_bal)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

models = {
    "Logistic Regression": LogisticRegression(max_iter=200, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "SVM": SVC(random_state=42, probability=True),
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
}

best_acc = 0
best_model = None
best_name = ""

print("\n===== Model Accuracies =====")
for name, clf in models.items():
    clf.fit(X_train_scaled, y_train)
    y_pred = clf.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"{name}: {acc * 100:.2f}%")
    if acc > best_acc:
        best_acc = acc
        best_model = clf
        best_name = name

print(f"\nBest Model: {best_name} ({best_acc * 100:.2f}%)")
print("Classification Report:\n", classification_report(y_test, best_model.predict(X_test_scaled)))

# Save best model + scaler
pickle.dump(scaler, open('scaler.pkl', 'wb'))
pickle.dump(best_model, open('best_model.pkl', 'wb'))
