import streamlit as st
from prediction_helper import predict

st.set_page_config(page_title="Health Insurance Premium Predictor", page_icon="💰", layout="centered")

# Title and styling
st.markdown("""
    <div style="background-color:#e6f2ff; padding: 15px; border-radius: 12px;">
        <h1 style="
            color: #003366;
            text-align: center;
            margin: 0;
            font-size: 28px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        ">
            💼 Health Insurance Premium Predictor
        </h1>
    </div>
""", unsafe_allow_html=True)


st.markdown("## 🔎 Enter the details below:")

# Category choices
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer', ''],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Diabetes & High blood pressure',
        'Thyroid', 'Heart disease', 'High blood pressure & Heart disease', 'Diabetes & Thyroid',
        'Diabetes & Heart disease'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# Layout
row1 = st.columns(3)
row2 = st.columns(3)
row3 = st.columns(3)
row4 = st.columns(3)

with row1[0]:
    age = st.number_input("🎂 Age", min_value=18, step=1, max_value=100)
with row1[1]:
    number_of_dependants = st.number_input("👨‍👩‍👧 Dependants", min_value=0, step=1, max_value=20)
with row1[2]:
    income_lakhs = st.number_input("💸 Yearly Income (Lakhs)", step=1, min_value=0, max_value=200)

with row2[0]:
    genetical_risk = st.number_input("🧬 Genetical Risk", step=1, min_value=0, max_value=5)
with row2[1]:
    insurance_plan = st.selectbox("📦 Insurance Plan", categorical_options['Insurance Plan'])
with row2[2]:
    employment_status = st.selectbox("💼 Employment Status", categorical_options['Employment Status'])

with row3[0]:
    gender = st.selectbox("⚧ Gender", categorical_options['Gender'])
with row3[1]:
    marital_status = st.selectbox("💍 Marital Status", categorical_options['Marital Status'])
with row3[2]:
    bmi_category = st.selectbox("⚖ BMI Category", categorical_options['BMI Category'])

with row4[0]:
    smoking_status = st.selectbox("🚬 Smoking Status", categorical_options['Smoking Status'])
with row4[1]:
    region = st.selectbox("🌍 Region", categorical_options['Region'])
with row4[2]:
    medical_history = st.selectbox("🩺 Medical History", categorical_options['Medical History'])

# Input dictionary
input_dict = {
    'Age': age,
    'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan,
    'Employment Status': employment_status,
    'Gender': gender,
    'Marital Status': marital_status,
    'BMI Category': bmi_category,
    'Smoking Status': smoking_status,
    'Region': region,
    'Medical History': medical_history
}

# Prediction
st.markdown("---")
if st.button("🧮 Predict Insurance Premium"):
    prediction = predict(input_dict)
    st.success(f"🏥 Estimated Health Insurance Premium: ₹ {prediction}")

