from flask import Flask, request, render_template, send_file
import pickle
import io
from fpdf import FPDF

app = Flask(__name__)
scaler = pickle.load(open('scaler.pkl', 'rb'))
model = pickle.load(open('best_model.pkl', 'rb'))

def risk_level(prob):
    if prob > 0.85:
        return "very high risk"
    elif prob > 0.65:
        return "high risk"
    elif prob > 0.5:
        return "borderline"
    else:
        return "low risk"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        prediction = None
        prob = None
        risk = None
        error = None
        show_result = False
        values = {}
        try:
            name = request.form.get('name')
            gender = request.form.get('gender')
            age = request.form.get('age')
            gluc = request.form.get('gluc')
            bp = request.form.get('bp')
            skin = request.form.get('skin')
            insulin = request.form.get('insulin')
            bmi = request.form.get('bmi')
            func = request.form.get('func')
            pregs = request.form.get('pregs')
            values = {'name': name, 'gender': gender, 'age': age, 'pregs': pregs, 'gluc': gluc, 'bp': bp, 'skin': skin, 'insulin': insulin, 'bmi': bmi, 'func': func}

            if not all([name, gender, age, gluc, bp, skin, insulin, bmi, func]):
                error = "Please fill in all required fields"
                return render_template('index.html', prediction=prediction, prob=prob, risk=risk, error=error, show_result=show_result, values=values)

            age = float(age)
            gluc = float(gluc)
            bp = float(bp)
            skin = float(skin)
            insulin = float(insulin)
            bmi = float(bmi)
            func = float(func)
            pregs = float(pregs) if (gender == 'female' and age > 25 and pregs) else 0
            high_bmi = int(bmi > 30)
            high_glucose = int(gluc > 125)
            is_older = int(age > 50)
            features = [pregs, gluc, bp, skin, insulin, bmi, func, age, high_bmi, high_glucose, is_older]
            scaled = scaler.transform([features])
            prediction = int(model.predict(scaled)[0])
            prob = float(model.predict_proba(scaled)[0][1])
            risk = risk_level(prob)
            show_result = True
        except Exception as e:
            error = f"Invalid input: {e}"
        return render_template('index.html', prediction=prediction, prob=prob, risk=risk, error=error, show_result=show_result, values=values)
    else:
        # GET request: always render a truly blank form, no download/result ever
        return render_template('index.html', prediction=None, prob=None, risk=None, error=None, show_result=False, values={})

@app.route('/download-pdf', methods=['POST'])
def download_pdf():
    name = request.form.get('name')
    gender = request.form.get('gender')
    age = request.form.get('age')
    pregs = request.form.get('pregs')
    gluc = request.form.get('gluc')
    bp = request.form.get('bp')
    skin = request.form.get('skin')
    insulin = request.form.get('insulin')
    bmi = request.form.get('bmi')
    func = request.form.get('func')
    prediction = request.form.get('prediction')
    risk = request.form.get('risk')
    prob = request.form.get('prob')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "Diabetes Prediction Report", ln=1, align='C')
    pdf.ln(6)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Name: {name}", ln=1)
    pdf.cell(0, 10, f"Gender: {gender}", ln=1)
    pdf.cell(0, 10, f"Age: {age}", ln=1)
    if gender == "female" and age and float(age) > 25:
        pdf.cell(0, 10, f"Pregnancies: {pregs}", ln=1)
    pdf.cell(0, 10, f"Glucose: {gluc}", ln=1)
    pdf.cell(0, 10, f"Blood Pressure: {bp}", ln=1)
    pdf.cell(0, 10, f"Skin Thickness: {skin}", ln=1)
    pdf.cell(0, 10, f"Insulin: {insulin}", ln=1)
    pdf.cell(0, 10, f"BMI: {bmi}", ln=1)
    pdf.cell(0, 10, f"Pedigree: {func}", ln=1)
    pdf.ln(8)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(34,139,34) if prediction == '0' else pdf.set_text_color(178,34,34)
    pdf.cell(0, 12, f"Prediction: {'Not Diabetic' if prediction == '0' else 'Diabetic'}", ln=1)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Risk level: {risk} (Probability: {float(prob)*100:.2f}%)", ln=1)
    pdf.ln(8)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, "Disclaimer: This prediction is based on statistical analysis and should not be considered medical advice. Please consult a healthcare professional for a final diagnosis.", align='L')

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf', download_name='diabetes_report.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
