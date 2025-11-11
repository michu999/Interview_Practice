"""
AI Service Layer - Clean Architecture for Multiple AI Providers
This module provides a unified interface for interacting with different AI models.
"""
import os
import re
import logging
from abc import ABC, abstractmethod
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)


class AIResponse:
    """Standardized AI response object"""
    def __init__(self, title: str, content: str, latitude: float, longitude: float):
        self.title = title[:200]  # Limit to model field size
        self.content = content
        self.latitude = latitude
        self.longitude = longitude


class AIServiceBase(ABC):
    """Base class for all AI service providers"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    @abstractmethod
    def generate_travel_post(self, prompt: str) -> AIResponse:
        """Generate a travel blog post from a prompt"""
        pass

    def extract_coordinates(self, prompt: str) -> tuple[Optional[float], Optional[float]]:
        """
        Extract GPS coordinates from prompt text
        Returns: (latitude, longitude) or (None, None) if not found
        """
        # Pattern to match coordinates like: 52.2297, 21.0122 or -8.4095, 115.1889
        coord_patterns = [
            r'(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)',  # Simple: 52.2297, 21.0122
            r'współrzędne:\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)',  # Polish: współrzędne: 52.2297, 21.0122
            r'coordinates:\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)',  # English: coordinates: 52.2297, 21.0122
            r'lat:\s*(-?\d+\.?\d*)\s*,?\s*lon[g]?:\s*(-?\d+\.?\d*)',  # lat: 52.2297, lon: 21.0122
        ]

        for pattern in coord_patterns:
            match = re.search(pattern, prompt.lower())
            if match:
                try:
                    lat = float(match.group(1))
                    lng = float(match.group(2))
                    # Validate coordinate ranges
                    if -90 <= lat <= 90 and -180 <= lng <= 180:
                        return lat, lng
                except (ValueError, IndexError):
                    continue

        return None, None

    def extract_title_from_prompt(self, prompt: str, default: str = "Niesamowita Podróż") -> str:
        """Extract a title from the prompt text"""
        # Try to find location name after common keywords
        keywords = ['o ', 'w ', 'na ', 'z ', 'dla ', 'about ', 'in ', 'at ', 'from ']

        for keyword in keywords:
            if keyword in prompt.lower():
                parts = prompt.lower().split(keyword)
                if len(parts) > 1:
                    potential_title = parts[1].split('.')[0].split(',')[0].split('współ')[0].strip()
                    if 3 < len(potential_title) < 100:
                        # Capitalize properly
                        return ' '.join(word.capitalize() for word in potential_title.split())

        return default


class OpenAIService(AIServiceBase):
    """OpenAI ChatGPT service implementation"""

    def generate_travel_post(self, prompt: str) -> AIResponse:
        """Generate content using OpenAI's ChatGPT"""
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)

            # Extract coordinates from prompt
            lat, lng = self.extract_coordinates(prompt)
            if lat is None or lng is None:
                lat, lng = 52.2297, 21.0122  # Default: Warsaw

            # Enhanced prompt for better travel content
            enhanced_prompt = f"""Jesteś ekspertem od blogów podróżniczych. Na podstawie poniższego promptu napisz ciekawy, angażujący post na bloga podróżniczego w języku polskim.

Prompt użytkownika: {prompt}

Wymogi:
- Pisz w języku polskim
- Używaj emotikonów i formatowania dla lepszej czytelności
- Podziel tekst na sekcje z nagłówkami (używaj prostego formatowania tekstowego)
- Opisz główne atrakcje, kulturę, kuchnię i praktyczne porady
- Napisz 300-500 słów
- Bądź entuzjastyczny i inspirujący
- Skoncentruj się na praktycznych informacjach dla podróżników"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Jesteś profesjonalnym blogerem podróżniczym, który pisze angażujące treści w języku polskim."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                max_tokens=1000,
                temperature=0.8
            )

            content = response.choices[0].message.content.strip()
            title = self.extract_title_from_prompt(prompt)

            logger.info(f"OpenAI successfully generated post: {title}")
            return AIResponse(title=title, content=content, latitude=lat, longitude=lng)

        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"Błąd OpenAI API: {str(e)}")


class GeminiService(AIServiceBase):
    """Google Gemini service implementation"""

    def generate_travel_post(self, prompt: str) -> AIResponse:
        """Generate content using Google Gemini"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)

            # Use gemini-2.5-pro - confirmed working model
            model = genai.GenerativeModel('gemini-2.5-pro')
            logger.info(f"Using Gemini model: gemini-2.5-pro")


            # Extract coordinates from prompt
            lat, lng = self.extract_coordinates(prompt)
            if lat is None or lng is None:
                lat, lng = 52.2297, 21.0122  # Default: Warsaw

            # Enhanced prompt for better travel content
            enhanced_prompt = f"""Jesteś ekspertem od blogów podróżniczych. Napisz fascynujący post na bloga podróżniczego w języku polskim na podstawie poniższego opisu.

Opis: {prompt}

Wytyczne:
- Pisz TYLKO w języku polskim
- Używaj emotikonów (🌍, ✨, 🏨, 🍽️, 💡, 📸, etc.) dla lepszej czytelności
- Podziel na sekcje z wyraźnymi nagłówkami
- Opisz atrakcje, kulturę, jedzenie, zakwaterowanie i praktyczne wskazówki
- Długość: 300-500 słów
- Ton: entuzjastyczny, przyjazny, inspirujący
- Dodaj konkretne porady dla podróżujących"""

            response = model.generate_content(enhanced_prompt)
            content = response.text.strip()
            title = self.extract_title_from_prompt(prompt)

            logger.info(f"Gemini successfully generated post: {title}")
            return AIResponse(title=title, content=content, latitude=lat, longitude=lng)

        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise Exception(f"Błąd Gemini API: {str(e)}")


