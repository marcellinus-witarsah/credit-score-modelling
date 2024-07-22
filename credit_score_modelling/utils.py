import os
import sys
import yaml
import json
import logging
import joblib
import pickle

from typing import Any
from pathlib import Path
from box import ConfigBox
from ensure import ensure_annotations
from typing import Any, Union
from box.exceptions import BoxValueError


# For Logging
logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging_directory = "logs"
os.makedirs(logging_directory, exist_ok=True)
log_filepath = os.path.join(logging_directory, "running_logs.log")

logging.basicConfig(
    level=logging.INFO,  # set minimum log level to respond
    format=logging_format,  # set the log output format
    handlers=[
        logging.FileHandler(log_filepath),  # set file to write the log messages
        logging.StreamHandler(sys.stdout),  # send log messages to the system output
    ],
)  # set logging configuration

logger = logging.getLogger("credit-score-modelling-logger")  # get logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Read YAML file and return its value.

    Parameters
    ----------
    path_to_yaml: Path
        File location.
        

    Returns
    -------
    ConfigBox
        Value inside YAML file and wrapped with ConfigBox.

    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose: bool=True) -> None:
    """Create directories.

    Parameters
    ----------
    path_to_directories: list :
        List of file directories to be created.
    verbose: bool, default=True
        Show informational messages when directories are created.


    Returns
    -------

    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict) -> None:
    """Load data into JSON format.

    Parameters
    ----------
    path: Path
        Destination file to store the data.
    data: dict
        Data being saved.

    Returns
    -------

    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"JSON file saved at: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load .json file.

    Parameters
    ----------
    path: Path
        File location.

    Returns
    -------
    ConfigBox
        Content inside the .json file.

    """
    with open(path) as f:
        content = json.load(f)

    logger.info(f"JSON file loaded successfully from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path) -> None:
    """Save to into binary format using joblib library.

    Parameters
    ----------
    data: Any
        Data being saved.
    path: Path
        Destination file to store the data.
        

    Returns
    -------

    """
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load binary data using joblib library.

    Parameters
    ----------
    path: Path
        File location.
        

    Returns
    -------

    """
    data = joblib.load(path)
    logger.info(f"Binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """Get file size.

    Parameters
    ----------
    path: Path
        File location.
        

    Returns
    -------
    str
        Size of the file in KiloBytes.

    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


@ensure_annotations
def load_pickle(path: Union[str, Path], mode: str) -> Any:
    """Load pickle file.

    Parameters
    ----------
    path: Union[str, Path]
        File source of the data/ object.
    mode: str
        Read mode.
        

    Returns
    -------

    """
    with open(path, mode) as f:
        data = pickle.load(f)
    logger.info(f"Pickle file loaded from: {path}")
    return data


@ensure_annotations
def save_pickle(data, path: Union[Path, str], mode:str) -> None:
    """Save data into .pkl file.

    Parameters
    ----------
    data :
        Data being saved.
    path : Union[Path, str]
        Destination file to store the data.
    mode : str
        Write mode.
        
        
    Returns
    -------

    """
    with open(path, mode) as f:
        pickle.dump(data, f)
    logger.info(f"Pickle file saved at: {path}")