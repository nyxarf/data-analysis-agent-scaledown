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
