import os
from typing import Optional
from dotenv import load_dotenv
load_dotenv()


class MockClient:
    """
    Offline stand-in for an LLM client.
    This lets the app run without an API key.
    """

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        # Very small, predictable behavior for demos.
        if "Return ONLY valid JSON" in system_prompt:
            # Purposely not JSON to force fallback unless students change behavior.
            return "I found some issues, but I'm not returning JSON right now."
        return "# MockClient: no rewrite available in offline mode.\n"


class GroqClient:
    """
    Groq API wrapper using the Groq SDK.

    Requirements:
    - groq installed (pip install groq)
    - GROQ_API_KEY set in environment (or loaded via python-dotenv)
    """

    def __init__(self, model_name: str = "qwen/qwen3-32b", temperature: float = 0.6):
        from groq import Groq
        self.client = Groq()  # reads GROQ_API_KEY from environment automatically
        self.model_name = model_name
        self.temperature = temperature

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=self.temperature,
                max_completion_tokens=4096,
                top_p=0.95,
                reasoning_effort="default",
                stream=True,
                stop=None,
            )
            result = ""
            for chunk in completion:
                result += chunk.choices[0].delta.content or ""
            return result   # full text, same as non-streaming from the agent's perspective
        except Exception:
            return ""


class GeminiClient:
    """
    Minimal Gemini API wrapper with added error resilience.

    Requirements:
    - google-generativeai installed
    - GEMINI_API_KEY set in environment (or loaded via python-dotenv)
    """

    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.2):
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError(
                "Missing GEMINI_API_KEY. Create a .env file and set GEMINI_API_KEY=..."
            )

        # Import here so heuristic mode doesn't require the dependency at import time.
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.temperature = float(temperature)

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends a single request to Gemini.

        UPDATED: Added try/except to handle rate limits and API errors gracefully.
        If an error occurs, it returns an empty string, triggering the agent's 
        heuristic fallback logic.
        """
        try:
            response = self.model.generate_content(
                [
                    {"role": "system", "parts": [system_prompt]},
                    {"role": "user", "parts": [user_prompt]},
                ],
                generation_config={"temperature": self.temperature},
            )

            # Defensive: response.text can be None or raise an error if blocked by filters.
            return response.text or ""
            
        except Exception as e:
            # Returning empty string allows the agent to detect the failure 
            # and switch to offline rules.
            return ""
