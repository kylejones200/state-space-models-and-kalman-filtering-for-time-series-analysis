"""
State space modeling and Kalman filtering on Oklahoma energy consumption.

This script fits a structural time series model to annual Oklahoma energy
consumption using statsmodels' state space framework, then:

- Decomposes the series into trend and irregular components
- Visualizes filtered vs. smoothed trend estimates
- Produces a multi-step forecast with uncertainty intervals

All plots are saved as PNGs so they can be used directly in articles.
"""

from __future__ import annotations

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.statespace.structural import UnobservedComponents


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "use_OK.csv"


def load_energy_series(csv_path: Path) -> pd.Series:
    """Load and aggregate Oklahoma energy consumption into an annual series."""
    logger.info("Loading energy data from %s", csv_path)
    df = pd.read_csv(csv_path)

    year_cols = [col for col in df.columns if col.isdigit()]
    if not year_cols:
        raise ValueError("No year columns found in energy consumption file.")

    year_totals = df[year_cols].apply(pd.to_numeric, errors="coerce").sum(axis=0)
    ts = pd.Series(
        data=year_totals.values,
        index=pd.to_datetime(year_totals.index, format="%Y"),
    ).sort_index()

    logger.info(
        "Time series length: %d (from %s to %s)",
        len(ts),
        ts.index.min().date(),
        ts.index.max().date(),
    )
    logger.info("Value range: %.2f to %.2f", ts.min(), ts.max())
    return ts


def fit_structural_model(ts: pd.Series):
    """Fit a local linear trend state space model to the series."""
    logger.info("Fitting local linear trend structural model...")
    model = UnobservedComponents(
        ts,
        level="local linear trend",
        irregular=True,
        seasonal=None,
    )
    results = model.fit(disp=False)
    logger.info("Model fitted. AIC=%.2f, BIC=%.2f", results.aic, results.bic)
    return results


def plot_decomposition(ts: pd.Series, results, plot: bool = False) -> None:
    """Plot observed data and smoothed trend component."""
    logger.info("Plotting Kalman-smoothed trend decomposition...")

    if plot:
        fig, ax = plt.subplots(figsize=(14, 6))
        plt.rcParams.update(
            {
                "font.family": "serif",
                "axes.spines.top": False,
                "axes.spines.right": False,
                "axes.grid": False,
            }
        )

    # Observed series
        ax.plot(ts.index, ts.values, "k-", label="Observed", alpha=0.7, linewidth=1.8)

    # Smoothed level (trend) component
        smoothed = results.level.smoothed
        ax.plot(
            ts.index,
            smoothed,
            color="#1f77b4",
            linewidth=2.2,
            label="Kalman-smoothed level",
        )

        ax.set_title(
            "Kalman Filter Decomposition: Observed vs. Smoothed Trend",
            fontsize=14,
            fontweight="bold",
        )
        ax.set_ylabel("Energy Consumption", fontsize=11)
        ax.legend(frameon=True, fancybox=True, shadow=True, fontsize=10)
        plt.tight_layout()
        output_path = BASE_DIR / "kalman_decomposition.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        logger.info("Saved decomposition plot to %s", output_path)
        plt.close(fig)


def plot_forecast(ts: pd.Series, results, horizon: int = 10, plot: bool = False) -> None:
    """Produce and plot a multi-step forecast with confidence intervals."""
    logger.info("Producing %d-step Kalman forecast...", horizon)
    forecast_res = results.get_forecast(steps=horizon)
    mean_forecast = forecast_res.predicted_mean
    conf_int = forecast_res.conf_int(alpha=0.05)

    forecast_index = pd.date_range(
        start=ts.index[-1] + pd.DateOffset(years=1),
        periods=horizon,
        freq="YS",
    )

    if plot:
        fig, ax = plt.subplots(figsize=(14, 6))
        plt.rcParams.update(
            {
                "font.family": "serif",
                "axes.spines.top": False,
                "axes.spines.right": False,
                "axes.grid": False,
            }
        )

    # Plot last 20 years of history for context
        history_window = min(20, len(ts))
        ax.plot(
            ts.index[-history_window:],
            ts.values[-history_window:],
            "k-",
            label="Historical",
            linewidth=2,
            alpha=0.7,
        )

    # Plot forecast and 95% interval
        ax.plot(
            forecast_index,
            mean_forecast.values,
            "b--",
            label="Kalman Forecast",
            linewidth=2,
            marker="o",
        )
        lower = conf_int.iloc[:, 0].values
        upper = conf_int.iloc[:, 1].values
    # Energy consumption cannot be negative; clip lower band at zero for visualization
        lower_clipped = lower.clip(min=0.0)

        ax.fill_between(
            forecast_index,
            lower_clipped,
            upper,
            color="#1f77b4",
            alpha=0.2,
            label="95% Interval",
        )

        ax.axvline(ts.index[-1], color="gray", linestyle=":", linewidth=1, alpha=0.6)
        ax.set_title(
            "Kalman Filter Forecast with Uncertainty",
            fontsize=14,
            fontweight="bold",
        )
        ax.set_ylabel("Energy Consumption", fontsize=11)
        ax.legend(frameon=False, fancybox=False, shadow=False, fontsize=10)
        plt.tight_layout()
        output_path = BASE_DIR / "kalman_forecast.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        logger.info("Saved forecast plot to %s", output_path)
        plt.close(fig)


def main() -> None:
    """Run the full Kalman-based analysis on Oklahoma energy data."""
    ts = load_energy_series(DATA_PATH)
    results = fit_structural_model(ts)

    logger.info("Model summary (truncated):\n%s", results.summary().as_text()[:800])

    plot_decomposition(ts, results)
    # Use a modest forecast horizon for annual data to avoid unrealistically wide bands
    plot_forecast(ts, results, horizon=5)


if __name__ == "__main__":
    main()


