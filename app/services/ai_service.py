import json
from openai import AsyncOpenAI
from app.core.config import settings

class AIService:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_text(self, text: str) -> dict:
        """
        Analyze text using OpenAI to generate summary and sentiment.
        """
        if not self.client:
            # Fallback if no key is provided
            return {
                "summary": "AI Key not configured. Using mock summary.",
                "sentiment": "Neutral"
            }

        try:
            prompt = f"""
            Analyze the following text. 
            1. Provide a concise summary.
            2. Determine the sentiment (Positive, Negative, or Neutral).
            
            Return the result in valid JSON format with keys "summary" and "sentiment".
            
            Text:
            {text}
            """

            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that analyzes text. You always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            result = json.loads(content)
            
            return {
                "summary": result.get("summary", "Could not generate summary"),
                "sentiment": result.get("sentiment", "Neutral")
            }
            
        except Exception as e:
            print(f"AI Error: {e}")
            return {
                "summary": "Error processing AI request.",
                "sentiment": "Neutral"
            }

ai_service = AIService()
