"""
A module for evaluating model performance.
"""

import numpy as np
from typing import Union
from sklearn.metrics import roc_auc_score
from sklearn.metrics import auc, precision_recall_curve
from scipy.stats import ks_2samp


def roc_auc(
    y_true: Union[list, np.array], y_pred_proba: Union[list, np.array]
) -> float:
    """Calculate ROC AUC (Area Under the Receiver Operating Characteristic Curve).

    Parameters
    ----------
    y_true: Union[list, np.array]
        True labels.
        
    y_pred_proba: Union[list, np.array]
        Prediction probability of target class of `1`.
        
    Returns
    -------
    float
        ROC AUC score.

    """
    return roc_auc_score(y_true, y_pred_proba)


def pr_auc(y_true: Union[list, np.array], y_pred_proba: Union[list, np.array]) -> float:
    """Calculate PR AUC (Area Under the Precision Recall Curve).

    Parameters
    ----------
    y_true: Union[list, np.array]
        True labels.
        
    y_pred_proba: Union[list, np.array]
        Prediction probability of target class of `1`.

    Returns
    -------
    float
        PR AUC score.

    """
    precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
    return auc(recall, precision)


def gini(y_true: Union[list, np.array], y_pred_proba: Union[list, np.array]) -> float:
    """Calculate Gini coefficient.

    Parameters
    ----------
    y_true: Union[list, np.array]
        True labels.
        
    y_pred_proba: Union[list, np.array]
        Prediction probability of target class of `1`.

    Returns
    -------
    float
        Gini coefficient.

    """
    return 2 * roc_auc_score(y_true, y_pred_proba) - 1


def ks(y_true: Union[list, np.array], y_pred_proba: Union[list, np.array]) -> float:
    """Calculate Kolmogorov-Smirnov (KS) statistic.

    Parameters
    ----------
    y_true: Union[list, np.array]
        True labels.
        
    y_pred_proba: Union[list, np.array]
        Prediction probability of target class of `1`.

    Returns
    -------
    float
        KS statistic.

    """
    y_pred_proba_not_default = y_pred_proba[y_true == 0]
    y_pred_proba_default = y_pred_proba[y_true == 1]
    ks_stat, _ = ks_2samp(y_pred_proba_not_default, y_pred_proba_default)
    return ks_stat