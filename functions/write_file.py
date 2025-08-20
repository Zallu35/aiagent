import os


def write_file(working_directory, file_path, content):
    joined_path= os.path.join(working_directory, file_path)
    complete_path=os.path.abspath(joined_path)
    if not complete_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(complete_path):
        try:
            os.makedirs(os.path.dirname(complete_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(complete_path) and os.path.isdir(complete_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(complete_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'