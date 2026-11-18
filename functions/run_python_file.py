import os, subprocess
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs python file with given optional arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the target file.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional arguments to pass with file we want to run"
            },
        },
            "required": ["file_path"],
        },
    },
}

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'       
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'



        command = ["python", target_dir]
        if args is not None:
            command.extend(args)
        object = subprocess.run(command,capture_output=True,text=True,timeout=30, cwd = working_dir_abs)
        output = ""
        if object.returncode != 0:
            output += f"Process exited with code {object.returncode} "
        if object.stdout == None and object.stderr == None:
            output += "No output produced"
        else:
            if object.stdout != None:
                output += f"STDOUT: {object.stdout}"
            if object.stderr != None:
                output += f"STDERR: {object.stderr}"
        return output


    except Exception as e:
        return f"Error: executing Python file: {e}"

