from pathlib import Path
import sys

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = root_path.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
IMAGE_URL = 'Image from URL' 
VIDEO = 'Video'
WEBCAM = 'Webcam'
YOUTUBE = 'YouTube'

SOURCES_LIST = [IMAGE, IMAGE_URL, VIDEO, WEBCAM, YOUTUBE]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'g2.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'g2_detected.jpg'

# URL config

# Videos config
VIDEO_DIR = ROOT / 'videos'
VIDEO_1_PATH = VIDEO_DIR / 'video_1.mp4'
VIDEOS_DICT = {
    'Select Video': VIDEO_1_PATH,
}

# ML Model config
MODEL_DIR = ROOT / 'weights'
DETECTION_MODEL = MODEL_DIR / 'bestV5.pt'
SEGMENTATION_MODEL = MODEL_DIR / 'yolov8n.pt'

# ML Model config
MODEL_DIR = ROOT / 'weights'
Root_Category = MODEL_DIR / 'bestV5.pt'
Subcategory = MODEL_DIR / 'bestV5.pt'
Sub_Subcategory = MODEL_DIR / 'bestV5.pt'
SEGMENTATION_MODEL = MODEL_DIR / 'yolov8n.pt'

# Webcam
WEBCAM_PATH = 0