import os



def get_files_info(working_directory, directory="."):
    full_path=os.path.join(working_directory, directory)
    #print(full_path)
    #print(os.path.abspath(full_path))
    if not os.path.abspath(full_path).startswith(os.path.abspath(working_directory)):
        return f'Result for {directory} directory\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Result for {directory} directory\n    Error: "{directory}" is not a directory'

    file_data=[]
    directory_list=os.listdir(full_path)
    for file in directory_list:
        file_data.append(f'- {file}: file_size={os.path.getsize(os.path.abspath(full_path)+'/'+file)} bytes, is_dir={os.path.isdir(os.path.abspath(full_path)+'/'+file)}')
    output="\n ".join(file_data)
    return f'Result for {directory} directory\n {output}'
    