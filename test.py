from agent.scaledown_client import ScaleDownClient

client = ScaleDownClient()
result = client.compress_text("This is a test for the real ScaleDown API.", max_tokens=50)
print(result)
