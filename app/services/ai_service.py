import asyncio
import random

class AIService:
    async def analyze_text(self, text: str) -> dict:
        """
        Mock AI analysis.
        In a real scenario, this would call OpenAI, Vertex AI, or HuggingFace.
        """
        # Simulate network delay
        await asyncio.sleep(1) 

        # Simple mock logic
        summary = f"Summary of: {text[:50]}..."
        
        sentiments = ["Positive", "Negative", "Neutral"]
        sentiment = random.choice(sentiments)
        
        # Basic keyword detection for slightly better mock
        lower_text = text.lower()
        if "good" in lower_text or "great" in lower_text or "love" in lower_text:
            sentiment = "Positive"
        elif "bad" in lower_text or "hate" in lower_text or "terrible" in lower_text:
            sentiment = "Negative"

        return {
            "summary": summary,
            "sentiment": sentiment
        }

ai_service = AIService()
