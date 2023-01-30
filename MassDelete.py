import glob
import os
import shutil

#keyword =''
#files = glob.glob("/Volumes/SSD/production/*/*.csv")
def filetype_delete(file_location,filetype):
    file_path=file_location+'/*'+filetype
    files=glob.glob(file_path)
    for x in files:
        if os.path.exists(x):
            os.remove(x)
    print('all'+ filetype+ ' files from ' +file_location+ ' deleted.')


def folder_clean_up(file_location,exclude_folder_name):
    folder_path=file_location+'/*'
    folders = glob.glob(folder_path)
    for folder in folders:
        if exclude_folder_name not in os.path.basename(folder):
           shutil.rmtree(folder)
    print('All folders in ' + file_location + ' deleted')


def csv_folder_delete(file_location):
    folder_path = glob.glob(file_location + '/*')
    for folders in folder_path:
        csv_file = folders + '/*.csv'
        csv_files = glob.glob(csv_file)
        print('Deleting files from ' + os.path.dirname(csv_files[0]))
        for files in csv_files:
            os.remove(files)
        print('all files in ' + folders)


csv_folder_delete('/Volumes/TPC')
folder_clean_up('/Volumes/TPC','xml')





