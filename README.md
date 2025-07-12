# 💙 Healthify — Diabetes Prediction App

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python&style=flat-square" />
  <img src="https://img.shields.io/badge/Flask-%23d3eafc?logo=flask&logoColor=black&style=flat-square" />
  <img src="https://img.shields.io/badge/Scikit--Learn-yellow?logo=scikit-learn&logoColor=black&style=flat-square" />
  <img src="https://img.shields.io/badge/Accuracy-84%25-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/Project-Healthify-6d28d9?style=flat-square" />
  <img src="https://img.shields.io/github/license/psyphon1/healthify?color=brightgreen&style=flat-square" />
</p>

---

> **Instant, accurate diabetes prediction. Dynamic UX, instant PDF medical report, risk levels & real ML.  
> Made with ❤️ by [Chinmay Duse (psyphon1)](https://github.com/psyphon1) 🚀**

---

## ✨ Features

- **AI-Powered Diabetes Prediction**
  - Multiple models (Random Forest, SVM, XGBoost, Logistic Regression)
  - Ensemble and best-model selection built-in

- **Basic UX**
  - Adapts questions based on user (e.g. pregnancies only for women age >25)
  - Super clear error handling, never leaves the user confused

- **Output**
  - Real model probability + risk level (low/high/very high/borderline)
  - Download a medical-style PDF report in one click

- **Safe, Private, Deployable**
  - No data saved on the server
  - Ready to deploy on Render, Railway, Heroku, PythonAnywhere, etc.

---

## 📊 Model Accuracies

| Model                 | Accuracy |
|-----------------------|:--------:|
| Logistic Regression   | 75.50%   |
| Random Forest         | 84.00%   |
| SVM                   | 81.00%   |
| XGBoost               | 80.50%   |
| **Ensemble Avg**      | 83.50%   |

**Best Model:** Random Forest

_See the output for the full classification report._

---

## 🚦 How to Use

1. **Clone the repo:**
    ```bash
    git clone https://github.com/psyphon1/healthify.git
    cd healthify
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Train & generate models and scaler:**
    ```bash
    python diabetes_prediction.py
    ```

4. **Start the app:**
    ```bash
    python app.py
    ```

5. **Open your browser:**  
    Visit [http://localhost:5000](http://localhost:5000)

---

## 📄 PDF Medical Report

- After each prediction, download a full, professional report
- Includes all inputs, probability, risk level, and outcome

---

## 🤝 Contributing

**Healthify** is open for contributions!  
Wanna make it better? Found a bug? Got a killer feature idea? PRs are welcome.

1. Fork the repo and make your changes in a new branch.
2. Open a Pull Request with a clear description of your edits.
3. Star the project to show some love!  
4. All contributors will get credit in the README and the project’s About section.

> Want to discuss big features or have questions?  
> [Open an issue](https://github.com/psyphon1/healthify/issues) or DM [@psyphon1](https://github.com/psyphon1) on GitHub!

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).  
Free for personal, academic, and commercial use with attribution.

---

## 👨‍💻 Author

**Chinmay Duse**  
Github: [psyphon1](https://github.com/psyphon1)  
LinkedIn: [Chinmay Duse](linkedin.com/in/chinmayduse/)

---

## 💎 Project Qualities

- Minimal, modern UI (no cringe hospital forms)
- Bug-free, always up-to-date, and fully validated
- ML accuracy >80%, ensemble-backed, and explainable
- Built for humans, not just engineers

---

## 🛡 Disclaimer

> **This tool is for informational/educational use only.  
> Not a substitute for real medical advice or diagnosis.  
> Always consult your doctor for actual health care.**

---

<p align="center">
  <b>Made with ❤️ by Chinmay Duse (psyphon1) — Healthify</b>
</p>
