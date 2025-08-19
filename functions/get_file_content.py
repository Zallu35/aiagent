import os
import functions.config


def get_file_content(working_directory, file_path):
    joined_path= os.path.join(working_directory, file_path)
    complete_path=os.path.abspath(joined_path)
    if not complete_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(complete_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(complete_path, "r") as f:
            file_content_string = f.read(functions.config.MAX_CHARACTERS)
        if len(file_content_string)==functions.config.MAX_CHARACTERS:
            return file_content_string + f'\n[...FILE "{file_path}" truncated at {functions.config.MAX_CHARACTERS} characters]'
        else:
            return file_content_string
    except Exception as e:
        return f"Error: {e}"