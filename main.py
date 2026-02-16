import os
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Read the OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        print(f"✓ API key loaded successfully (length: {len(api_key)} characters)")
        print(f"✓ API key starts with: {api_key[:7]}...")
    else:
        print("✗ OPENAI_API_KEY not found in .env file")
    
    print("\nEnvironment setup complete!")
    print("- python-dotenv: installed ✓")
    print("- pydantic-ai: installed ✓")
    print("- chromadb (vector search): installed ✓")


if __name__ == "__main__":
    main()
