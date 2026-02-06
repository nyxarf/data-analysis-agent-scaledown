# agent.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openai
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from scaledown import PromptOptimizer

# ===============================
# 1️⃣ Load your dataset
# ===============================
data = pd.read_csv("your_dataset.csv")  # Replace with your CSV path
print("Dataset loaded successfully!")

# ===============================
# 2️⃣ Define helper functions for the agent
# ===============================

# Function to summarize dataset
def summarize_data():
    return data.describe(include="all").to_string()

# Function to show missing values
def missing_values():
    return data.isna().sum().to_string()

# Function to plot distributions
def plot_distributions():
    numeric_cols = data.select_dtypes(include="number").columns
    for col in numeric_cols:
        plt.figure(figsize=(6,4))
        sns.histplot(data[col], kde=True)
        plt.title(f'Distribution of {col}')
        plt.savefig(f"{col}_distribution.png")
        plt.close()
    return f"Saved distribution plots for numeric columns: {', '.join(numeric_cols)}"

# Function to plot correlations
def plot_correlation():
    corr = data.corr()
    plt.figure(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation Matrix")
    plt.savefig("correlation_matrix.png")
    plt.close()
    return "Saved correlation matrix as 'correlation_matrix.png'"

# ===============================
# 3️⃣ Optimize prompt with Scaledown
# ===============================
optimizer = PromptOptimizer()

base_task = """
You are a data analysis assistant. 
Analyze the dataset provided and give insights including:
- Summary statistics
- Missing values
- Basic plots for distributions and correlations
"""
optimized_task = optimizer.optimize(base_task)

# ===============================
# 4️⃣ Define tools for the agent
# ===============================
tools = [
    Tool(name="Summarize Data", func=summarize_data, description="Returns summary statistics of the dataset"),
    Tool(name="Missing Values", func=missing_values, description="Returns count of missing values for each column"),
    Tool(name="Plot Distributions", func=plot_distributions, description="Generates histograms for numeric columns"),
    Tool(name="Plot Correlation", func=plot_correlation, description="Generates a heatmap of correlations"),
]

# ===============================
# 5️⃣ Initialize LangChain agent
# ===============================
llm = ChatOpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# ===============================
# 6️⃣ Run the agent
# ===============================
response = agent.run(optimized_task)
print("\n===== AGENT RESPONSE =====\n")
print(response)
