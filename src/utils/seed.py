"""
Project Avatar: Universal Random Seed Enforcement.
Ensures absolute reproducibility across Python standard library, NumPy, and ML frameworks.
"""

import os
import random
import numpy as np

GLOBAL_SEED: int = 42


def set_seed(seed: int = GLOBAL_SEED) -> int:
    """
    Sets global deterministic seeds across standard libraries and runtime environments.

    Args:
        seed: Universal integer seed (defaults to 42).

    Returns:
        The integer seed applied.
    """
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass

    return seed


# Automatically apply global seed on import
set_seed(GLOBAL_SEED)
