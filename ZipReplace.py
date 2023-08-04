import gzip
import os
import shutil
import tempfile
import timeit
import zipfile
import zlib
from pathlib import Path


class VirtualZip:
    def __init__(self, zip_path):
        self.zip_path = zip_path
        self.virtual_overwrite = False
        self.temp_dir = tempfile.mkdtemp()
        
    def open(self):
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)

    def filenames(self):
        return [str(path) for path in Path(self.temp_dir).rglob('*') if path.is_file()]

    def write(self, file_path, content):
        with open(os.path.join(self.temp_dir, file_path), 'w', encoding='latin1') as f:
            f.write(content)

    def close(self):
        destination_path = self.zip_path if self.virtual_overwrite else self.zip_path.replace('.zip', '_virtual.zip')
        
        if self.virtual_overwrite and os.path.exists(self.zip_path):
            os.remove(self.zip_path)
            
        with zipfile.ZipFile(destination_path, 'w') as zipf:
            for root, dirs, files in os.walk(self.temp_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), self.temp_dir))
        shutil.rmtree(self.temp_dir)

# Utility functions

def replace_signature(content, signature, replacement):
    """Replace the given signature with a replacement in the content."""
    return content.replace(signature, replacement)


def replace_zip_file(temp_filename, zip_file_path):
    """Replace the original zip file with the temporary file."""
    shutil.move(temp_filename, zip_file_path)


def copy_from_old_zip(zip_write, item, zip_read):
    """Copy a file from the original zip to the new zip."""
    zip_write.writestr(item, zip_read.read(item.filename))


def write_new_data(zip_write, file_path, data):
    """Write new data to the new zip."""
    zip_write.writestr(file_path, data)


# Zip file handling functions

def add_file_to_zip(new_zip, path_to_file, file_content):
    """Add a file to the new zip archive."""
    start_time = timeit.default_timer()
    new_zip.writestr(path_to_file, file_content)
    elapsed_time = timeit.default_timer() - start_time
    print(f"File '{path_to_file}' added to the new zip archive. Elapsed Time: {elapsed_time:.5f} seconds")

def is_valid_zip(archive):
    """Check if the file is a valid zip archive."""
    # start_time = timeit.default_timer()
    result = zipfile.is_zipfile(archive)
    # elapsed_time = timeit.default_timer() - start_time
    # print(f"Validation of '{archive}' as a valid zip archive: {result}.                        Elapsed Time: {elapsed_time:.5f} seconds")
    return result

# Dictionary to store namelists for archives
archive_namelists = {}

def is_valid_zip(archive):
    """Check if the given file is a valid zip archive."""
    # Implement the logic to check if 'archive' is a valid zip archive
    # Return True if it's valid, otherwise False
    return True

def get_namelist_from_archive(archive):
    """Get the namelist from the given archive using caching."""
    global archive_namelists

    
    # Check if the namelist for this archive is already cached
    if archive in archive_namelists:
        
        return archive_namelists[archive]

    
    # If not cached, open the archive and get the namelist
    with zipfile.ZipFile(archive, 'r') as zip_file:
        namelist = zip_file.namelist()

    # Cache the namelist for future use
    archive_namelists[archive] = namelist
    return namelist

def process_archive_files(new_zip, archive, paths_to_files):
    """Process multiple file handles within a single archive."""

    # Check if the input 'archive' is a valid zip file
    if not is_valid_zip(archive):
        print(f"ERROR: '{archive}' is not a valid zip archive. Skipping...")
        return

    # Get the namelist for the archive using caching
    namelist = get_namelist_from_archive(archive)

    # Open the archive once and read all the specified files
    with zipfile.ZipFile(archive, 'r') as original_zip:
        for path_to_file in paths_to_files:
            # Check if the specified 'path_to_file' exists in the namelist
            if path_to_file in namelist:
                # Read the content of the file
                file_content = original_zip.read(path_to_file)
                # Add the read file to the new zip archive
                add_file_to_zip(new_zip, path_to_file, file_content)
            else:
                # If the specified file is not found in the namelist, print an error message
                print(f"ERROR: File '{path_to_file}' not found in archive '{archive}'. Skipping...")

