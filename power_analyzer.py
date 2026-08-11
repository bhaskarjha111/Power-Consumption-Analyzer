import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# POWER CONSUMPTION ANALYZER
# Author: Bhaskar Jha
# Project: LTspice Power Consumption Analysis using Python
# ============================================================

# -----------------------------
# Folder Configuration
# -----------------------------

INPUT_FOLDER = "ltspice_outputs"
OUTPUT_FOLDER = "output_reports"

os.makedirs(INPUT_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# -----------------------------
# Sample Data Generator
# -----------------------------
# This function creates sample LTspice-like output files.
# Once you have real LTspice CSV files, you can replace these files.

def generate_sample_ltspice_data():
    """
    Generates sample LTspice-style CSV files for testing the analyzer.
    You can replace these files with real exported LTspice data later.
    """

    # Frequency vs Power data
    frequency = np.array([1e3, 5e3, 10e3, 50e3, 100e3, 500e3, 1e6, 5e6, 10e6])
    static_power = np.full(len(frequency), 0.002)      # 2 mW static power
    dynamic_power = 1e-12 * frequency * 1.8**2 * 1e3   # simplified dynamic power model
    total_power = static_power + dynamic_power

    freq_df = pd.DataFrame({
        "Frequency_Hz": frequency,
        "Static_Power_W": static_power,
        "Dynamic_Power_W": dynamic_power,
        "Total_Power_W": total_power
    })

    freq_df.to_csv(os.path.join(INPUT_FOLDER, "frequency_power.csv"), index=False)

    # Static vs Dynamic power data
    breakdown_df = pd.DataFrame({
        "Power_Type": ["Static Power", "Dynamic Power"],
        "Power_W": [static_power.mean(), dynamic_power.mean()]
    })

    breakdown_df.to_csv(os.path.join(INPUT_FOLDER, "static_dynamic_power.csv"), index=False)

    # Temperature vs Power data
    temperature = np.array([-40, -20, 0, 25, 50, 75, 100, 125])
    leakage_power = 0.0015 * np.exp((temperature - 25) / 80)
    switching_power = np.full(len(temperature), 0.003)
    total_temp_power = leakage_power + switching_power

    temp_df = pd.DataFrame({
        "Temperature_C": temperature,
        "Static_Power_W": leakage_power,
        "Dynamic_Power_W": switching_power,
        "Total_Power_W": total_temp_power
    })

    temp_df.to_csv(os.path.join(INPUT_FOLDER, "temperature_power.csv"), index=False)

    print("Sample LTspice-like CSV files generated successfully.")


# -----------------------------
# Data Loading Functions
# -----------------------------

def load_csv_file(filename):
    """
    Loads a CSV file from the LTspice output folder.
    """
    file_path = os.path.join(INPUT_FOLDER, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{filename} not found in {INPUT_FOLDER} folder.")

    data = pd.read_csv(file_path)
    return data


# -----------------------------
# Power vs Frequency Plot
# -----------------------------

def plot_power_vs_frequency(freq_df):
    """
    Plots power consumption with respect to frequency.
    """

    plt.figure(figsize=(10, 6))

    plt.plot(
        freq_df["Frequency_Hz"],
        freq_df["Total_Power_W"] * 1000,
        marker="o",
        linewidth=2,
        label="Total Power"
    )

    plt.plot(
        freq_df["Frequency_Hz"],
        freq_df["Dynamic_Power_W"] * 1000,
        marker="s",
        linestyle="--",
        linewidth=2,
        label="Dynamic Power"
    )

    plt.plot(
        freq_df["Frequency_Hz"],
        freq_df["Static_Power_W"] * 1000,
        marker="^",
        linestyle=":",
        linewidth=2,
        label="Static Power"
    )

    plt.xscale("log")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Consumption (mW)")
    plt.title("Power Consumption vs Frequency")
    plt.grid(True, which="both", linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_FOLDER, "power_vs_frequency.png")
    plt.savefig(output_path, dpi=300)
    plt.show()

    print(f"Power vs Frequency graph saved at: {output_path}")


# -----------------------------
# Static vs Dynamic Power Pie Chart
# -----------------------------

def plot_power_breakdown_pie(breakdown_df):
    """
    Plots static vs dynamic power breakdown.
    """

    plt.figure(figsize=(8, 8))

    plt.pie(
        breakdown_df["Power_W"],
        labels=breakdown_df["Power_Type"],
        autopct="%1.1f%%",
        startangle=90,
        shadow=True
    )

    plt.title("Static vs Dynamic Power Breakdown")
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_FOLDER, "power_breakdown_pie.png")
    plt.savefig(output_path, dpi=300)
    plt.show()

    print(f"Power breakdown pie chart saved at: {output_path}")


# -----------------------------
# Temperature Effect Plot
# -----------------------------

def plot_temperature_effect(temp_df):
    """
    Plots power consumption variation with temperature.
    """

    plt.figure(figsize=(10, 6))

    plt.plot(
        temp_df["Temperature_C"],
        temp_df["Total_Power_W"] * 1000,
        marker="o",
        linewidth=2,
        label="Total Power"
    )

    plt.plot(
        temp_df["Temperature_C"],
        temp_df["Static_Power_W"] * 1000,
        marker="s",
        linestyle="--",
        linewidth=2,
        label="Static Power"
    )

    plt.plot(
        temp_df["Temperature_C"],
        temp_df["Dynamic_Power_W"] * 1000,
        marker="^",
        linestyle=":",
        linewidth=2,
        label="Dynamic Power"
    )

    plt.xlabel("Temperature (°C)")
    plt.ylabel("Power Consumption (mW)")
    plt.title("Temperature Effect on Power Consumption")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()

    output_path = os.path.join(OUTPUT_FOLDER, "temperature_effect.png")
    plt.savefig(output_path, dpi=300)
    plt.show()

    print(f"Temperature effect graph saved at: {output_path}")


# -----------------------------
# Automated Power Report
# -----------------------------

def generate_power_report(freq_df, breakdown_df, temp_df):
    """
    Generates an automated text report based on power analysis.
    """

    max_power = freq_df["Total_Power_W"].max()
    min_power = freq_df["Total_Power_W"].min()
    avg_power = freq_df["Total_Power_W"].mean()

    max_power_freq = freq_df.loc[freq_df["Total_Power_W"].idxmax(), "Frequency_Hz"]
    min_power_freq = freq_df.loc[freq_df["Total_Power_W"].idxmin(), "Frequency_Hz"]

    static_power_avg = freq_df["Static_Power_W"].mean()
    dynamic_power_avg = freq_df["Dynamic_Power_W"].mean()

    static_percentage = (static_power_avg / avg_power) * 100
    dynamic_percentage = (dynamic_power_avg / avg_power) * 100

    max_temp_power = temp_df["Total_Power_W"].max()
    min_temp_power = temp_df["Total_Power_W"].min()

    max_temp = temp_df.loc[temp_df["Total_Power_W"].idxmax(), "Temperature_C"]
    min_temp = temp_df.loc[temp_df["Total_Power_W"].idxmin(), "Temperature_C"]

    report = f"""
============================================================
                AUTOMATED POWER ANALYSIS REPORT
============================================================

Project Name:
Power Consumption Analyzer using Python and LTspice Output Files

Objective:
To analyze power consumption behavior of a simulated electronic circuit
using LTspice output data and Python-based visualization.

------------------------------------------------------------
1. POWER VS FREQUENCY ANALYSIS
------------------------------------------------------------

Minimum Total Power:
{min_power * 1000:.4f} mW at {min_power_freq:.2f} Hz

Maximum Total Power:
{max_power * 1000:.4f} mW at {max_power_freq:.2f} Hz

Average Total Power:
{avg_power * 1000:.4f} mW

Observation:
As operating frequency increases, dynamic power also increases.
This is because dynamic power is directly proportional to switching
activity and frequency.

Formula:
Dynamic Power = α × C × V² × f

Where:
α = switching activity factor
C = load capacitance
V = supply voltage
f = operating frequency

------------------------------------------------------------
2. STATIC VS DYNAMIC POWER BREAKDOWN
------------------------------------------------------------

Average Static Power:
{static_power_avg * 1000:.4f} mW

Average Dynamic Power:
{dynamic_power_avg * 1000:.4f} mW

Static Power Percentage:
{static_percentage:.2f} %

Dynamic Power Percentage:
{dynamic_percentage:.2f} %

Observation:
Static power mainly comes from leakage current, while dynamic power
comes from charging and discharging of capacitances during switching.

------------------------------------------------------------
3. TEMPERATURE EFFECT ON POWER
------------------------------------------------------------

Minimum Power with Temperature:
{min_temp_power * 1000:.4f} mW at {min_temp:.2f} °C

Maximum Power with Temperature:
{max_temp_power * 1000:.4f} mW at {max_temp:.2f} °C

Observation:
Power consumption increases with temperature mainly because leakage
current increases at higher temperatures. This is an important factor
in VLSI circuit design and low-power semiconductor systems.

------------------------------------------------------------
4. ENGINEERING INSIGHTS
------------------------------------------------------------

1. Dynamic power dominates at high operating frequencies.
2. Static power becomes significant at higher temperatures.
3. Low-power design requires reducing voltage, capacitance, switching
   activity, and leakage current.
4. The circuit should be tested across frequency and temperature corners.
5. This type of analysis is useful in VLSI, CMOS design, embedded systems,
   and semiconductor power optimization.

------------------------------------------------------------
5. GENERATED OUTPUT FILES
------------------------------------------------------------

1. power_vs_frequency.png
2. power_breakdown_pie.png
3. temperature_effect.png
4. automated_power_report.txt

============================================================
End of Report
============================================================
"""

    output_path = os.path.join(OUTPUT_FOLDER, "automated_power_report.txt")

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"Automated power report generated at: {output_path}")


