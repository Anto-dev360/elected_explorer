"""
Author : Anthony Morin
Description : Utilities for downloading and caching data files.
"""

import os
import requests

def download_if_not_exists(url: str, output_path: str) -> None:
    """
    Download a file from a URL if it does not already exist locally.

    Parameters :
    url : str
        URL to download the file from.
    output_path : str
        Local path to store the downloaded file.

    Returns :
    None
    """
    if not os.path.exists(output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
        except requests.RequestException as e:
            raise RuntimeError(f"Erreur lors du téléchargement depuis {url} : {e}")
