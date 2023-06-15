import os
import numpy as np

LOCAL_REGISTRY1_PATH = os.environ.get("LOCAL_MODEL1_PATH")
LOCAL_REGISTRY2_PATH = os.environ.get("LOCAL_MODEL2_PATH")
LOCAL_TOKEN1_PATH = os.environ.get("LOCAL_TOKEN1_PATH")
LOCAL_TOKEN2_PATH = os.environ.get("LOCAL_TOKEN2_PATH")

MODEL_TARGET = os.environ.get("MODEL_TARGET")

GCP_PROJECT = os.environ.get("GCP_PROJECT")
GCP_REGION = os.environ.get("GCP_REGION")

GCR_IMAGE = os.environ.get("GCR_IMAGE")
GCR_REGION = os.environ.get("GCR_REGION")
GCR_MEMORY = os.environ.get("GCR_MEMORY")

BUCKET_NAME = os.environ.get("BUCKET_NAME")

BQ_DATASET = os.environ.get("BQ_DATASET")
BQ_TABLE = os.environ.get("BQ_TABLE")

TWITTER_USER_URL = os.environ.get("TWITTER_USER_URL")
X_RapidAPI_Key = os.environ.get("X_RapidAPI_Key")
X_RapidAPI_Host = os.environ.get("X_RapidAPI_Host")
TWITTER_USERTWEET_URL = os.environ.get("TWITTER_USERTWEET_URL")