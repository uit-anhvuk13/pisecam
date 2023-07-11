import constants
import os
import pyrebase
from pprint import pprint

Firebase = pyrebase.initialize_app(constants.FIREBASE_CONFIG)
Storage = Firebase.storage()
Database = Firebase.database()

def push_file(File):
    Dir = f'{constants.TYPE_VIDEO}/{File.split("_")[0]}'
    Filename = File.split("_")[-1]
    Storage.child(f'{Dir}/{Filename}').put(File)
    os.system("rm {0}".format(File))

def get_files(FirebaseFolder):
    Files = Storage.bucket.list_blobs(prefix = FirebaseFolder)
    Result = []
    for File in Files:
        File.make_public()
        Result.append({"name": File.name.split('/')[-1], "public_url": File.public_url})
    return Result

def get_subfolders(FirebaseFolder):
    Items = Storage.bucket.list_blobs(prefix = FirebaseFolder)
    SubFolders = []
    for Item in Items:
        SubFolders.append(Item.name.split('/')[1])
    return list(set(SubFolders))
