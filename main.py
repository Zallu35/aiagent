import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)
args=sys.argv[1:]
user_prompt=" ".join(args)
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
system_prompt='''
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
'''
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def main():
    if len(sys.argv) <= 1:
        raise Exception("No prompt provided")
        sys.exit(1)

    x=20
    while x>0:
        reply = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
        )
        for candidate in reply.candidates:
            messages.append(candidate.content)

        #print(f"reply.text exists: {bool(reply.text)}")
        #print(f"reply.function_calls exists: {bool(reply.function_calls)}")
        #if reply.function_calls:
            #print(f"Number of function calls: {len(reply.function_calls)}")

        

        if reply.function_calls:
            function_responses = []
            for func in reply.function_calls:
                #print(f"Calling function: {func.name}({func.args})")
                function_output=call_function(func, verbose="--verbose" in args)
                if not function_output.parts[0].function_response.response:
                    raise RuntimeError("Missing response from function call!")
                if "--verbose" in args:
                    print(f"-> {function_output.parts[0].function_response.response}")
                function_responses.append(function_output.parts[0])
            messages.append(types.Content(role="user", parts=function_responses))
        elif reply.text:
            print(reply.text)
            break
        x-=1
    

    prompt_tokens = reply.usage_metadata.prompt_token_count
    response_tokens = reply.usage_metadata.candidates_token_count
    if "--verbose" in args:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
