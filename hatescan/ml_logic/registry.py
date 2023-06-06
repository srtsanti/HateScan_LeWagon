import glob
import os
import time
import pickle

from colorama import Fore, Style
from tensorflow import keras
from google.cloud import storage

import mlflow
from mlflow.tracking import MlflowClient



def save_model(model: keras.Model = None) -> None:
    """
    Persist trained model locally on the hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
    - if MODEL_TARGET='gcs', also persist it in your bucket on GCS at "models/{timestamp}.h5" --> unit 02 only
    - if MODEL_TARGET='mlflow', also persist it on MLflow instead of GCS (for unit 0703 only) --> unit 03 only
    """
    LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".lewagon", "mlops", "training_outputs")
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Save model locally
    model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", f"{timestamp}.h5")
    model.save(model_path)
    
    return None


def load_model() -> keras.Model:
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only
    - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow' --> for unit 03 only

    Return None (but do not Raise) if no model is found

    """
    print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)
    LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".lewagon", "mlops", "training_outputs")
    # Get the latest model version name by the timestamp on disk
    local_model_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")
    local_model_paths = glob.glob(f"{local_model_directory}/*")

    if not local_model_paths:
        return None

    most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

    print(Fore.BLUE + f"\nLoad latest model from disk..." + Style.RESET_ALL)

    latest_model = keras.models.load_model(most_recent_model_path_on_disk)

    print("✅ Model loaded from local disk")

    return latest_model
   
    