# -----------------------------
# Advanced Summary Table
# -----------------------------

def generate_summary_table(freq_df, temp_df):
    """
    Generates a clean summary CSV table for resume/project documentation.
    """

    summary_data = {
        "Metric": [
            "Minimum Frequency Power",
            "Maximum Frequency Power",
            "Average Frequency Power",
            "Minimum Temperature Power",
            "Maximum Temperature Power",
            "Average Temperature Power"
        ],
        "Value_mW": [
            freq_df["Total_Power_W"].min() * 1000,
            freq_df["Total_Power_W"].max() * 1000,
            freq_df["Total_Power_W"].mean() * 1000,
            temp_df["Total_Power_W"].min() * 1000,
            temp_df["Total_Power_W"].max() * 1000,
            temp_df["Total_Power_W"].mean() * 1000
        ]
    }

    summary_df = pd.DataFrame(summary_data)

    output_path = os.path.join(OUTPUT_FOLDER, "summary_table.csv")
    summary_df.to_csv(output_path, index=False)

    print(f"Summary table saved at: {output_path}")


# -----------------------------
# Main Function
# -----------------------------

def main():
    print("============================================================")
    print("POWER CONSUMPTION ANALYZER")
    print("Python + Pandas + Matplotlib + LTspice Output Files")
    print("============================================================")

    # Step 1: Generate sample data
    # Comment this line when using real LTspice CSV files.
    generate_sample_ltspice_data()

    # Step 2: Load CSV data
    freq_df = load_csv_file("frequency_power.csv")
    breakdown_df = load_csv_file("static_dynamic_power.csv")
    temp_df = load_csv_file("temperature_power.csv")

    # Step 3: Display loaded data
    print("\nFrequency Power Data:")
    print(freq_df)

    print("\nStatic vs Dynamic Power Data:")
    print(breakdown_df)

    print("\nTemperature Power Data:")
    print(temp_df)

    # Step 4: Generate graphs
    plot_power_vs_frequency(freq_df)
    plot_power_breakdown_pie(breakdown_df)
    plot_temperature_effect(temp_df)

    # Step 5: Generate report
    generate_power_report(freq_df, breakdown_df, temp_df)

    # Step 6: Generate summary table
    generate_summary_table(freq_df, temp_df)

    print("\nAnalysis completed successfully.")
    print(f"Check the '{OUTPUT_FOLDER}' folder for graphs and report.")


# -----------------------------
# Program Execution
# -----------------------------

if __name__ == "__main__":
    main()
