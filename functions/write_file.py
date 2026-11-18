import os
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes/Overwrites a file with given content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path":{
                    "type": "string",
                    "description": "The file path we want to write the contents to."
                },
                "content":{
                    "type": "string",
                    "description": "Is the content that we want to write to the file path"
                }

            }, 
            "required": ["file_path","content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_dir),exist_ok=True)
        with open(target_dir,"w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"


