import os
import random
import shutil
import tempfile
import timeit
import zipfile

import matplotlib.pyplot as plt

from interprocess_deletion_example import delete_file_from_zip

# Function definitions
def overwrite_in_zip_file(zip_file_path, file_path, data):
    delete_file_from_zip(zip_file_path,file_path)
    with zipfile.ZipFile(zip_file_path, 'a') as zip_write:
        zip_write.writestr(file_path, data)

def replace_in_zip_file(zip_file_path, file_path, data):
    temp_filename = tempfile.mktemp()
    with zipfile.ZipFile(zip_file_path, 'r') as zip_read:
        with zipfile.ZipFile(temp_filename, 'w', zipfile.ZIP_DEFLATED) as zip_write:
            for item in zip_read.infolist():
                if item.filename != file_path:
                    zip_write.writestr(item, zip_read.read(item.filename))
                else:
                    zip_write.writestr(file_path, data)
    shutil.move(temp_filename, zip_file_path)

# Test setup
def create_zip_file(filename, data):
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for i in range(100):
            zipf.writestr(f'dummy_text_{i}.txt', f'{data}')


# Time measurement
file_sizes = [10, 50, 100, 500,1000, 5000, 10000, 50000, 100000]
overwrite_times = []
replace_times = []

for size in file_sizes:
    data = bytes(random.randint(0, 255) for _ in range(size))

    # Measure overwrite_in_zip_file
    create_zip_file('overwrite.zip', data)
    start_time = timeit.default_timer()
    overwrite_in_zip_file('overwrite.zip', 'dummy_text_5.txt', data)
    end_time = timeit.default_timer()
    overwrite_times.append(end_time - start_time)

    # Measure replace_in_zip_file
    create_zip_file('rewrite_by_comparison.zip', data)
    start_time = timeit.default_timer()
    replace_in_zip_file('rewrite_by_comparison.zip', 'dummy_text_5.txt', data)
    end_time = timeit.default_timer()
    replace_times.append(end_time - start_time)

# Matplotlib plot
plt.figure(figsize=(10, 6))
plt.plot(file_sizes, overwrite_times, label='New Custom Solution')
plt.plot(file_sizes, replace_times, label='Standard Python Library Solutions')
plt.xlabel('File Size (bytes)')
plt.ylabel('Time (seconds)')
plt.title('Time taken by methods at increasing file sizes')
plt.legend()
plt.grid(True)
plt.show()
