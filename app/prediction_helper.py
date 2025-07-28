
import os
import pandas as pd
import joblib

# Define base directory for loading artifacts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load pre-trained models and scalers
model_young = joblib.load(os.path.join(BASE_DIR, "artifacts", "model_young.joblib"))
model_rest = joblib.load(os.path.join(BASE_DIR, "artifacts", "model_rest.joblib"))
scaler_young = joblib.load(os.path.join(BASE_DIR, "artifacts", "scaler_young.joblib"))
scaler_rest = joblib.load(os.path.join(BASE_DIR, "artifacts", "scaler_rest.joblib"))

def calculate_normalized_risk(medical_history):
    """
    Assigns a risk score based on user's medical history and normalizes it.
    """
    risk_scores = {
        "diabetes": 6,
        "heart disease": 8,
        "high blood pressure": 6,
        "thyroid": 5,
        "no disease": 0,
        "none": 0
    }
    diseases = medical_history.lower().split(" & ")
    total_risk_score = sum(risk_scores.get(disease, 0) for disease in diseases)
    normalized_risk_score = total_risk_score / 14  # Max possible score is 14
    return normalized_risk_score

def preprocess_input(input_dict):
    """
    Converts user input into a model-friendly format with appropriate encoding and scaling.
    """
    expected_columns = [
        'age', 'number_of_dependants', 'income_lakhs', 'insurance_plan', 'genetical_risk', 'normalized_risk_score',
        'gender_Male', 'region_Northwest', 'region_Southeast', 'region_Southwest', 'marital_status_Unmarried',
        'bmi_category_Obesity', 'bmi_category_Overweight', 'bmi_category_Underweight', 'smoking_status_Occasional',
        'smoking_status_Regular', 'employment_status_Salaried', 'employment_status_Self-Employed'
    ]

    insurance_plan_encoding = {'Bronze': 1, 'Silver': 2, 'Gold': 3}
    df = pd.DataFrame(0, columns=expected_columns, index=[0])

    # Populate dataframe based on input values
    if input_dict.get('Gender') == 'Male':
        df['gender_Male'] = 1
    region = input_dict.get('Region')
    if region in ['Northwest', 'Southeast', 'Southwest']:
        df[f'region_{region}'] = 1
    if input_dict.get('Marital Status') == 'Unmarried':
        df['marital_status_Unmarried'] = 1

    bmi = input_dict.get('BMI Category')
    if bmi in ['Obesity', 'Overweight', 'Underweight']:
        df[f'bmi_category_{bmi}'] = 1

    smoking = input_dict.get('Smoking Status')
    if smoking in ['Occasional', 'Regular']:
        df[f'smoking_status_{smoking}'] = 1

    employment = input_dict.get('Employment Status')
    if employment in ['Salaried', 'Self-Employed']:
        df[f'employment_status_{employment}'] = 1

    df['insurance_plan'] = insurance_plan_encoding.get(input_dict.get('Insurance Plan'), 1)
    df['age'] = input_dict.get('Age', 0)
    df['number_of_dependants'] = input_dict.get('Number of Dependants', 0)
    df['income_lakhs'] = input_dict.get('Income in Lakhs', 0)
    df['genetical_risk'] = input_dict.get('Genetical Risk', 0)

    df['normalized_risk_score'] = calculate_normalized_risk(input_dict.get('Medical History', 'none'))
    return handle_scaling(df['age'][0], df)

def handle_scaling(age, df):
    """
    Applies appropriate scaler based on user's age.
    """
    scaler_object = scaler_young if age <= 25 else scaler_rest
    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']

    df['income_level'] = None  # Dummy column for compatibility
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df.drop('income_level', axis=1, inplace=True)

    return df

def predict(input_dict):
    """
    Runs prediction based on preprocessed user input.
    """
    input_df = preprocess_input(input_dict)
    model = model_young if input_dict['Age'] <= 25 else model_rest
    return int(model.predict(input_df)[0])

