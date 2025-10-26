# Bayesian Ordinal Regression for Obesity Level Prediction (R)

A full Bayesian analysis of obesity categories using ordinal regression models, comparing **Proportional Odds (PO)** and **Partial Proportional Odds (PPO)** structures across **Bayesian** and **Frequentist** frameworks.  

This project explores how lifestyle, diet, and behavior predict obesity levels among individuals from **Mexico, Peru, and Colombia**, using modern probabilistic modeling with rich diagnostics and comparison metrics.

---

## 🔍 Overview

**Goal:**  
To model the ordered categorical variable *Obesity Category* using predictors related to diet, activity, and lifestyle, and evaluate predictive performance under Bayesian and frequentist paradigms.

**Key Tasks:**
- Explore obesity category distributions and predictor characteristics.  
- Perform extensive **exploratory data analysis (EDA)**.  
- Build and compare:
  - Bayesian **Proportional Odds (PO)** and **Partial Proportional Odds (PPO)** models (via *JAGS*).  
  - Frequentist PO and PPO models (via *ordinal::clm()*).  
- Conduct full diagnostics: convergence checks, residuals, calibration, PPC, and WAIC/LOO model comparison.  
- Evaluate and compare predictive accuracy (Brier Score, Log Loss, Accuracy, MAE).

---

## 🧠 What the Model Does

**Input:**  
- Dataset: UCI *Estimation of Obesity Levels Based on Eating Habits and Physical Condition*  
- 2111 samples, 17 attributes from Mexico, Peru, and Colombia  
- Mix of **demographic**, **behavioral**, and **dietary** predictors  

**Process:**  
1. **Preprocessing & Feature Engineering**
   - Clean and rename variables  
   - Encode categorical predictors  
   - Compute **BMI = Weight / Height²**  
   - Feature selection via mutual information, ANOVA, chi-square, and Random Forest importance  
   - Exclude weak predictors (`SMOKE`, `SCC`, `FAVC`, `CALC`, `MTRANS`)  

2. **Exploratory Data Analysis**
   - Visualize continuous vs categorical variables  
   - Examine correlations, feature distributions, and multicollinearity  

3. **Modeling**
   - **Bayesian PO model (JAGS):** Ordered logit with weakly informative priors, cumulative cutpoints, and convergence diagnostics  
   - **Bayesian PPO model:** Allows threshold-specific predictor effects, improving flexibility  
   - **Frequentist PO & PPO:** Using `ordinal::clm()` for comparison  

4. **Diagnostics**
   - MCMC convergence (traceplots, density, ACF, R̂, ESS)  
   - Posterior Predictive Checks (PPC)  
   - Residual and calibration analysis  
   - WAIC and PSIS-LOO  

**Output:**  
- Posterior estimates, convergence plots, and residual diagnostics  
- Category-level calibration and predictive accuracy  
- Comparative metrics (Brier, LogLoss, Accuracy, MAE) across four models  
- Visual diagnostics: PPC, QQ, calibration, and proportional-odds checks  

---

## 📊 Dataset Summary

- Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition)  
- 2111 records, 17 features  
- ~77% synthetically generated via *Weka + SMOTE*, ~23% real web data  
- Target: `NObeyesdad` (7 ordered obesity levels)  
- Selected predictors include:
  - `Gender`, `Age`, `BMI`, `Family_history_with_overweight`
  - `Vegetable Consumption (FCVC)`
  - `Number of Meals (NCP)`
  - `Water Intake (CH2O)`
  - `Physical Activity (FAF)`
  - `Technology Use (TUE)`
  - `Snacking Habits (CAEC)`

---

## ⚙️ Environment & Dependencies

**Language:** R ≥ 4.2  
**Key Packages:**
```
brms, rjags, coda, bayesplot, loo, ordinal, 
FSelectorRcpp, ggplot2, dplyr, patchwork, corrplot, randomForest
```

Install dependencies in R:

```r
install.packages(c("brms", "rjags", "bayesplot", "loo", "ordinal",
                   "FSelectorRcpp", "randomForest", "patchwork", "corrplot"))
```

---

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/Bayesian-Obesity-Ordinal-Regression.git
   cd Bayesian-Obesity-Ordinal-Regression
   ```

2. **Open the R Markdown file**
   - `obesity_analysis.Rmd`  
   or render directly:
   ```r
   rmarkdown::render("obesity_analysis.Rmd", output_format = "html_document")
   ```

3. **Outputs generated:**
   - Summary tables for variables and models  
   - Visualizations (EDA, correlations, boxplots, density plots)  
   - MCMC diagnostics and PPC plots  
   - Model comparison metrics (WAIC, LOO, AIC, BIC, Accuracy, LogLoss)

---

## 📈 Results Summary

| Model | Framework | Brier ↓ | LogLoss ↓ | Accuracy ↑ | MAE ↓ | Notes |
|-------|------------|---------|------------|-------------|--------|--------|
| **Bayes_PPO** | Bayesian | **0.0837** | 0.1012 | **0.9493** | 0.112 | Best calibration and accuracy |
| **Bayes_PO** | Bayesian | 0.0895 | 0.1049 | 0.9418 | 0.103 | Stable and interpretable baseline |
| **Freq_PPO** | Frequentist | 0.1651 | **0.0983** | 0.7712 | 0.129 | Sharp but unstable (singularities) |
| **Freq_PO** | Frequentist | 0.0923 | 0.1057 | 0.9314 | **0.0898** | Best ordinal distance |

**Interpretation:**  
- **Bayesian PPO** yields the best balance between calibration and accuracy.  
- **Frequentist PPO** fits sharply but is numerically unstable.  
- **Frequentist PO** performs well for ordinal closeness (low MAE).  
- **Bayesian PO** provides robust, regularized inference.

---

## 🧩 Model Comparison Summary

| Criterion | Best Model | Comment |
|------------|-------------|----------|
| **WAIC / LOO** | Bayesian PPO | Improved predictive performance |
| **AIC / BIC** | Frequentist PPO | Better likelihood, penalized complexity |
| **Calibration** | Bayesian PPO | Best alignment between predicted and observed |
| **Residuals** | Both Bayesian models | Mild tail misfit, otherwise stable |

---

## 🧾 Conclusion

- **Bayesian PPO** is the preferred model for this dataset — it offers **well-calibrated, interpretable, and probabilistically consistent** predictions.  
- **Frequentist PO** remains a reliable baseline when prioritizing simplicity.  
- The **PPO framework** successfully captures threshold-specific effects and improves model fit.  
- The analysis demonstrates how **Bayesian regularization** stabilizes inference and enhances interpretability under ordinal data.

---

## 📚 Citation

If you use or adapt this work, please cite:

> Zohoorian, S. (2025). *Bayesian Ordinal Regression for Obesity Prediction.*  
> Comparative Bayesian and Frequentist Analysis using JAGS and Ordinal Models in R.

---

## 📄 License

This repository is distributed for academic and educational use.  
Attribution required for reuse.
