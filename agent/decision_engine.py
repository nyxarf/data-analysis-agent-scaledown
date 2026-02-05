class DecisionEngine:
    def decide_next(self, schema, history):
        steps_done = set()

        # Only look at the last 20 history entries
        for h in history[-20:]:
            if isinstance(h, str) and ":done" in h:
                steps_done.add(h.split(":")[0])

        if "load_data" not in steps_done:
            return "load_data"
        if "clean_data" not in steps_done:
            return "clean_data"
        if "analyze_data" not in steps_done:
            return "analyze_data"

        return "done"
