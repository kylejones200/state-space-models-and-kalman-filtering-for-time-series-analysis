# State Space Models and Kalman Filtering for Time Series

This project demonstrates state space models and Kalman filtering for time series analysis.

## Business context

Most time series models work directly with observed values. State space models take a different approach: they assume there is an underlying hidden state — a true signal — and that what you observe is that signal corrupted by noise. The model estimates the hidden state at each point in time, filtering out the noise.

The Kalman filter is the algorithm that does this estimation for linear systems. It is the engine behind GPS navigation, spacecraft guidance, financial smoothing models, and econometric decompositions. Understanding it gives you a fundamentally different way to think about time series.

## Project Structure

```
.
├── README.md           # This file
├── main.py            # Main entry point
├── config.yaml        # Configuration file
├── requirements.txt   # Python dependencies
├── src/               # Core functions
│   ├── core.py        # Kalman filter functions
│   └── plotting.py    # Tufte-style plotting utilities
├── tests/             # Unit tests
├── data/              # Data files
└── images/            # Generated plots and figures
```

## Configuration

Edit `config.yaml` to customize model parameters and output settings.

## Kalman Filter

The Kalman filter:
- Estimates hidden states from noisy observations
- Recursively updates state estimates
- Provides optimal filtering under Gaussian assumptions

## Disclaimer

Educational/demo code only. Not financial, safety, or engineering advice. Use at your own risk. Verify results independently before any production or operational use.

## License

MIT — see [LICENSE](LICENSE).