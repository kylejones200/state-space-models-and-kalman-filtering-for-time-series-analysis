#!/usr/bin/env python3
"""
Generated script to create Tufte-style visualizations
"""
import logging

logger = logging.getLogger(__name__)


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Set random seeds
np.random.seed(42)
try:
    import tensorflow as tf
    tf.random.set_seed(42)
except ImportError:
    tf = None
except Exception:
    pass

# Tufte-style configuration
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Palatino', 'Times New Roman', 'Times'],
    'font.size': 11,
    'axes.labelsize': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'normal',
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.linewidth': 0.5,
    'axes.edgecolor': '#333333',
    'axes.labelcolor': '#333333',
    'xtick.color': '#333333',
    'ytick.color': '#333333',
    'text.color': '#333333',
    'axes.grid': False,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

images_dir = Path("images")
images_dir.mkdir(exist_ok=True)

# Update all savefig calls to use images_dir
import matplotlib.pyplot as plt
original_savefig = plt.savefig

def savefig_tufte(filename, **kwargs):
    """Wrapper to save figures in images directory with Tufte style"""
    if not str(filename).startswith('/') and not str(filename).startswith('images/'):
        filename = images_dir / filename
    original_savefig(filename, **kwargs)
    logger.info(f"Saved: {filename}")

plt.savefig = savefig_tufte

# Code blocks from article

# Code block 1
import pandas as pd
from pathlib import Path

data_path = Path("../../geospatial/datasets/use_OK.csv")



# Code block 2
from filterpy.kalman import KalmanFilter

# Simple Kalman filter implementation
kf = KalmanFilter(dim_x=2, dim_z=1)
# State estimation and prediction



# Code block 3
from statsmodels.tsa.statespace.structural import UnobservedComponents

# Decompose into trend, seasonal, and irregular components
uc_model = UnobservedComponents(
    ts_data,
    level='local level',
    seasonal=12,  # Monthly seasonality
    irregular=True
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
