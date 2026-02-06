print("Starting Data Analysis Agent...")

import pandas as pd
from agent import SchemaCompressor, AnalysisMemory, DecisionEngine, Executor

df = pd.read_csv("data/sample_dataset.csv")

df["Amount"] = (
    df["Amount"]
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
    .astype(float)
)

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)

schema = SchemaCompressor(df).compress()
print("Schema compression:", schema["metrics"])

memory = AnalysisMemory()
engine = DecisionEngine()
executor = Executor(df)


while True:
    history = memory.compress() or []  
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

    memory.add_step(step)
    memory.add_insight(insight)



print("EDA Completed")
compressed_history = memory.compress()
for h in compressed_history:
    print("-", h)
