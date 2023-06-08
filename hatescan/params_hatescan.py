import os
import numpy as np

LOCAL_REGISTRY1_PATH = os.environ.get("LOCAL_MODEL1_PATH")
LOCAL_REGISTRY2_PATH = os.environ.get("LOCAL_MODEL2_PATH")
LOCAL_TOKEN_PATH = os.environ.get("LOCAL_TOKEN_PATH")

MODEL_TARGET = os.environ.get("MODEL_TARGET")

GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_REGION = os.environ.get("GCP_REGION")

GCR_IMAGE = os.environ.get("GCR_IMAGE")
GCR_REGION = os.environ.get("GCR_REGION")
GCR_MEMORY = os.environ.get("GCR_MEMORY")

BUCKET_NAME = os.environ.get("BUCKET_NAME")
