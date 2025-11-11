#!/usr/bin/env python
"""Test script to list available Gemini models"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

try:
    import google.generativeai as genai

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env file")
        exit(1)

    genai.configure(api_key=api_key)

    print("Available Gemini models:")
    print("-" * 50)

    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✓ {model.name}")
            print(f"  Display name: {model.display_name}")
            print(f"  Description: {model.description[:100]}..." if len(model.description) > 100 else f"  Description: {model.description}")
            print()

    print("-" * 50)
    print("\nTesting model creation:")

    # Test different model names
    test_models = [
        'models/gemini-1.5-flash',
        'models/gemini-1.5-flash-latest',
        'gemini-1.5-flash',
        'gemini-1.5-flash-latest',
        'models/gemini-pro',
        'gemini-pro'
    ]

    for model_name in test_models:
        try:
            model = genai.GenerativeModel(model_name)
            print(f"✓ SUCCESS: '{model_name}' works!")
        except Exception as e:
            print(f"✗ FAILED: '{model_name}' - {str(e)[:80]}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

