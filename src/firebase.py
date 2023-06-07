import pyrebase
import constants
from datetime import datetime

from pprint import pprint


firebase = pyrebase.initialize_app(constants.firebaseConfig)
storage = firebase.storage()
db = firebase.database()
def push_file(local_path, type):
  current_date = datetime.today().strftime("%d-%m-%Y")
  
  filename = local_path.split("/")[-1]
  
  storage.child(type + "/" + current_date + "/" + filename).put(local_path)

  print("public: " +storage.child(type+filename).get_url(token=None))


def get_files(firebase_folder):
  files = storage.bucket.list_blobs(prefix=firebase_folder)

  # print file names
  result = []
  for file in files:
    
    file.make_public()
    # print(dir(file))

    arr = file.name.split('/') # {current, sub_name, ''}
    if(len(arr) == 3 and arr[2] != ''):
      result.append({"name":arr[-1], "public_url": file.public_url})

  return result

def get_subfolders(firebase_folder):
  files = storage.bucket.list_blobs(prefix=firebase_folder)

  # print file names
  subfolders = []
  for file in files:
    # print(file)
    arr = file.name.split('/') # {current, sub_name, ''}a=
    subfolders.append(arr[1])

  return list(set(subfolders))

# push_file("/home/dinhnhi/Downloads/videoplayback2.mp4", constants.TYPE_VIDEO)


# result = get_files("videos/Ngay1")
# print(result)
# result = get_subfolders('videos/')