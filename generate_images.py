"""
Generated script to create Tufte-style visualizations
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from filterpy.kalman import KalmanFilter
from statsmodels.tsa.statespace.structural import UnobservedComponents


def savefig_tufte(filename, **kwargs):
    """Wrapper to save figures in images directory with Tufte style"""
    if not str(filename).startswith("/") and (not str(filename).startswith("images/")):
        filename = images_dir / filename
    original_savefig(filename, **kwargs)
    logger.info(f"Saved: {filename}")


def main() -> None:
    plt.savefig = savefig_tufte

    data_path = Path("../../geospatial/datasets/use_OK.csv")

    kf = KalmanFilter(dim_x=2, dim_z=1)

    np.random.seed(42)

    uc_model = UnobservedComponents(
        ts_data, level="local level", seasonal=12, irregular=True
    )

    uc_fitted = uc_model.fit()

    logger.info("All images generated successfully!")


if __name__ == "__main__":
    main()
