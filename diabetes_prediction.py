import warnings
warnings.filterwarnings('ignore')
import os
os.environ['XGBOOST_ENABLE_DEPRECATED_WARNING'] = '0'

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
import pickle

df = pd.read_csv('diabetes.csv')
for col in ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']:
    df[col] = df[col].replace(0, df[col].mean())
df = df.drop_duplicates()
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

clf1 = LogisticRegression(max_iter=200, random_state=42)
clf2 = RandomForestClassifier(n_estimators=200, random_state=42)
clf3 = SVC(probability=True, random_state=42)
clf4 = XGBClassifier(eval_metric='logloss', random_state=42)

models = {
    "Logistic Regression": clf1,
    "Random Forest": clf2,
    "SVM": clf3,
    "XGBoost": clf4
}

for name, clf in models.items():
    clf.fit(X_train_scaled, y_train)
    y_pred = clf.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    print(f"{name} Accuracy: {acc * 100:.2f}%")

ensemble = VotingClassifier(
    estimators=[
        ('lr', clf1),
        ('rf', clf2),
        ('svm', clf3),
        ('xgb', clf4)
    ],
    voting='soft'
)

ensemble.fit(X_train_scaled, y_train)
y_pred = ensemble.predict(X_test_scaled)
acc = accuracy_score(y_test, y_pred)
print(f"Finalised Accuracy Rate (Ensemble): {acc * 100:.2f}%")
pickle.dump(scaler, open('scaler.pkl', 'wb'))
pickle.dump(ensemble, open('best_model.pkl', 'wb'))