def gather_and_zip_files(file_handles, output_file='data2.pak'):
    """Gather specified files and write them to a new zip archive.

    file_handles: a list of tuples in the format [(archive, path_to_file), ...]
    output_file: the name of the zip archive to create
    """
    mode = 'w' if not os.path.exists(output_file) else 'a'

    # Group paths by archive to process all paths for a single archive at once
    archive_file_paths = {}
    for archive, path_to_file in file_handles:
        if archive not in archive_file_paths:
            archive_file_paths[archive] = []
        archive_file_paths[archive].append(path_to_file)

    # Open or create the output_file to append new files
    with zipfile.ZipFile(output_file, mode, zipfile.ZIP_DEFLATED) as new_zip:
        for archive, paths_to_files in archive_file_paths.items():
            start_time = timeit.default_timer()
            process_archive_files(new_zip, archive, paths_to_files)
            elapsed_time = timeit.default_timer() - start_time
            print(f"Processing '{archive}' completed. Elapsed Time: {elapsed_time:.5f} seconds")

    print(f"Operation completed successfully. '{output_file}' has been created/updated.")


def copy_from_old_zip(zip_write, item, zip_read):
    """Copy a file from the original zip to the new zip."""
    zip_write.writestr(item, zip_read.read(item.filename))

def replace_in_zip_file(data2_zip_file_path, tuple_file_path, data):
    """Replace a file in a zip archive with new data.

    zip_file_path: path to the zip file
    file_path: path to the file inside the zip archive to replace
    data: the new data to write to the file
    """

    temp_filename = tempfile.mktemp()

    with zipfile.ZipFile(data2_zip_file_path, 'r') as data2_zip_read:

        with zipfile.ZipFile(temp_filename, 'w', zipfile.ZIP_DEFLATED) as temp_zip_write:

            for data2_item in data2_zip_read.infolist():

                if data2_item.filename != tuple_file_path:
                    print('condition 1')
                    copy_from_old_zip(temp_zip_write, data2_item, data2_zip_read)
                else:
                    print('condition 2\n'*100)
                    
                    write_new_data(temp_zip_write, tuple_file_path, data)


    replace_zip_file(temp_filename, data2_zip_file_path)
    

# File handling functions

def file_exists_in_zip(zip_file, file_path):
    """Check if a file exists in a zip archive."""
    with zipfile.ZipFile(zip_file, 'r', zipfile.ZIP_DEFLATED) as zip:
        return file_path in zip.namelist()


def read_and_decode_file_from_zip(zip_file, file_path):
    """Read and decode a file from a zip archive."""
    with zipfile.ZipFile(zip_file, 'r', zipfile.ZIP_DEFLATED) as zip:
        with zip.open(file_path, 'r') as file:
            raw_content = file.read()
            try:
                return raw_content.decode('utf-8')
            except UnicodeDecodeError:
                return raw_content.decode('latin1')


def process_and_replace_in_zip(zip_file, file_path, content, signature, replacement):
    """Process the content, replace the signature, and update the zip archive."""
    processed_content = replace_signature(content, signature, replacement)
    replace_in_zip_file(zip_file, file_path, processed_content.encode('utf-8'))


# Data extraction and processing functions

def find_substring_in_text(lines, search_pattern):
    """Find occurrences of a search_pattern in a list of lines."""
    occurrences = []

    for i, line in enumerate(lines):
        if search_pattern in line:
            occurrences.append((i, line))

    return occurrences


def get_filename(lines, index):
    """Get the filename from a list of lines and a given index."""
    path = None
    while not path:
        line = lines[index]
        if line.startswith('Path'):
            return line
        index -= 1


