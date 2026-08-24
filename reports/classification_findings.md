# Classification Findings

## Overview

The objective of this analysis was to predict whether an appointment would result in a patient not attending. Four classification models were trained and evaluated on the same train-test split: Logistic Regression, Decision Tree, K-Nearest Neighbours, and Naive Bayes.

Because no-shows are the minority class, accuracy alone was not considered sufficient for selecting a model. Precision, recall, F1 score, and especially Precision-Recall AUC were also considered.

## Comparing the four classifiers

| Model | Accuracy | Precision | Recall | F1 | PR-AUC |
|---|---:|---:|---:|---:|---:|
| Majority Baseline | 0.822777 | 0.000000 | 0.000000 | 0.000000 | N/A |
| Logistic Regression | 0.826172 | 0.573034 | 0.075166 | 0.132899 | 0.342678 |
| Decision Tree | 0.719734 | 0.229609 | 0.246868 | 0.237926 | 0.190308 |
| K-Nearest Neighbours | 0.808933 | 0.371981 | 0.113486 | 0.173913 | 0.230423 |
| Naive Bayes | 0.812720 | 0.439938 | 0.207811 | 0.282282 | 0.321322 |

The majority-class baseline is useful for putting these results into perspective. It achieves 82.28% accuracy simply by predicting that every appointment will be attended, but its recall for no-shows is 0%. This shows why accuracy by itself can be misleading when the class we care about is relatively uncommon.

Logistic Regression achieved the highest PR-AUC of the four models at 0.342678. Naive Bayes and the Decision Tree identified more of the actual no-shows at the default threshold, but Logistic Regression provided the strongest overall precision-recall ranking performance. It was therefore selected for the threshold optimisation stage.

## ROC and Precision-Recall curves

ROC and Precision-Recall curves were generated for all four classifiers using the same test set.

For this problem, the Precision-Recall curve is the more useful one to present to the district. The reason is that the no-show class is the minority class and the practical decision is whether an appointment should receive a reminder.

The Precision-Recall curve makes it easier to see the trade-off between catching more genuine no-shows and generating unnecessary reminder calls. The ROC curve is still useful for model evaluation, but Precision-Recall provides a more direct view of the operational trade-off.

## Choosing a practical threshold

The default classification threshold of 0.50 is not necessarily the best choice for this problem. A lower threshold can identify more patients who are likely to miss their appointments, although this also increases the number of unnecessary reminders.

To make the threshold decision more realistic, an operational cost was assigned to each type of classification error.

A false positive, where a reminder is sent to a patient who would have attended anyway, was assigned a cost of **XAF 500**. A false negative, where the model fails to identify a patient who subsequently does not attend, was assigned a cost of **XAF 5,000**.

These figures are project operational assumptions rather than published district prices. The assumption is that a missed no-show is considerably more costly than an unnecessary reminder.

The false-negative cost is:

**5,000 / 500 = 10 times**

the false-positive cost.

The total expected cost was calculated as:

**Total cost = (false positives × 500) + (false negatives × 5,000)**

Testing thresholds from 0.01 to 0.99 showed that the lowest calculated cost occurred at a threshold of **0.11**.

At this threshold, the Logistic Regression model produced:

- False positives: **4,706**
- False negatives: **150**
- True positives: **1,207**
- True negatives: **1,594**

The resulting cost is:

**(4,706 × 500) + (150 × 5,000)**

**= 2,353,000 + 750,000**

**= XAF 3,103,000**

The recommended threshold is therefore **0.11**.

Compared with the conventional threshold of 0.50:

**|0.11 - 0.50| = 0.39**

The selected threshold is therefore **0.39 below** the default threshold.

## What this threshold means operationally

A threshold is not just a model setting in this project; it determines how many patients would actually receive reminders.

At the recommended threshold of 0.11, the model would generate:

**4,706 false-positive reminders + 1,207 true-positive reminders = 5,913 reminder calls**

The test data covers approximately **100.71 weeks**.

Therefore:

**5,913 / 100.71 = 58.71 calls per week**

The recommended approach would therefore generate approximately **59 reminder calls per week**.

This workload should be considered alongside the cost reduction provided by identifying likely no-shows. In practice, the district could also review these assumptions with actual operational costs before deploying the model.

## Probability calibration

Because the model outputs probabilities, calibration was also examined. A calibration curve was produced before and after applying Platt scaling.

The Brier score before calibration was:

**0.1354100482**

After Platt scaling, the Brier score was:

**0.1358687577**

The change was:

**0.1358687577 - 0.1354100482 = +0.0004587095**

Since a lower Brier score represents better calibration, the positive change indicates that Platt scaling slightly worsened the Brier score in this evaluation.

The change is small, so calibration does not alter the model or threshold recommendation. The operational threshold remains based on the cost analysis.

## Final recommendation

Based on the comparison of the four classifiers, **Logistic Regression** is recommended for the no-show prediction task. It achieved the highest PR-AUC at **0.342678**, making it the strongest model for ranking appointments by their likelihood of no-showing among the models tested.

A classification threshold of **0.11** is recommended instead of the default 0.50 threshold. Under the stated cost assumptions, this threshold produced the lowest calculated operational cost of **XAF 3,103,000** on the test set.

The threshold would result in approximately **59 reminder calls per week**.

The recommendation should be treated as an analytical starting point rather than a fixed operational rule. Before deployment, the district should validate the assumed costs of unnecessary reminders and missed no-shows against its actual operating costs.