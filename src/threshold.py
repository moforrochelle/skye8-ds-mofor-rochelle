import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


def find_cost_optimal_threshold(
    y_true,
    probabilities,
    false_positive_cost=500,
    false_negative_cost=5000,
):
    thresholds = np.arange(0.01, 1.00, 0.01)

    results = []

    for threshold in thresholds:
        predictions = (
            probabilities >= threshold
        ).astype(int)

        tn, fp, fn, tp = confusion_matrix(
            y_true,
            predictions,
            labels=[0, 1],
        ).ravel()

        total_cost = (
            fp * false_positive_cost
            + fn * false_negative_cost
        )

        results.append(
            {
                "threshold": threshold,
                "false_positives": fp,
                "false_negatives": fn,
                "true_positives": tp,
                "true_negatives": tn,
                "total_cost_xaf": total_cost,
            }
        )

    results = pd.DataFrame(results)

    best = results.loc[
        results["total_cost_xaf"].idxmin()
    ]

    return best, results