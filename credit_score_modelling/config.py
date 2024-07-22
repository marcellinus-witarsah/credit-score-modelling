from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from credit_score_modelling.utils import read_yaml

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")


# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass

CONFIG = read_yaml(PROJ_ROOT / "credit_score_modelling/config.yaml")
DATA_PREPROCESSING = CONFIG.date_preprocessing
TRAIN_CONFIG = CONFIG.train
EVALUATE_CONFIG = CONFIG.evaluate
INFERENCE_CONFIG = CONFIG.inference
