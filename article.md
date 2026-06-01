# State Space Models and Kalman Filtering for Time Series Analysis

*Techniques for understanding the hidden states of time series data*

---

Most time series models work directly with observed values. State space models take a different approach: they assume there is an underlying hidden state — a true signal — and that what you observe is that signal corrupted by noise. The model estimates the hidden state at each point in time, filtering out the noise.

The Kalman filter is the algorithm that does this estimation for linear systems. It is the engine behind GPS navigation, spacecraft guidance, financial smoothing models, and econometric decompositions. Understanding it gives you a fundamentally different way to think about time series.

## The Two Equations

Every state space model has two equations.

**State transition equation** (how the hidden state evolves):

```
x_t = F · x_{t-1} + w_t,    w_t ~ N(0, Q)
```

- `x_t` — the hidden state at time t
- `F` — transition matrix (how the state moves forward)
- `w_t` — process noise with covariance Q

**Observation equation** (how measurements relate to the state):

```
y_t = H · x_t + v_t,    v_t ~ N(0, R)
```

- `y_t` — what you actually observe
- `H` — measurement matrix (which parts of the state you see)
- `v_t` — measurement noise with covariance R

The key parameters to tune are Q (how much you trust your model of how the state evolves) and R (how much you trust your measurements). High Q means the state can change rapidly. High R means your measurements are noisy and the filter should weight them less.

## The Kalman Filter Algorithm

The filter operates in two steps at each time point:

**Predict** — project the state estimate forward using the transition model:

```
x̂_{t|t-1} = F · x̂_{t-1|t-1}
P_{t|t-1} = F · P_{t-1|t-1} · F' + Q
```

**Update** — incorporate the new observation to correct the prediction:

```
K_t = P_{t|t-1} · H' · (H · P_{t|t-1} · H' + R)^{-1}
x̂_{t|t} = x̂_{t|t-1} + K_t · (y_t - H · x̂_{t|t-1})
P_{t|t} = (I - K_t · H) · P_{t|t-1}
```

`K_t` is the Kalman gain — the weight given to the new observation vs. the prior prediction. When R is small (measurements are accurate), the gain is high and the filter trusts observations. When Q is small (the model is reliable), the gain is low and the filter trusts the prediction.

## Python Implementation

`statsmodels` provides a clean state space interface through `UnobservedComponents`:

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm

np.random.seed(42)
n = 200
true_state = np.cumsum(np.random.normal(0, 0.5, n))
observed = true_state + np.random.normal(0, 2.0, n)

model = sm.tsa.UnobservedComponents(
    observed,
    level='local level'
)
result = model.fit(disp=False)

filtered = result.filtered_state[0]
smoothed = result.smoothed_state[0]
```

The `local level` specification is the simplest state space model: the hidden state is a random walk and observations are noisy measurements of it. The filter recovers the true underlying level.

`filtered_state` uses only information up to time t (causal). `smoothed_state` uses the full dataset (non-causal). For forecasting, use filtered. For retrospective analysis of what the true state was, use smoothed.

## Practical Example: Object Tracking

Consider tracking an object moving along a sinusoidal path with noisy position sensors. The state vector holds position and velocity:

```python
dt = 0.1
F = np.array([[1, dt], [0, 1]])  # constant velocity model
H = np.array([[1, 0]])            # we observe position only
Q = np.eye(2) * 0.01             # small process noise
R = np.array([[4.0]])            # noisy sensor

x = np.array([0.0, 0.0])        # initial state
P = np.eye(2)                    # initial covariance

filtered_positions = []
for y_t in noisy_observations:
    # Predict
    x = F @ x
    P = F @ P @ F.T + Q
    # Update
    K = P @ H.T @ np.linalg.inv(H @ P @ H.T + R)
    x = x + K @ (y_t - H @ x)
    P = (np.eye(2) - K @ H) @ P
    filtered_positions.append(x[0])
```

The filter outputs a smooth position estimate even when individual measurements are scattered. The velocity state is never directly observed but is estimated from the pattern of position changes.

## Advanced Filters for Nonlinear Systems

The standard Kalman filter assumes linear state transitions and Gaussian noise. Two extensions handle nonlinear systems:

**Extended Kalman Filter (EKF)** — linearizes the nonlinear model at each step using a first-order Taylor expansion. Jacobian matrices replace the linear transition and measurement matrices. Fast but can diverge when the nonlinearity is severe.

**Unscented Kalman Filter (UKF)** — propagates a set of carefully chosen "sigma points" through the nonlinear function and reconstructs the mean and covariance from the results. More accurate than EKF for strongly nonlinear systems because it captures higher-order effects without requiring Jacobians. Preferred for modern navigation and autonomous systems.

For non-Gaussian noise (outliers, multimodal distributions), neither filter is optimal — particle filters handle those cases at significantly higher computational cost.

## Choosing Q and R

This is the hardest part of practical Kalman filtering. Some guidelines:

- **Start with R from sensor specifications** if available. Measurement noise is often characterized by hardware manufacturers.
- **Tune Q based on how quickly the true state changes.** A slowly drifting signal needs small Q. A rapidly varying signal needs large Q.
- **If the filter is slow to respond to real changes**, Q is probably too small.
- **If the filtered output is noisy**, Q is probably too large or R too small.

The ratio Q/R matters more than the absolute values.

## Conclusion

State space models and Kalman filtering offer a principled framework for separating signal from noise in time series data. The two-equation structure is flexible enough to model position tracking, economic trend decomposition, seasonal adjustment, and latent factor models — all with the same algorithm.

For linear systems with Gaussian noise, the Kalman filter is optimal — it is mathematically provable that no other algorithm produces better estimates. For nonlinear or non-Gaussian systems, EKF and UKF provide practical approximations.

The `statsmodels` `UnobservedComponents` class is the easiest entry point in Python. For custom state spaces, implement the predict-update loop directly in NumPy — it is only about 10 lines of code.
