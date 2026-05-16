from __future__ import annotations

import math
from typing import Dict, List

import numpy as np
import pandas as pd
import streamlit as st


CATEGORIES = [
    "Insufficient Weight",
    "Normal Weight",
    "Overweight Level I",
    "Overweight Level II",
    "Obesity Type I",
    "Obesity Type II",
    "Obesity Type III",
]


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def ordinal_probabilities(score: float, cutpoints: List[float]) -> List[float]:
    """Convert a latent risk score into ordered-category probabilities."""
    cumulative = [sigmoid(c - score) for c in cutpoints]
    probs = []
    prev = 0.0
    for cdf in cumulative:
        probs.append(max(cdf - prev, 0.0))
        prev = cdf
    probs.append(max(1.0 - prev, 0.0))
    total = sum(probs)
    return [p / total for p in probs]


def compute_demo_score(inputs: Dict[str, float]) -> float:
    """Transparent simulator score.

    This is not a replacement for your R/JAGS model. It simply creates a coherent
    interactive demo until real coefficients/posterior summaries are exported.
    """
    bmi = inputs["weight"] / (inputs["height"] ** 2)
    score = 0.0
    score += 0.42 * (bmi - 24.0)
    score += 0.012 * (inputs["age"] - 30.0)
    score += 0.20 if inputs["family_history"] else -0.15
    score += -0.10 * (inputs["vegetable_consumption"] - 2.0)
    score += 0.12 * (inputs["snacking_level"] - 1.0)
    score += -0.10 * (inputs["physical_activity"] - 1.0)
    score += -0.06 * (inputs["water_intake"] - 2.0)
    score += 0.07 * (inputs["technology_use"] - 1.0)
    return score


def make_prediction(inputs: Dict[str, float]) -> pd.DataFrame:
    cutpoints = [-4.5, -2.2, -0.7, 0.4, 1.5, 2.8]
    score = compute_demo_score(inputs)
    probs = ordinal_probabilities(score, cutpoints)
    return pd.DataFrame({"Category": CATEGORIES, "Probability": probs})


st.set_page_config(
    page_title="Bayesian Obesity Ordinal Regression Demo",
    page_icon="📊",
    layout="wide",
)

st.title("Bayesian Ordinal Regression for Obesity Level Prediction")
st.caption("Interactive portfolio dashboard for Saeed Zohoorian's Bayesian ordinal-regression project")

st.warning(
    "This app currently runs in demo-simulator mode. It is ready for deployment, "
    "but you should export your real R/JAGS model parameters before presenting it as real model inference."
)

with st.sidebar:
    st.header("Input profile")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.slider("Age", 14, 65, 25)
    height = st.slider("Height (m)", 1.40, 2.05, 1.72, 0.01)
    weight = st.slider("Weight (kg)", 40, 180, 75)
    family_history = st.checkbox("Family history with overweight", value=True)
    vegetable_consumption = st.slider("Vegetable consumption frequency", 1.0, 3.0, 2.0, 0.1)
    meals = st.slider("Number of main meals", 1.0, 4.0, 3.0, 0.1)
    water_intake = st.slider("Daily water intake level", 1.0, 3.0, 2.0, 0.1)
    physical_activity = st.slider("Physical activity frequency", 0.0, 3.0, 1.0, 0.1)
    technology_use = st.slider("Technology use time", 0.0, 2.0, 1.0, 0.1)
    snacking = st.selectbox("Snacking between meals", ["No", "Sometimes", "Frequently", "Always"], index=1)

snacking_map = {"No": 0.0, "Sometimes": 1.0, "Frequently": 2.0, "Always": 3.0}
inputs = {
    "gender": 1.0 if gender == "Male" else 0.0,
    "age": float(age),
    "height": float(height),
    "weight": float(weight),
    "family_history": bool(family_history),
    "vegetable_consumption": float(vegetable_consumption),
    "meals": float(meals),
    "water_intake": float(water_intake),
    "physical_activity": float(physical_activity),
    "technology_use": float(technology_use),
    "snacking_level": snacking_map[snacking],
}

bmi = weight / (height ** 2)
pred_df = make_prediction(inputs)
top_row = pred_df.iloc[pred_df["Probability"].idxmax()]

col1, col2, col3 = st.columns(3)
col1.metric("BMI", f"{bmi:.1f}")
col2.metric("Most likely class", top_row["Category"])
col3.metric("Top probability", f"{top_row['Probability']:.1%}")

left, right = st.columns([1.2, 1])
with left:
    st.subheader("Predicted ordered-category probabilities")
    st.bar_chart(pred_df.set_index("Category"))

with right:
    st.subheader("Probability table")
    st.dataframe(
        pred_df.assign(Probability=lambda d: (100 * d["Probability"]).round(2)),
        use_container_width=True,
        hide_index=True,
    )

st.subheader("What this project proves")
st.markdown(
    """
- You can model ordered target variables instead of forcing plain multiclass classification.
- You compared Bayesian and frequentist approaches.
- You considered diagnostics, calibration, and model comparison instead of only accuracy.
- The next professional step is exporting fitted parameters so this dashboard uses real posterior predictions.
    """
)
