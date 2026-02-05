class AnalysisMemory:
    def __init__(self):
        self.steps_done = []
        self.insights = []

    def add_step(self, step_name):
        self.steps_done.append(f"{step_name}:done")

    def add_insight(self, insight):
        self.insights.append(insight)

    def compress(self):
        # Return a single list combining steps and insights
        return self.steps_done + self.insights
