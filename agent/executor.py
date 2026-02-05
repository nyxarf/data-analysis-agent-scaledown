import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Executor:
    def __init__(self, df):
        self.df = df

    def run(self, task):
        if task == "load_data":
            # Already loaded in main.py
            return "load_data", "Data loaded into memory"

        if task == "clean_data":
            # Clean Amount column if it is string
            if "Amount" in self.df.columns:
                if self.df["Amount"].dtype == object:  # object = string
                    self.df["Amount"] = (
                         self.df["Amount"]
                        .str.replace("$", "", regex=False)
                        .str.replace(",", "", regex=False)
                        .astype(float)
                    )
                elif not pd.api.types.is_float_dtype(self.df["Amount"]):
                    # Fallback: convert to float if not string or float
                    self.df["Amount"] = pd.to_numeric(self.df["Amount"], errors="coerce")

    # Parse Date only if not already datetime
            if "Date" in self.df.columns and not pd.api.types.is_datetime64_any_dtype(self.df["Date"]):
                self.df["Date"] = pd.to_datetime(self.df["Date"], dayfirst=True)

            return "clean_data", "Amount cleaned and Date parsed (if needed)"

        if task == "analyze_data":
            # Run all EDA tasks
            insights = []

            # missing values
            numeric_df = self.df.select_dtypes(include="number")
            missing = numeric_df.isna().mean()
            top_missing = missing.sort_values(ascending=False).head(3)
            insights.append(f"Top missing ratios (numeric cols): {top_missing.to_dict()}")

            # numerical summary
            desc = numeric_df.describe().loc[["mean", "std"]]
            insights.append("Computed mean and std for numerical features")

            # correlation heatmap
            corr = numeric_df.corr()
            sns.heatmap(corr)
            plt.savefig("outputs/plots/correlation.png")
            plt.close()
            insights.append("Correlation heatmap generated at outputs/plots/correlation.png")

            # Combine all insights
            full_insight = "\n".join(insights)
            return "analyze_data", full_insight

        return None, None
