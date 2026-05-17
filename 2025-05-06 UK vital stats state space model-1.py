"""UK vital statistics state-space / structural model demo."""

from statsmodels.tsa.statespace.structural import UnobservedComponents
import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    dates = pd.date_range("2000-03-01", periods=100, freq="QS")
    births = 700 + 20 * (pd.Series(range(100)).values % 20) / 20
    marriages = 200 + 10 * (pd.Series(range(100)).values % 15) / 15
    df = pd.DataFrame({"Births": births, "Marriages": marriages}, index=dates)

    model = UnobservedComponents(df["Births"], level="local linear trend", seasonal=4)
    result = model.fit(disp=False)
    print(result.summary())

    pred = result.get_prediction()
    fig, ax = plt.subplots(figsize=(10, 4))
    df["Births"].plot(ax=ax, label="Observed", color="black")
    pred.predicted_mean.plot(ax=ax, label="Smoothed", color="steelblue")
    ax.legend()
    ax.set_title("UK births — structural state-space model")
    plt.tight_layout()
    plt.savefig("uk_births_state_space.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
