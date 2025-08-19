import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)
args=sys.argv[1:]
user_prompt=" ".join(args)
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]

def main():
    reply = client.models.generate_content(model='gemini-2.0-flash-001', contents=messages)
    if len(sys.argv) <= 1:
        raise Exception("No prompt provided")
        sys.exit(1)
    print(reply.text)
    #print(reply.usage_metadata)
    prompt_tokens = reply.usage_metadata.prompt_token_count
    response_tokens = reply.usage_metadata.candidates_token_count
    if "--verbose" in args:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
