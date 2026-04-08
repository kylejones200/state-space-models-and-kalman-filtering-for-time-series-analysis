# State Space Models for Time Series: Beyond Kalman Filtering


Focus: Structural time series, dynamic linear models, practical applications  
Dataset: Oklahoma Energy Consumption (use_OK.csv)

## Introduction

State space models provide a flexible framework for time series with unobserved components such as trend, seasonality, and latent shocks. Instead of modeling the observed series directly, you describe how hidden states evolve over time and how they generate observations. We explore structural time series models and dynamic linear models beyond basic Kalman filtering.

## Dataset: Oklahoma Energy Consumption

We use the same Oklahoma energy consumption series as in earlier articles: an annual time series covering multiple decades. The aggregated series has 64 observations from 1960 to 2023, with total consumption rising from roughly 8.7 million units at the beginning of the sample to around 24.8 million units at the end. This makes it a good candidate for state space modeling, because it combines a long-term upward trend driven by population and economic growth, structural changes from policy shifts and efficiency improvements, and year-to-year noise that we want to separate from the underlying signal.

## Basic Kalman Filter

The Kalman filter is the workhorse algorithm for linear Gaussian state space models. At its core, it combines two ingredients: a state transition equation describing how hidden states evolve over time and an observation equation describing how those states map to observable data. The filter alternates between a prediction step, which propagates the current state and its uncertainty forward using the transition equation, and an update step, which refines that prediction using new observations and their measurement noise. In the simplest local-level model for energy demand, the hidden state is the underlying consumption level, which evolves smoothly with Gaussian process noise while observations add additional measurement noise.

## Structural Time Series

Structural time series models make the unobserved components explicit. A typical specification for annual energy consumption might include a local level representing slowly evolving baseline demand, a local trend capturing growth or decline over time, and optional seasonal or cycle components if the data were higher frequency. Fitting such a model with a Kalman filter and smoother lets you decompose the observed series into interpretable pieces: how much of the movement is long-term trend, how much is shorter-term fluctuation, and how much is unexplained noise. In our Oklahoma example, the structural model estimated by the new script produces a smoothed trend that tracks the long-run growth in consumption while filtering out year-to-year volatility; this decomposition is visualized in `kalman_decomposition.png`, where the Kalman-smoothed level overlays the raw series.

## Dynamic Linear Models

Dynamic linear models (DLMs) extend this framework by allowing regression coefficients themselves to evolve over time. For example, you could regress consumption on production, prices, or weather, while allowing the sensitivity to each driver to change year by year.

In practice, you specify a state vector that includes both latent levels/trends and time-varying regression coefficients, then use the Kalman filter to update that full state as new data arrives. This makes DLMs powerful tools for modeling **time-varying relationships** in energy systems.

## Applications

State space models and Kalman filtering are widely used across domains. In energy and utilities, they underpin load forecasting and real-time state estimation in grid operations. In finance, they drive volatility models and latent factor tracking. Navigation and control systems, such as GPS receivers and autonomous robots, rely on Kalman variants for sensor fusion, while econometrics uses structural state space models for trend–cycle decomposition and intervention analysis. For Oklahoma’s energy consumption, the state space approach implemented in the new script delivers more than just a forecast: it yields a decomposition into interpretable components and a principled way to update your beliefs as new data arrives, and it produces a multi-step forecast with uncertainty bands (shown in `kalman_forecast.png`) that extend the historical trend into the future while quantifying the range of plausible outcomes.


