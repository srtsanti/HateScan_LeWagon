import glob
import os
import time
import pickle
from colorama import Fore, Style
from tensorflow import keras
from google.cloud import storage
from hatescan.params_hatescan import *


def save_model_scale(model: keras.Model = None) -> None:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    # Save model locally
    model_path = os.path.join(LOCAL_REGISTRY1_PATH, f"{timestamp}.h5")
    model.save(model_path)
    
    print("✅ Model saved locally")
    
def save_model_topic(model: keras.Model = None) -> None:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    # Save model locally
    model_path = os.path.join(LOCAL_REGISTRY2_PATH, f"{timestamp}.h5")
    model.save(model_path)
    
    print("✅ Model saved locally")

def load_model_hatescale() -> keras.Model:
    if MODEL_TARGET == "local":
        print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)

        # Get the latest model version name by the timestamp on disk
        local_model_directory = LOCAL_REGISTRY1_PATH
        local_model_paths = glob.glob(f"{local_model_directory}/*")
        if not local_model_paths:
            return None
        most_recent_model_path_on_disk = sorted(local_model_paths)[-1]
        print(Fore.BLUE + f"\nLoad latest model from disk..." + Style.RESET_ALL)
        latest_model = keras.models.load_model(most_recent_model_path_on_disk)
        print("✅ Model loaded from local disk")

        return latest_model
    
def load_model_hatetopic() -> keras.Model:
    if MODEL_TARGET == "local":
        print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)

        # Get the latest model version name by the timestamp on disk
        local_model_directory = LOCAL_REGISTRY2_PATH
        local_model_paths = glob.glob(f"{local_model_directory}/*")
        if not local_model_paths:
            return None
        most_recent_model_path_on_disk = sorted(local_model_paths)[-1]
        print(Fore.BLUE + f"\nLoad latest model from disk..." + Style.RESET_ALL)
        latest_model = keras.models.load_model(most_recent_model_path_on_disk)
        print("✅ Model loaded from local disk")
        
        return latest_model    

    # elif MODEL_TARGET == "gcs":
    #     print(Fore.BLUE + f"\nLoad latest model from GCS..." + Style.RESET_ALL)

    #     client = storage.Client()
    #     blobs = list(client.get_bucket('hate_scan_srtsanti').list_blobs(prefix="model"))
        
    #     try:
    #         latest_blob = max(blobs, key=lambda x: x.updated)
    #         latest_model_path_to_save = os.path.join(LOCAL_REGISTRY_PATH, latest_blob.name)
    #         latest_blob.download_to_filename(latest_model_path_to_save)
    #         latest_model = keras.models.load_model(latest_model_path_to_save)

    #         print("✅ Latest model downloaded from cloud storage")

    #         return latest_model
    #     except:
    #         print(f"\n❌ No model found in GCS bucket {BUCKET_NAME}")

    #         return None
