# Problem Statement

Modern civil infrastructure often requires advanced ground motion characterization, including the joint hazard across multiple periods and locations. The goal of this exercise is to develop a simple ground motion model that addresses this objective using the NGA-West2 Effective Amplitude Spectrum (EAS) dataset.

The provided dataframe includes:

- **Source, path, and site metadata**, such as:
  - Moment magnitude: `mag`
  - Rupture distance: `Rrup`
  - Time-averaged shear-wave velocity in the top 30 m: `Vs30`
- **Earthquake and station locations in UTM coordinates**:
  - Earthquake: `eqUTMx`, `eqUTMy`
  - Station: `staUTMx`, `staUTMy`
- **Effective amplitude spectral values at different frequencies**:
  - Columns of the form: `freqX` where `X` is the frequency value
- **Residuals with respect to the Bayless and Abrahamson (2018) EAS GMM**:
  - Columns of the form: `resid_freqX` where `X` is the frequency value

You may choose to work either directly with the ground motion values or with the residuals relative to the Bayless and Abrahamson (2018) model.

---

## Task

Develop a **ground motion model** that:

1. Captures the correlation of at least five frequencies in the range 0.25–5 Hz.  
2. Includes magnitude, distance, and Vs30 scaling, that is, the model should depend on:
   - Magnitude `M`
   - Rupture distance `R`
   - Site parameter `Vs30`
3. Is a function of both source and site location, for example through the UTM coordinates of the earthquake and station.

You are free to use any statistical or machine learning framework** that you consider appropriate (for example, linear models, Gaussian processes, neural networks, Optimal transport mapping, or others), provided that the model structure and assumptions are clearly documented.

---

## Expected Deliverables

Prepare a **10-minute presentation** summarizing:

- The **modeling approach**, including:
  - Choice of variables and features
  - Modeling framework and assumptions
  - Treatment of frequency correlation
- **Results and evaluation**, which may include:
  - Summary figures and tables showing the fit to the observed data
  - Diagnostics or residual analyses
- **Scenario-based evaluations**, for example:
  - Predicted EAS or residuals across multiple periods for a given earthquake scenario  
    (fixed `M`, `R`, and `Vs30`)
  - Predicted variation at a single frequency as a function of:
    - Magnitude `M`
    - Distance `R`
    - Site condition `Vs30`

Please ensure that your figures and tables are clearly labeled and that your assumptions and choices are explained in a concise and transparent manner.