def get_lines_from_file(file_name):
    """Read file content into a list of lines."""
    with open(file_name, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
    return lines


def get_raw_paths(lines, signature):
    """Find the signature in lines and generate raw paths."""
    result = find_substring_in_text(lines, signature)
    raw_paths = []
    for index, _ in result:
        raw_paths.append(get_filename(lines, index))
    return raw_paths


def format_raw_paths(raw_paths):
    """Format raw paths into a list of tuples (archive, path_to_file)."""
    paths = set()
    base_path = Path("Path:  'Dying Light 2\\ph\\source\\")
    
    for raw_path in raw_paths:
        raw_path = Path(raw_path.strip())
        relative_path = raw_path.relative_to(base_path)
        source_archive = str(relative_path)[:5] + '.pak'
        
        if relative_path.parts[0] in ('data0', 'data1'):
            path = "/".join(relative_path.parts[1:])
        else:
            path = relative_path.as_posix()
        
        paths.add((source_archive, path[:-1]))
    
    return list(paths)



def get_files_with_signature(signature):
    """Return a list of tuples [(archive, path_to_file), ...] with files containing the signature."""
    lines = get_lines_from_file('master1.11.4.txt')
    raw_paths = get_raw_paths(lines, signature)
    return format_raw_paths(raw_paths)


def process_and_zip_files(file_handles, output_file='data2.pak', signature='random_signature_value', replacement='new_signature_value'):
    """Process the specified files in the zip archive, replacing a given signature with a new value.

    Args:
        file_handles (list of tuple): List of tuples in the format [(archive, path_to_file), ...].
        output_file (str): The name of the zip archive to process.
        signature (str): The signature to search for in the files.
        replacement (str): The new value to replace the signature with in the files.
    """
    
    total_files = len(file_handles)
    processed_files = 0

    # Open the zip file
    try:
        with zipfile.ZipFile(output_file, 'r', zipfile.ZIP_DEFLATED) as zip:
            # Iterate over file handles
            vZip = VirtualZip(output_file)
            vZip.open()
            print(vZip.filenames())
            for _, path_to_file in file_handles:
                # If path_to_file is in the archive, process its content and replace it in the zip
                
                if file_exists_in_zip(output_file, path_to_file):
                    
                    try:


                        content = read_and_decode_file_from_zip(output_file, path_to_file)
                        content = content.replace(signature, replacement)
                        vZip.write(path_to_file, content)
                        # process_and_replace_in_zip(output_file, path_to_file, content, signature, replacement)

                        processed_files += 1
                        remaining_files = total_files - processed_files
                        print(f"Processed {processed_files} out of {total_files}. Remaining files: {remaining_files}")

                    except (UnicodeDecodeError, zlib.error, gzip.BadGzipFile) as e:
                        print(f"Error processing file {path_to_file}: {e}")
            vZip.close()
    except zipfile.BadZipFile as e:
        print(f"Error opening zip file {output_file}: {e}")

# class Mod:
#     def __init__(self) -> None:
        
class Zip:
    def __init__(self, path) -> None:
        self.path = path
    
    def replace(self, old, new):
        '''
        Replaces all instances of string in every file within a zipfile
        
        ## arg1 -> str
        ## old 
        
        ## arg2 -> str
        ## new 
        '''
        handles = get_files_with_signature(old)
        gather_and_zip_files(handles, self.path)
        process_and_zip_files(handles, self.path, signature=old, replacement=new)
        
    
def main():
    # Move to the root folder containing data0.pak, data1.pak, and master1.11.4.txt
    os.chdir('C:/Users/dento/Desktop/Visual Studio Workspaces/modding/dl2/misc-tools/Tree Amortizer')
    zip = Zip('data2.pak')
    zip.replace('TinyObjectDensity;Low', 'TinyObjectDensity;Max')
    # handles = get_files_with_signature('TinyObjectDensity;')
    # gather_and_zip_files(handles, 'data2.pak')
    
    # process_and_zip_files(handles, 'data2.pak', signature='TinyObjectDensity;Low', replacement='TinyObjectDensity;Max')    

if __name__ == '__main__':
    main()