class DeepSeekService(AIServiceBase):
    """DeepSeek service implementation"""

    def generate_travel_post(self, prompt: str) -> AIResponse:
        """Generate content using DeepSeek API"""
        try:
            import requests

            # Extract coordinates from prompt
            lat, lng = self.extract_coordinates(prompt)
            if lat is None or lng is None:
                lat, lng = 52.2297, 21.0122  # Default: Warsaw

            # Enhanced prompt for better travel content
            enhanced_prompt = f"""Jesteś specjalistą od blogów podróżniczych. Stwórz szczegółowy post podróżniczy w języku polskim.

Temat: {prompt}

Wymagania:
- Pisz WYŁĄCZNIE w języku polskim
- Używaj emotikonów dla lepszej prezentacji (🌍, ⭐, 🏖️, 🍴, 🏨, 💡)
- Strukturyzuj tekst z wyraźnymi sekcjami
- Zawrzyj: główne atrakcje, kulturę lokalną, kulinaria, opcje noclegowe, praktyczne porady
- Długość: około 400 słów
- Styl: analityczny ale przystępny, inspirujący do podróży
- Dodaj konkretne, praktyczne informacje"""

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Jesteś ekspertem od blogów podróżniczych, który tworzy wysokiej jakości treści w języku polskim."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }

            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            response.raise_for_status()
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            title = self.extract_title_from_prompt(prompt)

            logger.info(f"DeepSeek successfully generated post: {title}")
            return AIResponse(title=title, content=content, latitude=lat, longitude=lng)

        except requests.exceptions.RequestException as e:
            logger.error(f"DeepSeek API error: {str(e)}")
            raise Exception(f"Błąd DeepSeek API: {str(e)}")


class AIServiceFactory:
    """Factory class to create appropriate AI service instances"""

    @staticmethod
    def create_service(model_name: str) -> AIServiceBase:
        """
        Create and return the appropriate AI service based on model name

        Args:
            model_name: Name of the AI model (ChatGPT, Gemini, DeepSeek)

        Returns:
            AIServiceBase instance

        Raises:
            ValueError: If model is not supported or API key is missing
        """
        # Get API keys from environment
        api_keys = {
            'ChatGPT': os.getenv('OPENAI_API_KEY'),
            'Gemini': os.getenv('GEMINI_API_KEY'),
            'DeepSeek': os.getenv('DEEPSEEK_API_KEY'),
        }

        # Map model names to service classes
        services = {
            'ChatGPT': OpenAIService,
            'Gemini': GeminiService,
            'DeepSeek': DeepSeekService,
        }

        if model_name not in services:
            raise ValueError(f"Model '{model_name}' nie jest obsługiwany. Dostępne modele: {', '.join(services.keys())}")

        api_key = api_keys.get(model_name)
        if not api_key:
            raise ValueError(f"Brak klucza API dla modelu {model_name}. Sprawdź plik .env")

        logger.info(f"Creating AI service for model: {model_name}")
        return services[model_name](api_key)


def generate_ai_blog_post(model_name: str, prompt: str) -> AIResponse:
    """
    Main entry point for generating AI blog posts

    Args:
        model_name: Name of AI model to use
        prompt: User's prompt text

    Returns:
        AIResponse object with generated content

    Raises:
        ValueError: If model is not supported
        Exception: If AI generation fails
    """
    try:
        service = AIServiceFactory.create_service(model_name)
        return service.generate_travel_post(prompt)
    except Exception as e:
        logger.error(f"Failed to generate blog post with {model_name}: {str(e)}")
        raise

