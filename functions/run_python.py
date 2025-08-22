import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    joined_path= os.path.join(working_directory, file_path)
    complete_path=os.path.abspath(joined_path)
    if not complete_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(complete_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        command = ["python3", complete_path] + (args if args else [])
        pyfile_return=subprocess.run(command, capture_output=True, timeout=30, cwd=os.path.abspath(working_directory), text=True)
        output = []

        if pyfile_return.stdout:
            output.append(f"STDOUT:\n{pyfile_return.stdout}")

        if pyfile_return.stderr:
            output.append(f"STDERR:\n{pyfile_return.stderr}")
            
        if pyfile_return.returncode != 0:
            output.append(f"Process exited with code {pyfile_return.returncode}")

        if output:  
            return "\n".join(output)
        else:  
            return "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a given python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The relative path to the file to be executed.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="The argumetns to pass to the function within the python file being run. Not all functions need arguments so this is optional."
            )
        },
        required=["file_path"],
    ),
)