print("Starting Data Analysis Agent...")

import pandas as pd
from agent import SchemaCompressor, AnalysisMemory, DecisionEngine, Executor

# Load data
df = pd.read_csv("data/sample_dataset.csv")

# Clean Amount column
df["Amount"] = (
    df["Amount"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

# Parse Date
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

# Compress schema
schema = SchemaCompressor(df).compress()
print("Schema compression:", schema["metrics"])

# Initialize memory, engine, executor
memory = AnalysisMemory()
engine = DecisionEngine()
executor = Executor(df)

# Main loop
while True:
    history = memory.compress() or []  # ensures list
    if isinstance(history, str):
        history = [history]

    print("History:", history)

    decision = engine.decide_next(schema, history)
    print("Next step:", decision)

    if decision == "done":
        break

    step, insight = executor.run(decision)

    if step is None:
        print(f"Executor could not handle step: {decision}")
        break

    # ✅ Store the "step done" properly
    memory.add_step(step)
    memory.add_insight(insight)




# Print results
print("EDA Completed")
compressed_history = memory.compress()
for h in compressed_history:
    print("-", h)
