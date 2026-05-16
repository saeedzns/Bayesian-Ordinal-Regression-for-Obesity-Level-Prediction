# Bayesian obesity ordinal-regression Streamlit dashboard

This demo is for:

`Bayesian-Ordinal-Regression-for-Obesity-Level-Prediction`

## What it does

It creates an interactive dashboard where users adjust demographic/lifestyle variables and see predicted probabilities across ordered obesity categories.

## Current mode

This app runs in transparent `demo-simulator` mode unless you add exported model parameters.

Your current repo is an R Markdown analysis. To make the app use your real model, export posterior summaries or coefficients from R to JSON and update `load_model_parameters()` in `streamlit_app.py`.

## How to deploy on Streamlit Community Cloud

1. Copy these files to the root of the repo:

```text
streamlit_app.py
requirements.txt
```

2. Push to GitHub.
3. Go to Streamlit Community Cloud.
4. Create a new app from your GitHub repo.
5. Main file path:

```text
streamlit_app.py
```

## Suggested next improvement

In R, export final model parameters like this:

```r
library(jsonlite)
params <- list(
  intercepts = c(-2.1, -1.2, -0.4, 0.3, 1.1, 2.0),
  beta = list(BMI=0.85, Age=0.03, FAF=-0.18, FCVC=-0.12, CH2O=-0.10, TUE=0.08)
)
write_json(params, "model_params.json", auto_unbox = TRUE, pretty = TRUE)
```

Then change the Python app to read `model_params.json`.
