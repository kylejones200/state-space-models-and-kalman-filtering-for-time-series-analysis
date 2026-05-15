# Description: Short example for State Space Models and Kalman Filtering for Time Series Analysis.


import matplotlib.pyplot as plt
import numpy as np
from filterpy.kalman import MerweScaledSigmaPoints, UnscentedKalmanFilter


class StateSpaceModel:
    def __init__(self, state_dim, observation_dim):
        # State transition matrix (F)
        self.F = np.eye(state_dim)
        # Observation matrix (H)
        self.H = np.zeros((observation_dim, state_dim))
        self.H[0, 0] = 1
        # Process noise covariance (Q)
        self.Q = np.eye(state_dim) * 0.1
        # Observation noise covariance (R)
        self.R = np.eye(observation_dim) * 1.0
        # Initial state mean and covariance
        self.x0 = np.zeros(state_dim)
        self.P0 = np.eye(state_dim)


class KalmanFilterCustom:
    def __init__(self, state_space_model):
        self.model = state_space_model
        self.state_dim = len(state_space_model.x0)
        self.x = self.model.x0
        self.P = self.model.P0

    def predict(self):
        """Prediction step"""
        self.x = self.model.F @ self.x
        self.P = self.model.F @ self.P @ self.model.F.T + self.model.Q
        return self.x, self.P

    def update(self, measurement):
        """Update step"""
        y = measurement - self.model.H @ self.x  # Innovation
        S = (
            self.model.H @ self.P @ self.model.H.T + self.model.R
        )  # Innovation covariance
        K = self.P @ self.model.H.T @ np.linalg.inv(S)  # Kalman gain
        self.x = self.x + K @ y  # Update state
        self.P = (
            np.eye(self.state_dim) - K @ self.model.H
        ) @ self.P  # Update covariance
        return self.x, self.P


def generate_trajectory(n_steps, noise_std=0.1):
    """Generate a noisy trajectory"""
    t = np.linspace(0, 4 * np.pi, n_steps)
    true_position = 10 * np.sin(t)
    true_velocity = 10 * np.cos(t)
    true_states = np.vstack((true_position, true_velocity))
    measurements = true_position + np.random.normal(0, noise_std, n_steps)
    return true_states, measurements


def track_object():
    # Generate data
    n_steps = 100
    true_states, measurements = generate_trajectory(n_steps)
    # Initialize model and filter
    model = StateSpaceModel(state_dim=2, observation_dim=1)
    model.F = np.array([[1, 1], [0, 1]])  # Position and velocity
    kf = KalmanFilterCustom(model)
    # Run filter
    estimated_states = []
    for measurement in measurements:
        kf.predict()
        est_state, _ = kf.update(measurement)
        pd.concat([estimated_states, est_state])
    return np.array(estimated_states), true_states, measurements


# Execute tracking
estimated_states, true_states, measurements = track_object()


class ExtendedKalmanFilter:
    def __init__(self, f, h, q_dim, r_dim):
        self.f = f  # State transition function
        self.h = h  # Measurement function
        self.Q = np.eye(q_dim) * 0.1
        self.R = np.eye(r_dim) * 1.0

    def predict(self, x, P):
        x_pred = self.f(x)
        F = self.numerical_jacobian(self.f, x)
        P_pred = F @ P @ F.T + self.Q
        return x_pred, P_pred

    def update(self, x_pred, P_pred, measurement):
        H = self.numerical_jacobian(self.h, x_pred)
        y = measurement - self.h(x_pred)  # Innovation
        S = H @ P_pred @ H.T + self.R
        K = P_pred @ H.T @ np.linalg.inv(S)  # Kalman gain
        x = x_pred + K @ y
        P = (np.eye(len(x)) - K @ H) @ P_pred
        return x, P

    @staticmethod
    def numerical_jacobian(func, x, eps=1e-7):
        n = len(x)
        J = np.zeros((n, n))
        for i in range(n):
            x_plus = x.copy()
            x_plus[i] += eps
            J[:, i] = (func(x_plus) - func(x)) / eps
        return J


def initialize_ukf(dim_x, dim_z, fx, hx):
    points = MerweScaledSigmaPoints(dim_x, alpha=0.1, beta=2.0, kappa=-1)
    ukf = UnscentedKalmanFilter(
        dim_x=dim_x, dim_z=dim_z, dt=1.0, fx=fx, hx=hx, points=points
    )
    ukf.Q = np.eye(dim_x) * 0.1
    ukf.R = np.eye(dim_z) * 1.0
    return ukf


def visualize_results(true_states, measurements, estimated_states, plot: bool = False):
    if plot:
        plt.figure(figsize=(12, 6))
        plt.plot(true_states[0], label="True Position")
        plt.plot(measurements, "r.", label="Measurements")
        plt.plot(estimated_states[:, 0], "g-", label="Estimated Position")
        plt.title("Kalman Filter Tracking")
        plt.legend()
        plt.show()


# Visualize
visualize_results(true_states, measurements, estimated_states)
