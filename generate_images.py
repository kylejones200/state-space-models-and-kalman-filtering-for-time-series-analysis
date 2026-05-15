#!/usr/bin/env python3
"""
Generated script to create Tufte-style visualizations
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import logging

import signalplot

logger = logging.getLogger(__name__)


from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Set random seeds

# Tufte-style configuration
signalplot.apply(font_family="serif")

images_dir = Path("images")
images_dir.mkdir(exist_ok=True)

# Update all savefig calls to use images_dir
original_savefig = plt.savefig


def savefig_tufte(filename, **kwargs):
    """Wrapper to save figures in images directory with Tufte style"""
    if not str(filename).startswith("/") and not str(filename).startswith("images/"):
        filename = images_dir / filename
    original_savefig(filename, **kwargs)
    logger.info(f"Saved: {filename}")



def main():
    plt.savefig = savefig_tufte

    # Code blocks from article

    # Code block 1

    data_path = Path("../../geospatial/datasets/use_OK.csv")


    # Code block 2
    from filterpy.kalman import KalmanFilter

    # Simple Kalman filter implementation
    kf = KalmanFilter(dim_x=2, dim_z=1)
    # State estimation and prediction


    # Code block 3
    from statsmodels.tsa.statespace.structural import UnobservedComponents

    np.random.seed(42)

    # Decompose into trend, seasonal, and irregular components
    uc_model = UnobservedComponents(
        ts_data,
        level="local level",
        seasonal=12,  # Monthly seasonality
        irregular=True,
    )
    uc_fitted = uc_model.fit()


    # Code block 4
    # Time-varying parameters
    # Regime switching
    # Hierarchical models


    # Code block 5
    # Trend extraction
    # Seasonal adjustment
    # Anomaly detection
    # Forecasting with uncertainty


    logger.info("All images generated successfully!")


if __name__ == "__main__":
    main()
