# Data Analysis Agent with ScaleDown Integration

This project is an **AI-powered automated data analysis agent** that performs EDA (Exploratory Data Analysis) on a dataset, including cleaning, analysis, and insight generation. It integrates with the **ScaleDown API** for schema compression, with a **mock fallback** for offline or restricted environments.

---

## Features

- Loads and cleans data automatically (amounts, dates, etc.)
- Performs EDA:
  - Missing value analysis
  - Numerical summary (mean, std)
  - Correlation heatmap (saved to `outputs/plots/`)
- Schema compression using **ScaleDown API** (real or mock)
- Fully automated decision engine
- Automatic fallback to **mock compression** if the real API fails (network issues, invalid API key, etc.)
- Logs warnings when fallback occurs

---

## Setup

1. **Clone the repo:**

```bash
git clone <your-repo-url>
cd data-analysis-agent-scaledown
```
2. **Installation**

Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set your OpenAI API key if using the real LLM integration:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_openai_api_key"
# macOS/Linux
export OPENAI_API_KEY="your_openai_api_key"
```
3. **Usage**

Place your dataset in the data/ folder (e.g., data/sample_dataset.csv).

Run the agent script:
```bash
python app.py
```

Upload your csv file and click analyze and generate.

Numerical summaries, missing values, and top categorical columns are printed in the console.

Correlation heatmaps and other plots are saved to outputs/plots/.

ScaleDown Integration

The agent uses ScaleDown API for schema compression and prompt optimization.

If the API is unavailable or the key is invalid, a mock fallback is automatically triggered.

Warnings are logged when fallback occurs, ensuring seamless offline execution.

**Project Structure**
```bash
data-analysis-agent-scaledown/
│
├─ data/                     # Datasets (CSV files)
├─ outputs/                  # Generated plots and figures
│   └─ plots/
├─ agentsd.py                # Main data analysis agent script
├─ app.py                    # Optional Flask web interface
├─ cost.py                   # Middleware for ScaleDown API integration
├─ requirements.txt          # Python dependencies
└─ README.md
```

Features

Automated data loading and cleaning

Missing value analysis

Numerical summary (mean, std, min, max)

Correlation heatmap and basic plotting

Schema compression using ScaleDown (real API or mock)

Fully automated decision engine

API fallback and warning logging

**Future Improvements**

1. Support multiple datasets in batch mode

2. Integrate with other LLMs and prompt optimization techniques
