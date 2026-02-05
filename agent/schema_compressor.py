from agent.scaledown_client import ScaleDownClient

class SchemaCompressor:
    def __init__(self, df):
        self.df = df
        self.client = ScaleDownClient()

    def compress(self):
        schema_text = "\n".join(
            f"{col}: {self.df[col].dtype}"
            for col in self.df.columns
        )

        result = self.client.compress_text(schema_text, max_tokens=80)

        return {
            "compressed_schema": result["compressed_text"],
            "metrics": {
                "original_chars": result["original_chars"],
                "compressed_chars": result["compressed_chars"],
                "mode": result["mode"]
            }
        }
