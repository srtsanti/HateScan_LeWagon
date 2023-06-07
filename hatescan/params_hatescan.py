import os
import numpy as np

LOCAL_REGISTRY_PATH = os.path.join(os.path.expanduser('~'), ".lewagon", "mlops", "training_outputs")

MODEL_TARGET = os.environ.get("MODEL_TARGET")

GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_REGION = os.environ.get("GCP_REGION")

GCR_IMAGE = os.environ.get("GCR_IMAGE")
GCR_REGION = os.environ.get("GCR_REGION")
GCR_MEMORY = os.environ.get("GCR_MEMORY")

BUCKET_NAME = os.environ.get("BUCKET_NAME")
