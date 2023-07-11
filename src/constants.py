TIMEOUT = 0.04 # Gap time between 2 times getting a captured frame from camera
SERVER = '0.0.0.0' # Hosting IP address
PORT = 3000 # Hosting port
SEC_GAP_BETWEEN_SCORING = 0.45 # Gap time between 2 times sending frame to detector
SEC_TO_END_RECORD_WHEN_NO_DETECTION = 5 # Time to continue recording before stopping
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

FIREBASE_CONFIG = {
  "apiKey": "<FIXED_ME>",
  "authDomain": "<FIXED_ME>",
  "projectId": "<FIXED_ME>",
  "storageBucket": "<FIXED_ME>",
  "messagingSenderId": "<FIXED_ME>",
  "appId": "<FIXED_ME>",
  "measurementId": "<FIXED_ME>",
  "databaseURL": "<FIXED_ME>",
  "serviceAccount": "<FIXED_ME>"
}

TYPE_VIDEO = "videos"
TYPE_IMAGE = "images"
TYPE_FOLDER = "folder"
