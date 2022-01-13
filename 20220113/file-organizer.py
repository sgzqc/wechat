import os
from pathlib import Path

# define the file categories with dictionary
SUBDIR = {
        "DOCUMENTS":[".pdf",".docx",".txt"],
        "AUDIO":[".m4a",".m4b",".mp3"],
        "IMAGES":[".jpg",".jpeg",".png"]
        }

def pickDir(value):
    '''
    value: str contain extension of the file.
    return name of the category who defined before.
    e.g. value = '.pdf' so the function will return DOCUMENTS.
    '''
    for category, ekstensi in SUBDIR.items():
        for suffix in ekstensi:
            if suffix == value:
                return category

def organizeDir():
    '''
    this function will scan any files in the same directory, and then
    look at every extension of files and move that file to the exact category from calling the pickDir function.
    
    
    '''
    for item in os.scandir():
                
        #just looking for file, skip the directory
        if item.is_dir():
                continue
                
        filePath = Path(item)
        fileType = filePath.suffix.lower()
        directory = pickDir(fileType)
        
        #just skip, if the file extension not defined.
        if directory == None:
            continue
        
        directoryPath = Path(directory)
        #make new directory if the category's directory not found.
        if directoryPath.is_dir() != True:
                directoryPath.mkdir()
        filePath.rename(directoryPath.joinpath(filePath))

organizeDir()