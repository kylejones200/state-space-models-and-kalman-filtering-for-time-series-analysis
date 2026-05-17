
def main() -> None:
    import ruptures as rpt
    from PIL import Image
    from linearmodels.panel import PanelOLS
    from sklearn.metrics import (
    from statsmodels.api import OLS
    from statsmodels.tools import add_constant
    from statsmodels.tsa.statespace.structural import UnobservedComponents
    import io
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns# Load and clean the datasetfile_name = "/content / Uk marriage data - unique - Sheet1.csv"
    df = pd.read_csv(file_name)# Forward - fill missing yearsdf["Year"] = df["Year"].ffill()# Map quarters to the first month of the quarterquarter_month_map = {"Mar": 3, "Jun": 6, "Sep": 9, "Dec": 12}df["Month"] = df["Quarter"].map(quarter_month_map)# Ensure Year is integerdf["Year"] = df["Year"].astype(int)# Construct datetime from Year and Monthdf["Date"] = pd.to_datetime(dict(year = df["Year"], month = df["Month"], day = 1))# Sort and set indexdf = df.sort_values("Date").set_index("Date")# Drop rows with missing datadf = df[["Births", "Marriages", "Deaths"]].dropna()# Compute 4 - quarter centered moving averagesdf["Births_Smoothed"] = df["Births"].rolling(window = 4, center = True).mean()
    df["Marriages_Smoothed"] = df["Marriages"].rolling(window = 4, center = True).mean()
    df["Deaths_Smoothed"] = df["Deaths"].rolling(window = 4, center = True).mean()# Compute demographic ratiosdf["Deaths_per_Birth"] = df["Deaths"] / df["Births"] * 1000df["Marriages_per_Birth"] = df["Marriages"] / df["Births"] * 1000df["Marriages_per_Death"] = df["Marriages"] / df["Deaths"] * 1000# Plot raw and smoothed time seriesplt.figure(figsize=(14, 6))
    plt.plot(df.index, df["Births"], label="Births", alpha = 0.3)
    plt.plot(df.index, df["Births_Smoothed"], label="Births (Smoothed)", linewidth = 2)
    plt.plot(df.index, df["Deaths"], label="Deaths", alpha = 0.3)
    plt.plot(df.index, df["Deaths_Smoothed"], label="Deaths (Smoothed)", linewidth = 2)
    plt.plot(df.index, df["Marriages"], label="Marriages", alpha = 0.3)
    plt.plot(df.index,    df["Marriages_Smoothed"],    label="Marriages (Smoothed)",    linewidth = 2)# Annotated eventsevents = {"1847 - 01 - 01": "Famine Peak","1918 - 10 - 01": "Spanish Flu","1939 - 09 - 01": "WWII Start","1945 - 05 - 01": "WWII End","1947 - 01 - 01": "Baby Boom Begins",}for date_str, label in events.items():date = pd.to_datetime(date_str)
    plt.axvline(date, color="gray", linestyle="--", alpha = 0.5)
    plt.text(date, plt.ylim()[1] * 0.9, label, rotation = 90, verticalalignment="top")
    plt.title("UK Quarterly Births, Deaths, and Marriages (1837–1983)")
    plt.xlabel("Year")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(True, linestyle="--", alpha = 0.5)
    plt.tight_layout()
    plt.show()# Plot demographic ratiosplt.figure(figsize=(14, 6))
    plt.plot(df.index, df["Deaths_per_Birth"], label="Deaths per 1000 Births")
    plt.plot(df.index, df["Marriages_per_Birth"], label="Marriages per 1000 Births")
    plt.plot(df.index, df["Marriages_per_Death"], label="Marriages per 1000 Deaths")
    plt.title("Demographic Ratios Over Time")
    plt.xlabel("Year")
    plt.ylabel("Ratio")
    plt.legend()
    plt.grid(True, linestyle="--", alpha = 0.5)
    plt.tight_layout()
    plt.show()# Optional: seasonal heatmap by decadedf["Year"] = df.index.yeardf["Quarter_Label"] = df.index.to_period("Q").strftime("%q")
    pivot_births = df.pivot_table(values="Births", index="Year", columns="Quarter_Label")
    sns.heatmap(pivot_births, cmap="YlGnBu", linewidths = 0.1)
    plt.title("Seasonality of Births by Quarter (1837–1983)")
    plt.ylabel("Year")
    plt.xlabel("Quarter")
    plt.tight_layout()
    plt.show()

    df['Deaths_per_Birth_Smoothed'] = df['Deaths_per_Birth'].rolling(window=8, center=True).mean()

    df['Marriages_per_Birth_Smoothed'] = df['Marriages_per_Birth'].rolling(window=8, center=True).mean()

    df['Marriages_per_Death_Smoothed'] = df['Marriages_per_Death'].rolling(window=8, center=True).mean()

    plt.axvspan(pd.to_datetime('1914 - 01 - 01'), pd.to_datetime('1918 - 12 - 31'), color='gray', alpha=0.2)

    plt.axvspan(pd.to_datetime('1939 - 01 - 01'), pd.to_datetime('1945 - 12 - 31'), color='gray', alpha=0.2)

    plt.yscale('log')

    plt.figure(figsize=(14, 6))

    plt.plot(df.index, df['Deaths_per_Birth_Smoothed'], label='Deaths per 1000 Births (Smoothed)')

    plt.plot(df.index, df['Marriages_per_Birth_Smoothed'], label='Marriages per 1000 Births (Smoothed)')

    plt.plot(df.index, df['Marriages_per_Death_Smoothed'], label='Marriages per 1000 Deaths (Smoothed)')

    plt.title('Demographic Ratios Over Time (Smoothed)')

    plt.xlabel('Year')

    plt.ylabel('Ratio')

    plt.legend()

    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()

    plt.show()

    df = pd.read_csv(file_name)

    df = df.sort_values('Date').set_index('Date')

    df['Marriages_Smoothed'] = df['Marriages'].rolling(window=4, center=True).mean()

    df['Deaths_Smoothed'] = df['Deaths'].rolling(window=4, center=True).mean()

    df['Marriages_per_Death_Smoothed'] = df['Marriages_Smoothed'] / df['Deaths_Smoothed'] * 1000

    breaks = model.predict(pen=10)

    plt.title('Smoothed Demographic Ratios with Structural Breaks')

    plt.xlabel('Year')

    plt.ylabel('Ratio')

    plt.legend()

    plt.tight_layout()

    plt.grid(True, linestyle='--', alpha=0.5)

    plt.show()

    df = pd.read_csv(file_name)

    df['Marriages_Smoothed'] = df['Marriages'].rolling(window=4, center=True).mean()

    df['Deaths_Smoothed'] = df['Deaths'].rolling(window=4, center=True).mean()

    df['Marriages_per_Death_Smoothed'] = df['Marriages_Smoothed'] / df['Deaths_Smoothed'] * 1000

    breaks = model.predict(pen=10)

    plt.title('Smoothed Demographic Ratios with Structural Breaks')

    plt.xlabel('Year')

    plt.ylabel('Ratio')

    plt.legend()

    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()

    plt.show()

    rolling_vol = vol_df.rolling(window=5).std()

    plt.plot(rolling_vol.index.year, rolling_vol['Births'], label='Births Volatility')

    plt.plot(rolling_vol.index.year, rolling_vol['Deaths'], label='Deaths Volatility')

    plt.plot(rolling_vol.index.year, rolling_vol['Marriages'], label='Marriages Volatility')

    plt.title('5 - Year Rolling Volatility of UK Births, Deaths, and Marriages')

    plt.xlabel('Year')

    plt.ylabel('Volatility (% change)')

    plt.legend()

    plt.tight_layout()

    plt.show()

    # Load your cleaned volatility data (already created earlier)# This assumes your DataFrame is named `df` and indexed by date# Load and clean the datasetfile_name = "/content / Uk marriage data - unique - Sheet1.csv"
    df = pd.read_csv(file_name)# Forward - fill missing yearsdf["Year"] = df["Year"].ffill()# Map quarters to the first month of the quarterquarter_month_map = {"Mar": 3, "Jun": 6, "Sep": 9, "Dec": 12}df["Month"] = df["Quarter"].map(quarter_month_map)# Ensure Year is integerdf["Year"] = df["Year"].astype(int)# Construct datetime from Year and Monthdf["Date"] = pd.to_datetime(dict(year = df["Year"], month = df["Month"], day = 1))# Sort and set indexdf = df.sort_values("Date").set_index("Date")# Drop rows with missing datadf = df[["Births", "Marriages", "Deaths"]].dropna()# First, compute year - over - year percent change and 5 - year rolling volatilitydf_yearly = df.resample("Y").sum()
    df_pct = df_yearly.pct_change() * 100
    df_vol = df_pct.rolling(window = 5).std()# Rename for claritydf_vol.columns = ["Births Volatility", "Marriages Volatility", "Deaths Volatility"]df_vol = df_vol.dropna()# Function to detect structural breaks using PELTdef detect_breaks(series, penalty = 5):algo = rpt.Pelt(model="l2").fit(series.values)
    result = algo.predict(pen = penalty)return result[:-1]  # drop the last index (end of signal)# Apply ruptures to each seriesbreaks_births = detect_breaks(df_vol["Births Volatility"], penalty = 6)
    breaks_deaths = detect_breaks(df_vol["Deaths Volatility"], penalty = 6)
    breaks_marriages = detect_breaks(df_vol["Marriages Volatility"], penalty = 6)# Plot all series with breakpointsplt.figure(figsize=(14, 6))
    plt.plot(df_vol.index, df_vol["Births Volatility"], label="Births Volatility")
    plt.plot(df_vol.index, df_vol["Deaths Volatility"], label="Deaths Volatility")
    plt.plot(df_vol.index, df_vol["Marriages Volatility"], label="Marriages Volatility")# Add breakpointsfor idx in breaks_births:plt.axvline(df_vol.index[idx], color="blue", linestyle="--", alpha = 0.3)for idx in breaks_deaths:plt.axvline(df_vol.index[idx], color="orange", linestyle="--", alpha = 0.3)for idx in breaks_marriages:plt.axvline(df_vol.index[idx], color="green", linestyle="--", alpha = 0.3)
    plt.title("5 - Year Rolling Volatility of UK Births, Deaths, and Marriages with Structural Breaks")
    plt.xlabel("Year")
    plt.ylabel("Volatility (% change)")
    plt.legend()
    plt.tight_layout()
    plt.grid(True, linestyle="--", alpha = 0.5)
    plt.show()

    # Assuming df_vol contains volatility columns with datetime indextrim_years = 10
    df_trimmed = df_vol[df_vol.index >= (df_vol.index.min() + pd.DateOffset(years = trim_years))]# Re - run rupture detection on trimmed dataalgo = rpt.Pelt(model="rbf").fit(df_trimmed["Births Volatility"].values)
    birth_breaks = algo.predict(pen = 5)
    algo = rpt.Pelt(model="rbf").fit(df_trimmed["Deaths Volatility"].values)
    death_breaks = algo.predict(pen = 5)
    algo = rpt.Pelt(model="rbf").fit(df_trimmed["Marriages Volatility"].values)
    marriage_breaks = algo.predict(pen = 5)# Plotplt.figure(figsize=(16, 6))
    plt.plot(df_trimmed.index, df_trimmed["Births Volatility"], label="Births Volatility")
    plt.plot(df_trimmed.index, df_trimmed["Deaths Volatility"], label="Deaths Volatility")
    plt.plot(df_trimmed.index, df_trimmed["Marriages Volatility"], label="Marriages Volatility")for idx in birth_breaks:if idx < len(df_trimmed):plt.axvline(df_trimmed.index[idx], color="blue", linestyle="--", alpha = 0.3)for idx in death_breaks:if idx < len(df_trimmed):plt.axvline(df_trimmed.index[idx], color="orange", linestyle="--", alpha = 0.3)for idx in marriage_breaks:if idx < len(df_trimmed):plt.axvline(df_trimmed.index[idx], color="green", linestyle="--", alpha = 0.3)
    plt.title("5 - Year Rolling Volatility of UK Births,    Deaths,    and Marriages with Structural Breaks (Trimmed)")
    plt.ylabel("Volatility (% change)")
    plt.xlabel("Year")
    plt.legend()
    plt.tight_layout()
    plt.show()

    df_vol.head()

    df = pd.read_csv(file_name)

    df['deaths_z'] = (df['Deaths'] - df['Deaths'].mean()) / df['Deaths'].std()

    df['marriages_z'] = (df['Marriages'] - df['Marriages'].mean()) / df['Marriages'].std()

    panel_data['const'] = 1

    panel_data = panel_data.set_index(['year'])

    ols_model = OLS(y, X).fit()

    print(ols_model.summary())

    df.head()

    res = mod.fit()

    print(res.summary())

    plt.tight_layout()

    plt.show()

    df = pd.read_csv(file_name)

    model_marriages = UnobservedComponents(df['Marriages'], level='local level', exog=df[['Births', 'Deaths']])

    results_marriages = model_marriages.fit(disp=False)

    fig_births.suptitle('State - Space Model for Births', fontsize=14)

    fig_marriages.suptitle('State - Space Model for Marriages', fontsize=14)

    df = pd.read_csv(file_name)

    df = df.asfreq('QE')

    results = model.fit(disp=False)

    fig.suptitle(f'State - Space Model for {title}', fontsize=16)

    mean = pred.predicted_meanci = pred.conf_int()

    axes[0].plot(series.index, series, label='Observed', color='black', linewidth=1)

    axes[0].plot(mean.index, mean, label='One - step - ahead predictions', color='steelblue')

    axes[0].fill_between(mean.index, ci.iloc[:, 0], ci.iloc[:, 1], color='steelblue', alpha=0.3)

    axes[0].legend()

    axes[0].set_title('Predicted vs observed')

    axes[1].plot(series.index, level, label='Level (smoothed)', color='steelblue')

    axes[1].fill_between(series.index, level_ci['level_smoothed_lower'], level_ci['level_smoothed_upper'], color='steelblue', alpha=0.3)

    axes[1].set_title('Level component')

    axes[1].legend()

    plt.tight_layout()

    plt.subplots_adjust(top=0.9)

    plt.show()

    run_ucm('Deaths', 'Deaths')

    run_ucm('Marriages', 'Marriages')

    def run_ucm(df, series_name, title):series = df[series_name]# Fit the local level modelmodel = UnobservedComponents(series, level="local level")
    results = model.fit(disp = False)# Plot predicted vs observedfig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex = True)
    fig.suptitle(f"State - Space Model for {title}", fontsize = 16)# One - step - ahead predictionspred = results.get_prediction()
    mean = pred.predicted_meanci = pred.conf_int()
    axes[0].plot(series.index, series, label="Observed", color="black", linewidth = 1)
    axes[0].plot(mean.index, mean, label="One - step - ahead predictions", color="steelblue")
    axes[0].fill_between(mean.index, ci.iloc[:, 0], ci.iloc[:, 1], color="steelblue", alpha = 0.3)
    axes[0].legend()
    axes[0].set_title("Predicted vs observed")# Smoothed levellevel = results.level_smoothedlevel_ci = results.get_smoothed_conf_int(alpha = 0.05)
    axes[1].plot(series.index, level, label="Level (smoothed)", color="steelblue")
    axes[1].fill_between(series.index,level_ci["level_smoothed_lower"],level_ci["level_smoothed_upper"],color="steelblue",alpha = 0.3,)
    axes[1].set_title("Level component")
    axes[1].legend()
    plt.tight_layout()
    plt.subplots_adjust(top = 0.90)
    plt.savefig(f"statespace_{series_name.lower()}.png")
    plt.show()mean_absolute_error,mean_squared_error,mean_absolute_percentage_error,)# Drop any NaNs before calculating metricsobserved = series.loc[mean.index].dropna()
    predicted = mean.loc[observed.index].dropna()# Align lengthsobserved, predicted = observed.align(predicted, join="inner")# Compute metricsmae = mean_absolute_error(observed, predicted)
    mse = mean_squared_error(observed, predicted)
    rmse = np.sqrt(mse)
    mape = mean_absolute_percentage_error(observed, predicted)
    print(f"\nError Metrics for {title}:")
    print(f"
      MAE  = {mae:,.0f}")
    print(f"
      RMSE = {rmse:,.0f}")
    print(f"
      MAPE = {mape:.2%}")# Example usage:# df = pd.read_csv('your_data.csv', parse_dates=['Date'], index_col='Date')# df = df.asfreq('Q')# run_ucm(df, 'Births', 'Births')# run_ucm(df, 'Deaths', 'Deaths')# run_ucm(df, 'Marriages', 'Marriages')

    mean_absolute_error,mean_squared_error,mean_absolute_percentage_error,)def run_ucm(df, series_name, title):series = df[series_name].dropna()
    model = UnobservedComponents(series, level="local level")
    results = model.fit(disp = False)# One - step - ahead predictionspred = results.get_prediction()
    mean = pred.predicted_meanci = pred.conf_int()fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex = True)
    fig.suptitle(f"State - Space Model for {title}", fontsize = 16)# Plot observed vs predictedaxes[0].plot(series.index, series, label="Observed", color="black", linewidth = 1)
    axes[0].plot(mean.index, mean, label="One - step - ahead predictions", color="steelblue")
    axes[0].fill_between(mean.index, ci.iloc[:, 0], ci.iloc[:, 1], color="steelblue", alpha = 0.3)
    axes[0].legend()
    axes[0].set_title("Predicted vs observed")# Extract smoothed level from results.smoothed_statesmoothed_level = results.smoothed_state[0]  # Index 0 is level componentsmoothed_index = series.index# Smoothed level confidence intervalslevel_var = results.smoothed_state_cov[0, 0, :]  # variance of levellevel_std = np.sqrt(level_var)
    lower = smoothed_level - 1.96 * level_stdupper = smoothed_level + 1.96 * level_stdaxes[1].plot(smoothed_index, smoothed_level, label="Level (smoothed)", color="steelblue")
    axes[1].fill_between(smoothed_index, lower, upper, color="steelblue", alpha = 0.3)
    axes[1].set_title("Level component")
    axes[1].legend()
    plt.tight_layout()
    plt.subplots_adjust(top = 0.90)
    plt.savefig(f"statespace_{series_name.lower()}.png")
    plt.show()# Error metricsobserved = series.loc[mean.index].dropna()
    predicted = mean.loc[observed.index].dropna()observed, predicted = observed.align(predicted, join="inner")
    mae = mean_absolute_error(observed, predicted)
    rmse = np.sqrt(mean_squared_error(observed, predicted))
    mape = mean_absolute_percentage_error(observed, predicted)
    print(f"\nError Metrics for {title}:")
    print(f"
      MAE  = {mae:,.0f}")
    print(f"
      RMSE = {rmse:,.0f}")
    print(f"
      MAPE = {mape:.2%}")
    run_ucm(df, "Births", "Births")

    def run_ucm(df, series_name, title):# Ensure datetime indexif not isinstance(df.index, pd.DatetimeIndex):raise ValueError("The DataFrame index must be a DatetimeIndex.")# Ensure quarterly frequencydf = df.asfreq("Q")# Clean the series: drop NaNs and ensure it's floatseries = df[series_name].copy()
    series = pd.to_numeric(series, errors="coerce")  # force conversionseries = series.fillna(method="ffill").fillna(method="bfill")  # handle NaNsif series.isnull().any() or len(series) < 10:raise ValueError(f"{series_name} still has missing or insufficient data after cleaning.")# Fit the state - space modelmodel = UnobservedComponents(series, level="local level")
    results = model.fit(disp = False)# One - step - ahead predictionspred = results.get_prediction()
    mean = pred.predicted_meanci = pred.conf_int()# Smoothed levellevel = results.level_smoothedlevel_ci = results.get_smoothed_conf_int(alpha = 0.05)# Plotfig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex = True)
    fig.suptitle(f"State - Space Model for {title}", fontsize = 16)# Observed vs predictedaxes[0].plot(series.index, series, label="Observed", color="black", linewidth = 1)
    axes[0].plot(mean.index, mean, label="One - step prediction", color="blue")
    axes[0].fill_between(mean.index, ci.iloc[:, 0], ci.iloc[:, 1], color="blue", alpha = 0.3)
    axes[0].legend()
    axes[0].set_title("Observed vs Predicted")# Level componentaxes[1].plot(series.index, level, label="Smoothed Level", color="blue")
    axes[1].fill_between(series.index,level_ci["level_smoothed_lower"],level_ci["level_smoothed_upper"],color="blue",alpha = 0.3,)
    axes[1].legend()
    axes[1].set_title("Smoothed Level Component")
    plt.tight_layout()
    plt.subplots_adjust(top = 0.9)
    plt.savefig(f"statespace_{series_name.lower()}.png")
    plt.show()mean_absolute_error,mean_squared_error,mean_absolute_percentage_error,)# Drop any NaNs before calculating metricsobserved = series.loc[mean.index].dropna()
    predicted = mean.loc[observed.index].dropna()# Align lengthsobserved, predicted = observed.align(predicted, join="inner")# Compute metricsmae = mean_absolute_error(observed, predicted)
    mse = mean_squared_error(observed, predicted)
    rmse = np.sqrt(mse)
    mape = mean_absolute_percentage_error(observed, predicted)
    print(f"\nError Metrics for {title}:")
    print(f"
      MAE  = {mae:,.0f}")
    print(f"
      RMSE = {rmse:,.0f}")
    print(f"
      MAPE = {mape:.2%}")

    df = pd.read_csv(file_name)

    df.to_csv('Uk vital statistics data cleaned_data.csv')

    mean_absolute_error,mean_squared_error,mean_absolute_percentage_error,)def run_ucm(df, series_name, title):series = df[series_name].dropna()
    model = UnobservedComponents(series, level="local level")
    results = model.fit(disp = False)# One - step - ahead predictionspred = results.get_prediction()
    mean = pred.predicted_meanci = pred.conf_int()fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex = True)
    fig.suptitle(f"State - Space Model for {title}", fontsize = 16)# Plot observed vs predictedaxes[0].plot(series.index, series, label="Observed", color="black", linewidth = 1)
    axes[0].plot(mean.index, mean, label="One - step - ahead predictions", color="steelblue")
    axes[0].fill_between(mean.index, ci.iloc[:, 0], ci.iloc[:, 1], color="steelblue", alpha = 0.3)
    axes[0].legend()
    axes[0].set_title("Predicted vs observed")# Extract smoothed level from results.smoothed_statesmoothed_level = results.smoothed_state[0]  # Index 0 is level componentsmoothed_index = series.index# Smoothed level confidence intervalslevel_var = results.smoothed_state_cov[0, 0, :]  # variance of levellevel_std = np.sqrt(level_var)
    lower = smoothed_level - 1.96 * level_stdupper = smoothed_level + 1.96 * level_stdaxes[1].plot(smoothed_index, smoothed_level, label="Level (smoothed)", color="steelblue")
    axes[1].fill_between(smoothed_index, lower, upper, color="steelblue", alpha = 0.3)
    axes[1].set_title("Level component")
    axes[1].legend()
    plt.tight_layout()
    plt.subplots_adjust(top = 0.90)
    plt.savefig(f"statespace_{series_name.lower()}.png")
    plt.show()# Error metricsobserved = series.loc[mean.index].dropna()
    predicted = mean.loc[observed.index].dropna()observed, predicted = observed.align(predicted, join="inner")
    mae = mean_absolute_error(observed, predicted)
    rmse = np.sqrt(mean_squared_error(observed, predicted))
    mape = mean_absolute_percentage_error(observed, predicted)
    print(f"\nError Metrics for {title}:")
    print(f"
      MAE  = {mae:,.0f}")
    print(f"
      RMSE = {rmse:,.0f}")
    print(f"
      MAPE = {mape:.2%}")
    url = "https://raw.githubusercontent.com / kylejones200 / time_series / refs / heads / main / Uk%20vital%20statistics%20data%20cleaned_data.csv"
    df = pd.read_csv(url)
    run_ucm(df, "Births", "Births")

    mean_absolute_error,mean_squared_error,mean_absolute_percentage_error,)def run_ucm_with_gif(df, series_name, title):series = df[series_name].dropna()
    model = UnobservedComponents(series, level="local level")
    results = model.fit(disp = False)
    pred = results.get_prediction()
    mean = pred.predicted_meanci = pred.conf_int()
    smoothed_level = results.smoothed_state[0]smoothed_index = series.indexlevel_var = results.smoothed_state_cov[0, 0, :]level_std = np.sqrt(level_var)
    lower = smoothed_level - 1.96 * level_stdupper = smoothed_level + 1.96 * level_stdframes = []for i in range(10, len(series)):fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex = True)
    fig.suptitle(f"State - Space Model for {title}", fontsize = 16)# Observed vs predicted up to index iaxes[0].plot(series.index[:i],series.values[:i],label="Observed",color="black",linewidth = 1,)
    axes[0].plot(mean.index[:i], mean.values[:i], label="Prediction", color="steelblue")
    axes[0].fill_between(mean.index[:i], ci.iloc[:i, 0], ci.iloc[:i, 1], color="steelblue", alpha = 0.3)
    axes[0].legend()
    axes[0].set_title("Predicted vs observed")# Smoothed level up to index iaxes[1].plot(smoothed_index[:i],smoothed_level[:i],label="Level (smoothed)",color="steelblue",)
    axes[1].fill_between(smoothed_index[:i], lower[:i], upper[:i], color="steelblue", alpha = 0.3)
    axes[1].set_title("Level component")
    axes[1].legend()
    plt.tight_layout()
    plt.subplots_adjust(top = 0.90)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image = Image.open(buf)
    frames.append(image.convert("RGB"))
    plt.close()
    frames[0].save(f"statespace_{series_name.lower()}.gif",format="GIF",save_all = True,append_images = frames[1:],duration = 150,loop = 0,)# Print error metricsobserved = series.loc[mean.index].dropna()
    predicted = mean.loc[observed.index].dropna()observed, predicted = observed.align(predicted, join="inner")
    mae = mean_absolute_error(observed, predicted)
    rmse = np.sqrt(mean_squared_error(observed, predicted))
    mape = mean_absolute_percentage_error(observed, predicted)
    print(f"\nError Metrics for {title}:")
    print(f"
      MAE  = {mae:,.0f}")
    print(f"
      RMSE = {rmse:,.0f}")
    print(f"
      MAPE = {mape:.2%}")# Load dataurl = "https://raw.githubusercontent.com / kylejones200 / time_series / refs / heads / main / Uk%20vital%20statistics%20data%20cleaned_data.csv"
    df = pd.read_csv(url, parse_dates=["Date"], index_col="Date")# Runrun_ucm_with_gif(df, "Births", "Births")

if __name__ == "__main__":
    main()
