
# Modules

from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import shap
import matplotlib.pyplot as plt
import dice_ml
from catboost import CatBoostClassifier
from dice_ml import Dice

# page configuration

st.set_page_config(
    page_title="Explainable Diabetes Risk",
    page_icon="🩺",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "model_.pkl"
TRAIN_PATH = BASE_DIR / "train_data.csv"

RISK_LABELS = {
    0: "Low Risk",
    1: "Moderate Risk",
    2: "High Risk"
}

FEATURE_LABELS = {
    "Age": "Age",
    "Height_cm": "Height",
    "Weight_kg": "Weight",
    "BMI": "BMI",
    "Waist_Circumference_cm": "Waist circumference",
    "Blood_Glucose": "Blood glucose",
    "HbA1c": "HbA1c",
    "Fasting_Blood_Sugar": "Fasting blood sugar",
    "Insulin_Level": "Insulin level",
    "Blood_Pressure_Systolic": "Systolic blood pressure",
    "Blood_Pressure_Diastolic": "Diastolic blood pressure",
    "Total_Cholesterol": "Total cholesterol",
    "HDL": "HDL",
    "LDL": "LDL",
    "Triglycerides": "Triglycerides",
    "Heart_Rate": "Heart rate",
    "Physical_Activity_Level": "Physical activity level",
    "Exercise_Hours_Per_Week": "Exercise hours per week",
    "Daily_Walking_Minutes": "Daily walking minutes",
    "Diet_Quality": "Diet quality",
    "Sugar_Intake_Level": "Sugar intake level",
    "Sleep_Hours": "Sleep hours",
    "Stress_Level": "Stress level",
    "Alcohol_Consumption": "Alcohol consumption",
    "Family_History_Diabetes": "Family history of diabetes",
    "Hypertension": "Hypertension",
    "Heart_Disease": "Heart disease",
    "Fatty_Liver": "Fatty liver",
    "PCOS": "PCOS",
    "Daily_Water_Intake_L": "Daily water intake",
    "Doctor_Consultation_Needed": "Doctor consultation needed",
    "Gender_Male": "Gender: Male",
    "Gender_Other": "Gender: Other",
    "Smoking_Status_Former": "Smoking: Former",
    "Smoking_Status_Never": "Smoking: Never",
    "Medication_Adherence_Good": "Medication adherence: Good",
    "Medication_Adherence_Poor": "Medication adherence: Poor",
    "Work_Type_Government": "Work: Government",
    "Work_Type_Private": "Work: Private",
    "Work_Type_Retired": "Work: Retired",
    "Work_Type_Student": "Work: Student",
    "Residence_Type_Urban": "Residence: Urban",
}

COUNTRIES = [
    "Australia", "Bangladesh", "Brazil", "Canada", "China", "Egypt",
    "France", "Germany", "India", "Indonesia", "Italy", "Japan",
    "Malaysia", "Mexico", "Nigeria", "Pakistan", "Russia",
    "Saudi Arabia", "South Africa", "South Korea", "Spain",
    "Turkey", "United Kingdom", "United States"
]

COUNTRY_COLUMNS = {
    "Australia": "Country_Australia",
    "Bangladesh": "Country_Bangladesh",
    "Brazil": "Country_Brazil",
    "Canada": "Country_Canada",
    "China": "Country_China",
    "Egypt": "Country_Egypt",
    "France": "Country_France",
    "Germany": "Country_Germany",
    "India": "Country_India",
    "Indonesia": "Country_Indonesia",
    "Italy": "Country_Italy",
    "Japan": "Country_Japan",
    "Malaysia": "Country_Malaysia",
    "Mexico": "Country_Mexico",
    "Nigeria": "Country_Nigeria",
    "Pakistan": "Country_Pakistan",
    "Russia": "Country_Russia",
    "Saudi Arabia": "Country_Saudi Arabia",
    "South Africa": "Country_South Africa",
    "South Korea": "Country_South Korea",
    "Spain": "Country_Spain",
    "Turkey": "Country_Turkey",
    "United Kingdom": "Country_United Kingdom",
    "United States": "Country_United States",
}

# -----------------------------
# Load model/data
# -----------------------------
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

@st.cache_data
def load_train_data():
    return pd.read_csv(TRAIN_PATH)

try:
    model = load_model()
    train_data = load_train_data()
except Exception as e:
    st.error(f"Could not load model/data: {e}")
    st.stop()

FEATURES = [c for c in train_data.columns if c != "target"]

if hasattr(model, "feature_names_in_"):
    FEATURES = list(model.feature_names_in_)

# -----------------------------
# SHAP explainer
# -----------------------------
@st.cache_resource
def make_shap_explainer(_model):
    return shap.TreeExplainer(_model)

try:
    shap_explainer = make_shap_explainer(model)
except Exception as e:
    shap_explainer = None
    st.warning(f"SHAP explainer could not be initialized: {e}")

# -----------------------------
# DiCE explainer
# -----------------------------
ORDINAL_COLS = [
    "Physical_Activity_Level",
    "Diet_Quality",
    "Sugar_Intake_Level",
    "Stress_Level",
    "Alcohol_Consumption",
]

BINARY_COLS = [
    "Family_History_Diabetes",
    "Hypertension",
    "Heart_Disease",
    "Fatty_Liver",
    "PCOS",
    "Doctor_Consultation_Needed",
    "Gender_Male",
    "Gender_Other",
    "Smoking_Status_Former",
    "Smoking_Status_Never",
    "Medication_Adherence_Good",
    "Medication_Adherence_Poor",
    "Work_Type_Government",
    "Work_Type_Private",
    "Work_Type_Retired",
    "Work_Type_Student",
    "Residence_Type_Urban",
] + list(COUNTRY_COLUMNS.values())

CATEGORICAL_COLS = [c for c in ORDINAL_COLS + BINARY_COLS if c in FEATURES]
CONTINUOUS_COLS = [c for c in FEATURES if c not in CATEGORICAL_COLS]

@st.cache_resource
def make_dice_explainer(_train_data, _model):
    data = dice_ml.Data(
        dataframe=_train_data,
        continuous_features=[c for c in CONTINUOUS_COLS if c in _train_data.columns],
        categorical_features=[c for c in CATEGORICAL_COLS if c in _train_data.columns],
        outcome_name="target",
    )
    dice_model = dice_ml.Model(
        model=_model,
        backend="sklearn",
        model_type="classifier",
    )
    return Dice(data, dice_model, method="random")

try:
    dice_explainer = make_dice_explainer(train_data, model)
except Exception as e:
    dice_explainer = None

# -----------------------------
# Helper functions
# -----------------------------
def one_hot_from_choice(row, prefix_columns, selected_column):
    for col in prefix_columns:
        row[col] = int(col == selected_column)

def build_input():
    row = {feature: 0 for feature in FEATURES}

    # Numerical inputs
    row["Age"] = age
    row["Height_cm"] = height
    row["Weight_kg"] = weight
    row["BMI"] = weight/((height/100)**2)
    row["Waist_Circumference_cm"] = waist
    row["Blood_Glucose"] = blood_glucose
    row["HbA1c"] = hba1c
    row["Fasting_Blood_Sugar"] = fasting_sugar
    row["Insulin_Level"] = insulin
    row["Blood_Pressure_Systolic"] = systolic
    row["Blood_Pressure_Diastolic"] = diastolic
    row["Total_Cholesterol"] = cholesterol
    row["HDL"] = hdl
    row["LDL"] = ldl
    row["Triglycerides"] = triglycerides
    row["Heart_Rate"] = heart_rate
    row["Physical_Activity_Level"] = activity_level
    row["Exercise_Hours_Per_Week"] = exercise_hours
    row["Daily_Walking_Minutes"] = walking
    row["Diet_Quality"] = diet_quality
    row["Sugar_Intake_Level"] = sugar_level
    row["Sleep_Hours"] = sleep
    row["Stress_Level"] = stress_level
    row["Alcohol_Consumption"] = alcohol
    row["Daily_Water_Intake_L"] = water

    # Binary health history
    row["Family_History_Diabetes"] = int(family_history == "Yes")
    row["Hypertension"] = int(hypertension == "Yes")
    row["Heart_Disease"] = int(heart_disease == "Yes")
    row["Fatty_Liver"] = int(fatty_liver == "Yes")
    row["PCOS"] = int(pcos == "Yes")
    row["Doctor_Consultation_Needed"] = int(doctor_consultation == "Yes")

    # Gender
    row["Gender_Male"] = int(gender == "Male")
    row["Gender_Other"] = int(gender == "Other")

    # Country
    for col in COUNTRY_COLUMNS.values():
        if col in row:
            row[col] = 0
    row[COUNTRY_COLUMNS[country]] = 1

    # Smoking: "Current" is the reference category in this encoding
    row["Smoking_Status_Former"] = int(smoking == "Former")
    row["Smoking_Status_Never"] = int(smoking == "Never")

    # Medication adherence: "Not specified" is the reference category
    row["Medication_Adherence_Good"] = int(medication == "Good")
    row["Medication_Adherence_Poor"] = int(medication == "Poor")

    # Work type: "Other" is the reference category
    row["Work_Type_Government"] = int(work_type == "Government")
    row["Work_Type_Private"] = int(work_type == "Private")
    row["Work_Type_Retired"] = int(work_type == "Retired")
    row["Work_Type_Student"] = int(work_type == "Student")

    # Residence: Rural is the reference category
    row["Residence_Type_Urban"] = int(residence == "Urban")

    return pd.DataFrame([[row[c] for c in FEATURES]], columns=FEATURES)

def get_class_shap_explanation(shap_values, input_data, predicted_class):
    values = np.asarray(shap_values.values)
    base = np.asarray(shap_values.base_values)

    if values.ndim == 3:
        class_values = values[0, :, predicted_class]
        if base.ndim == 2:
            base_value = base[0, predicted_class]
        else:
            base_value = base[predicted_class]
    elif values.ndim == 2:
        # Some SHAP versions represent one observation as (features, classes).
        class_values = values[:, predicted_class]
        if base.ndim == 1:
            base_value = base[predicted_class]
        else:
            base_value = base[0]
    else:
        class_values = values
        base_value = base[0] if base.ndim else base

    return shap.Explanation(
        values=class_values,
        base_values=base_value,
        data=input_data.iloc[0].values,
        feature_names=input_data.columns.tolist(),
    )

# -----------------------------
# UI
# -----------------------------
st.title("🩺 Explainable Diabetes Risk Prediction")
st.caption(
    "A prototype showing prediction, SHAP-based explanations, and "
    "counterfactual explanations."
)

st.info(
    "This is an educational/research prototype, not a medical diagnosis "
    "or treatment recommendation."
)

with st.expander("👤 Basic information", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age", 18.0, 90.0, 40.0, 1.0)
        gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        country = st.selectbox("Country", COUNTRIES, index=COUNTRIES.index("India"))
    with c2:
        height = st.number_input("Height (cm)", 145.0, 195.0, 170.0, 0.1)
        weight = st.number_input("Weight (kg)", 45.0, 130.0, 70.0, 0.1)
    with c3:
        waist = st.number_input("Waist circumference (cm)", 60.0, 140.0, 85.0, 0.1)
        residence = st.selectbox("Residence", ["Rural", "Urban"])
        work_type = st.selectbox(
            "Work type",
            ["Other", "Government", "Private", "Retired", "Student"]
        )

with st.expander("🧪 Blood & cardiovascular measurements", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        blood_glucose = st.number_input("Blood glucose", 70.0, 250.0, 100.0, 0.1)
        hba1c = st.number_input("HbA1c", 4.5, 12.5, 5.5, 0.1)
        fasting_sugar = st.number_input("Fasting blood sugar", 65.0, 220.0, 95.0, 0.1)
        insulin = st.number_input("Insulin level", 2.0, 45.0, 10.0, 0.1)
    with c2:
        systolic = st.number_input("Systolic BP", 90.0, 190.0, 120.0, 1.0)
        diastolic = st.number_input("Diastolic BP", 60.0, 120.0, 80.0, 1.0)
        heart_rate = st.number_input("Heart rate", 50.0, 120.0, 72.0, 1.0)
    with c3:
        cholesterol = st.number_input("Total cholesterol", 120.0, 320.0, 190.0, 1.0)
        hdl = st.number_input("HDL", 25.0, 90.0, 50.0, 1.0)
        ldl = st.number_input("LDL", 50.0, 220.0, 110.0, 1.0)
        triglycerides = st.number_input("Triglycerides", 60.0, 400.0, 140.0, 1.0)

with st.expander("🏃 Lifestyle", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        activity_level = st.selectbox(
            "Physical activity",
            [0, 1, 2],
            format_func=lambda x: {0: "Low", 1: "Moderate", 2: "High"}[x],
        )
        exercise_hours = st.number_input("Exercise hours/week", 0.0, 10.0, 3.0, 0.1)
        walking = st.number_input("Daily walking (minutes)", 0.0, 180.0, 30.0, 1.0)
    with c2:
        diet_quality = st.selectbox(
            "Diet quality",
            [0, 1, 2],
            format_func=lambda x: {0: "Poor", 1: "Average", 2: "Good"}[x],
        )
        sugar_level = st.selectbox(
            "Sugar intake",
            [0, 1, 2],
            format_func=lambda x: {0: "Low", 1: "Moderate", 2: "High"}[x],
        )
        alcohol = st.selectbox(
            "Alcohol consumption",
            [0, 1, 2],
            format_func=lambda x: {0: "Low", 1: "Moderate", 2: "High"}[x],
        )
    with c3:
        sleep = st.number_input("Sleep hours", 3.0, 10.0, 7.0, 0.1)
        stress_level = st.selectbox(
            "Stress level",
            [0, 1, 2],
            format_func=lambda x: {0: "Low", 1: "Moderate", 2: "High"}[x],
        )
        water = st.number_input("Daily water (L)", 1.0, 5.0, 2.0, 0.1)

with st.expander("🧬 Medical history", expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        family_history = st.selectbox("Family history of diabetes", ["No", "Yes"])
        hypertension = st.selectbox("Hypertension", ["No", "Yes"])
    with c2:
        heart_disease = st.selectbox("Heart disease", ["No", "Yes"])
        fatty_liver = st.selectbox("Fatty liver", ["No", "Yes"])
    with c3:
        pcos = st.selectbox("PCOS", ["No", "Yes"])
        doctor_consultation = st.selectbox(
            "Doctor consultation needed",
            ["No", "Yes"]
        )

with st.expander("🚬 Medication & smoking", expanded=False):
    c1, c2 = st.columns(2)
    with c1:
        smoking = st.selectbox(
            "Smoking status",
            ["Current", "Former", "Never"]
        )
    with c2:
        medication = st.selectbox(
            "Medication adherence",
            ["Not specified", "Good", "Poor"]
        )

st.divider()

# -----------------------------
# Prediction trigger
# -----------------------------
# NOTE ON THE FIX:
# Previously, everything below (prediction display, SHAP, AND the
# counterfactual section) lived inside `if st.button("Predict...")`.
# Clicking the *inner* "Generate Counterfactuals" button triggers a
# script rerun, and on that rerun the outer Predict button is no longer
# "pressed" (Streamlit buttons are only True on the run where they were
# clicked). So the whole outer `if` became False and everything vanished
# instead of showing counterfactual results.
#
# Fix: compute the prediction once and stash it in st.session_state.
# Rendering of results below is driven by session_state, not by the
# live truthiness of the Predict button, so the inner button no longer
# collapses the outer block.

if st.button("🔎 Predict Risk & Explain", type="primary", use_container_width=True):
    try:
        input_data = build_input()
        prediction = int(np.asarray(model.predict(input_data)).ravel()[0])
        probabilities = model.predict_proba(input_data)[0]

        st.session_state["input_data"] = input_data
        st.session_state["prediction"] = prediction
        st.session_state["probabilities"] = probabilities
        st.session_state["predicted"] = True
        # A fresh prediction invalidates any previously generated counterfactuals
        st.session_state.pop("cf_output", None)
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        st.exception(e)
        st.session_state["predicted"] = False

# -----------------------------
# Results (persisted across reruns)
# -----------------------------
if st.session_state.get("predicted"):
    input_data = st.session_state["input_data"]
    prediction = st.session_state["prediction"]
    probabilities = st.session_state["probabilities"]

    st.subheader("Prediction")

    risk_col, prob_col = st.columns([1, 2])

    with risk_col:
        if prediction == 2:
            st.error(f"### {RISK_LABELS[prediction]}")
        elif prediction == 1:
            st.warning(f"### {RISK_LABELS[prediction]}")
        else:
            st.success(f"### {RISK_LABELS[prediction]}")

    with prob_col:
        prob_df = pd.DataFrame({
            "Risk level": [RISK_LABELS[i] for i in range(len(probabilities))],
            "Probability": [f"{p * 100:.2f}%" for p in probabilities],
        })
        st.dataframe(prob_df, hide_index=True, use_container_width=True)

    # -------------------------
    # SHAP
    # -------------------------
    if shap_explainer is not None:
        st.divider()
        st.subheader("🔍 Why did the model make this prediction?")

        shap_values = shap_explainer(input_data)
        explanation = get_class_shap_explanation(
            shap_values,
            input_data,
            prediction
        )

        # Top 5 local contributions
        abs_values = np.abs(explanation.values)
        top_idx = np.argsort(abs_values)[::-1][:5]

        top_explanation = shap.Explanation(
            values=explanation.values[top_idx],
            base_values=explanation.base_values,
            data=explanation.data[top_idx],
            feature_names=[
                explanation.feature_names[i] for i in top_idx
            ],
        )

        fig, ax = plt.subplots(figsize=(10, 5))
        shap.plots.waterfall(top_explanation, show=False, max_display=5)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        st.markdown(
            f"**Interpretation:** The SHAP explanation above shows which "
            f"features pushed this specific prediction toward "
            f"**{RISK_LABELS[prediction]}**. Red contributions push the "
            f"selected class output upward; blue contributions push it downward."
        )

        for idx in top_idx:
            feature = explanation.feature_names[idx]
            contribution = explanation.values[idx]
            label = FEATURE_LABELS.get(feature, feature)

            if contribution > 0:
                st.write(
                    f"🔴 **{label}** pushed the model toward "
                    f"**{RISK_LABELS[prediction]}** "
                    f"(SHAP: +{contribution:.3f})."
                )
            else:
                st.write(
                    f"🔵 **{label}** pushed the model away from "
                    f"**{RISK_LABELS[prediction]}** "
                    f"(SHAP: {contribution:.3f})."
                )

    # -------------------------
    # Counterfactual
    # -------------------------
    st.divider()
    st.subheader("🔄 What could change the prediction?")

    target_risk = st.selectbox(
        "Choose a desired risk class",
        options=[0, 1, 2],
        index=1 if prediction == 2 else 2,
        format_func=lambda x: RISK_LABELS[x],
        key="cf_target",
    )

    # We deliberately avoid immutable/difficult-to-change variables
    # and avoid changing BMI independently because BMI is derived from
    # height/weight.
    modifiable_options = [
        "Weight_kg",
        "Waist_Circumference_cm",
        "Blood_Glucose",
        "HbA1c",
        "Fasting_Blood_Sugar",
        "Insulin_Level",
        "Blood_Pressure_Systolic",
        "Blood_Pressure_Diastolic",
        "Total_Cholesterol",
        "HDL",
        "LDL",
        "Triglycerides",
        "Exercise_Hours_Per_Week",
        "Daily_Walking_Minutes",
        "Diet_Quality",
        "Sugar_Intake_Level",
        "Sleep_Hours",
        "Stress_Level",
        "Alcohol_Consumption",
        "Daily_Water_Intake_L",
    ]
    modifiable_options = [c for c in modifiable_options if c in FEATURES]

    selected_features = st.multiselect(
        "Features DiCE is allowed to change",
        options=modifiable_options,
        default=[
            c for c in [
                "Weight_kg",
                "Blood_Glucose",
                "HbA1c",
                "Exercise_Hours_Per_Week",
                "Stress_Level",
            ] if c in modifiable_options
        ],
        format_func=lambda x: FEATURE_LABELS.get(x, x),
        key="cf_features",
    )

    if target_risk == prediction:
        st.info("Choose a different target risk class to generate counterfactuals.")
    elif not selected_features:
        st.info("Select at least one feature that DiCE is allowed to change.")
    elif dice_explainer is None:
        st.error(
            "DiCE could not be initialized. Check the dice-ml installation "
            "and the model/data versions."
        )
    else:
        if st.button("Generate Counterfactuals", type="secondary"):
            with st.spinner("Searching for valid counterfactuals..."):
                try:
                    # Only continuous features need permitted numeric ranges.
                    permitted_range = {}
                    for feature in selected_features:
                        if feature in CONTINUOUS_COLS:
                            permitted_range[feature] = [
                                float(train_data[feature].min()),
                                float(train_data[feature].max()),
                            ]

                    cfs = dice_explainer.generate_counterfactuals(
                        input_data,
                        total_CFs=3,
                        desired_class=target_risk,
                        features_to_vary=selected_features,
                        permitted_range=permitted_range or None,
                    )

                    if not cfs.cf_examples_list:
                        st.session_state["cf_output"] = None
                        st.warning("No counterfactuals were found.")
                    else:
                        cf_df = cfs.cf_examples_list[0].final_cfs_df

                        if cf_df is None or cf_df.empty:
                            st.session_state["cf_output"] = None
                            st.warning(
                                "DiCE could not find a counterfactual in the "
                                "requested target class."
                            )
                        else:
                            # Stash results in session_state so they survive
                            # future reruns (e.g. touching another widget)
                            # instead of vanishing.
                            st.session_state["cf_output"] = {
                                "cf_df": cf_df,
                                "target_risk": target_risk,
                                "selected_features": list(selected_features),
                                "input_data": input_data,
                            }

                except Exception as e:
                    st.session_state["cf_output"] = None
                    st.error(
                        "Counterfactual generation failed. "
                        "This can happen when the requested class is difficult "
                        "to reach with the selected features."
                    )
                    st.exception(e)

        # Render the most recently generated counterfactuals, if any.
        cf_output = st.session_state.get("cf_output")
        if cf_output is not None:
            cf_df = cf_output["cf_df"]
            cf_target_risk = cf_output["target_risk"]
            cf_selected_features = cf_output["selected_features"]
            cf_input_data = cf_output["input_data"]

            st.success(
                f"Found {len(cf_df)} counterfactual(s) targeting "
                f"**{RISK_LABELS[cf_target_risk]}**."
            )

            for i, (_, cf) in enumerate(cf_df.iterrows(), start=1):
                st.markdown(f"### Counterfactual {i}")

                cf_features = cf[FEATURES].to_frame().T
                cf_prediction = int(
                    np.asarray(model.predict(cf_features)).ravel()[0]
                )
                cf_probability = float(
                    model.predict_proba(cf_features)[0][cf_prediction]
                )

                st.write(
                    f"**New prediction:** {RISK_LABELS[cf_prediction]} "
                    f"({cf_probability * 100:.2f}% model probability)"
                )

                changes = []
                for feature in cf_selected_features:
                    original = cf_input_data.iloc[0][feature]
                    new = cf[feature]

                    if feature in CATEGORICAL_COLS:
                        changed = original != new
                    else:
                        changed = not np.isclose(
                            float(original),
                            float(new),
                            rtol=1e-5,
                            atol=1e-6
                        )

                    if changed:
                        label = FEATURE_LABELS.get(feature, feature)

                        if feature in CATEGORICAL_COLS:
                            changes.append(
                                f"**{label}:** {int(original)} → {int(new)}"
                            )
                        else:
                            changes.append(
                                f"**{label}:** "
                                f"{float(original):.2f} → {float(new):.2f}"
                            )

                if changes:
                    st.markdown("**Suggested changes:**")
                    for change in changes:
                        st.markdown(f"- {change}")
                else:
                    st.write("No selected features changed.")

st.divider()
st.caption(
    "XAI methods: XGBoost • SHAP • DiCE | "
    "Use this application for educational/research purposes only."
)