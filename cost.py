# cost.py
import os
import time
from functools import wraps

# If using OpenAI
import openai

# For Google GenAI (new package)
try:
    import google.genai as genai
except ImportError:
    genai = None

# Middleware decorator to handle API errors, retries, and logging
def api_middleware(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except openai.error.RateLimitError:
                    print(f"OpenAI rate limit reached. Retry {retries + 1}/{max_retries} after {delay}s...")
                    retries += 1
                    time.sleep(delay)
                except openai.error.OpenAIError as e:
                    print(f"OpenAI API Error: {e}")
                    break
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    break
            return None
        return wrapper
    return decorator

# Example function to calculate cost of a request
@api_middleware(max_retries=3, delay=2)
def calculate_openai_cost(prompt_tokens, completion_tokens, model="gpt-3.5-turbo"):
    # OpenAI pricing per 1K tokens
    pricing = {
        "gpt-3.5-turbo": 0.002,  # per 1K tokens
        "gpt-4": 0.03
    }
    price_per_1k = pricing.get(model, 0.002)
    total_tokens = prompt_tokens + completion_tokens
    cost = (total_tokens / 1000) * price_per_1k
    return round(cost, 6)

# Optional: Google GenAI cost calculation
@api_middleware(max_retries=3, delay=2)
def calculate_google_genai_cost(units_used):
    if not genai:
        print("Google GenAI SDK not installed")
        return None
    # Replace with actual pricing logic
    cost_per_unit = 0.001  # placeholder
    return round(units_used * cost_per_unit, 6)
