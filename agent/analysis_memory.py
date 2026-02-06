class AnalysisMemory:
    def __init__(self):
        self.steps_done = []
        self.insights = []
    def add(self, key, value):
        self.steps_done.append((key, value))

    def add_step(self, step_name):
        self.steps_done.append(f"{step_name}:done")

    def add_insight(self, insight):
        self.insights.append(insight)

    def compress(self):
        
        return self.steps_done + self.insights
