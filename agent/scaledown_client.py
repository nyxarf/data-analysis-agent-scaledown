

import os
import requests
from dotenv import load_dotenv

load_dotenv()


class ScaleDownClient:
    def __init__(self):
        self.api_key = os.getenv("SCALEDOWN_API_KEY")
        self.mode = os.getenv("SCALEDOWN_MODE", "mock").lower()

        if self.mode == "api" and not self.api_key:
            print("[WARNING] SCALEDOWN_MODE=api but no API key found. Falling back to mock mode.")
            self.mode = "mock"

    def compress_text(self, text: str, max_tokens: int = 100) -> dict:
        """
        Compress text using ScaleDown API or fallback to mock if API fails.
        Returns dict with:
            - compressed_text
            - original_chars
            - compressed_chars
            - mode ('api' or 'mock')
        """

        if self.mode != "api":
            
            compressed = text[:max_tokens]
            return {
                "compressed_text": compressed,
                "original_chars": len(text),
                "compressed_chars": len(compressed),
                "mode": "mock",
            }

        
        try:
            response = requests.post(
                "https://api.scaledown.ai/compress",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={"text": text, "max_tokens": max_tokens},
                timeout=10  
            )
            response.raise_for_status()
            data = response.json()

            return {
                "compressed_text": data.get("compressed_text", text[:max_tokens]),
                "original_chars": len(text),
                "compressed_chars": len(data.get("compressed_text", text[:max_tokens])),
                "mode": "api"
            }

        except Exception as e:
            
            print(f"[WARNING] ScaleDown API failed ({e}). Using mock compression instead.")
            compressed = text[:max_tokens]
            return {
                "compressed_text": compressed,
                "original_chars": len(text),
                "compressed_chars": len(compressed),
                "mode": "mock",
            }
