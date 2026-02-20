from flask import Flask, render_template, request, redirect
from agent.analysis_memory import AnalysisMemory
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
from dotenv import load_dotenv
import requests
import json

load_dotenv()

SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")
SCALEDOWN_MODE = os.getenv("SCALEDOWN_MODE", "mock")  # "api" or "mock"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

memory = AnalysisMemory()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):

            # Save uploaded file
            file_id = str(uuid.uuid4())
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_id + ".csv")
            file.save(filepath)

            # Load dataset
            df = pd.read_csv(filepath)
            memory.add("load_data", f"Loaded {len(df)} rows and {len(df.columns)} columns")

            # --- Dynamic plotting ---
            numeric_cols = df.select_dtypes(include='number').columns
            categorical_cols = df.select_dtypes(include='object').columns

            num_plots = len(numeric_cols) + len(categorical_cols)
            if num_plots == 0:
                # No plottable data
                plt.figure(figsize=(6,4))
                plt.text(0.5, 0.5, "No numeric or categorical columns to plot",
                         ha='center', va='center', fontsize=12)
                plt.axis('off')
            else:
                # Determine grid size
                rows = (num_plots // 2) + (num_plots % 2)
                cols = 2 if num_plots > 1 else 1
                fig, axes = plt.subplots(rows, cols, figsize=(cols*6, rows*4))
                if num_plots == 1:
                    axes = [axes]  # make iterable
                else:
                    axes = axes.flatten()

                plot_idx = 0
                # Numeric histograms
                for col in numeric_cols:
                    df[col].hist(ax=axes[plot_idx], bins=20, color='#6366f1', alpha=0.7)
                    axes[plot_idx].set_title(f"Histogram of {col}")
                    axes[plot_idx].set_xlabel(col)
                    axes[plot_idx].set_ylabel("Frequency")
                    plot_idx += 1

                # Categorical count plots
                for col in categorical_cols:
                    top_categories = df[col].value_counts().nlargest(10)
                    sns.barplot(x=top_categories.values, y=top_categories.index, ax=axes[plot_idx], palette="viridis")
                    axes[plot_idx].set_title(f"Top Categories of {col}")
                    axes[plot_idx].set_xlabel("Count")
                    axes[plot_idx].set_ylabel(col)
                    plot_idx += 1

                # Hide any unused subplots
                for i in range(plot_idx, len(axes)):
                    axes[i].axis('off')

                plt.tight_layout()

            # Save plot
            output_file = os.path.join(app.config['OUTPUT_FOLDER'], f"{file_id}.png")
            plt.savefig(output_file, bbox_inches='tight')
            plt.close()
            # --- Get ScaleDown insights ---
            insights = get_scaledown_insights(df)
            memory.add("scaledown_insights", "\n".join(insights))

            return {'png_path': '/' + output_file.replace("\\", "/"),
                    'insights': insights}

    return render_template('index.html')

def get_scaledown_insights(df: pd.DataFrame):
    """
    Sends the DataFrame to ScaleDown API (or fallback mock)
    and returns a list of AI-generated insights.
    """
    try:
        if SCALEDOWN_MODE == "mock":
            # Simple mock response
            insights = [
                f"Dataset has {len(df)} rows and {len(df.columns)} columns.",
                f"Top numeric column: {df.select_dtypes(include='number').columns[0]}" if len(df.select_dtypes(include='number')) > 0 else "No numeric columns.",
                f"Top categorical column: {df.select_dtypes(include='object').columns[0]}" if len(df.select_dtypes(include='object')) > 0 else "No categorical columns."
            ]
        else:
            # Real API call
            url = "https://api.scaledown.ai/v1/eda"  # example endpoint
            payload = df.head(1000).to_dict(orient="records")  # send only first 1000 rows
            headers = {"Authorization": f"Bearer {SCALEDOWN_API_KEY}", "Content-Type": "application/json"}
            response = requests.post(url, headers=headers, data=json.dumps({"data": payload}))
            response.raise_for_status()
            result = response.json()
            insights = result.get("insights", [])
        return insights
    except Exception as e:
        print("ScaleDown API error:", e)
        return ["ScaleDown API failed; showing local analysis only."]


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render provides PORT
    app.run(host="0.0.0.0", port=port)
