import subprocess
import json
import os

def delete_file_from_zip(zip_file_path, file_to_delete):
    input_data = {
        "ZipFilePath": zip_file_path,
        "FileToDelete": file_to_delete
    }
    json_input = json.dumps(input_data)
    result = subprocess.run(["ZipProc.exe"], input=json_input, text=True, capture_output=True)

    try:
        result_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        result_data = {"Success": False, "Path": "Invalid JSON format."}

    return result_data

def on_success(file_path):
    print(f"Deletion successful for file: {file_path}")
    # Trigger your function for success here

def on_failure(file_path):
    print(f"Deletion failed for file: {file_path}")
    # Trigger your function for failure here



if __name__ == '__main__':
        
    # Two test cases
    root_level_file = "backyard_chute_b.prefab"
    subdir_file = "prefabs/backyard_chute_b.prefab"

    zip_name = "data2.pak"
    zip_path = os.path.join(str(os.getcwd()), zip_name)

    result1 = delete_file_from_zip(zip_path, root_level_file)
    if result1['Success']:
        on_success(result1['Path'])
    else:
        on_failure(result1['Path'])

    result2 = delete_file_from_zip(zip_path, subdir_file)
    if result2['Success']:
        on_success(result2['Path'])
    else:
        on_failure(result2['Path'])
