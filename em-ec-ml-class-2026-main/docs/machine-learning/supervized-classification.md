# Supervized Classification

A list of supervized classifier implementations from ther `scikit-learn` python library is available [here](https://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html).<br>
A great source for learning supervized classification is the `scikit-learn` [landing page](https://scikit-learn.org/stable/supervised_learning.html).

## Plan

- [1. Evaluation criteria of binary classifiers](#1-evaluation-criteria-of-binary-classifiers)
  - [Binary classification metrics](#binary-classification-metrics)
  - [Precision - Recall curve and threshold selection](#precision---recall-curve-and-threshold-selection)
- [2. Model calibration](#3-model-calibration)
- [3. Ensemble methods](#4-ensemble-methods)
  - [Bagging](#bagging)
  - [Stacking](#stacking)
  - [Boosting](#boosting)
- [4. Non-binary classification](#5-non-binary-classification)
  - [Multiclass classification](#multiclass-classification)
  - [Multilabel classification](#multilabel-classification)
  - [Multiclass/multioutput classification](#multiclassmultioutput-classification)

## 1. Evaluation criteria of binary classifiers

### Binary classification metrics

The default scoring function of a classifier is its *Accuracy*, that is, the percentage of well-predicted classes among an evaluation dataset. This way of evaluating a model can be very misleading when this evaluation dataset is *imbalanced*, in the sense that some classes are over-represented and some other classes are under-represented in the evaluation set.

Take for instance the situation on a binary classification problem where the evaluation set consists of 90% of data points belonging tho the class $0$ whereas the remaining 10% belong to the class $1$. Then the trivial classifier constantly predicting the class $0$ will achieve 90% accuracy on this evaluation set !

In order to get a better estimation of the quality of a binary classifier, we consider a total of 6 different scores :

- Accuracy
- Recall
- Precision
- Specificity
- False Positive Rate
- F1-score

<img src="../docs/imgs/notebooks/precision_recall_specificity.bmp" alt="" style="width: 50%"/>

The 6 metrics for binary classification

- *Accuracy* =  percentage of `predicted = true` among all.
- *Recall* =  percentage of `predicted = 1` _among_ `true = 1`.
- *Precision* =  percentage of `true = 1` _among_ `predicted = 1`.
- *Specificity* =  percentage of `true = 0` _among_ `predicted = 0`.
- *False Positive Rate* =  percentage of `true = 1` _among_ `predicted = 0`.
- *F1-score*: harmonic mean between recall and precision.

$$\text{Accuracy} = \frac{TP+TN}{TP+TN+FP+FN} $$

**Accuracy** is the default scoring metric for a classifier. It is very simple and **intuitive**, as it measure the % of correct predictions. But it can be very **misleading** in case of unbalanced datasets.

$$\text{Recall} = \frac{TP}{TP+FN}$$

**Recall** measures the **coverage** of the model : among all the relevant instances, how many did my model predict correctly ? Recall is important when you don't want to miss any important instance in your predictions. Example : medical diagnosis, fraud detection, machine failure.

$$\text{Precision} = \frac{TP}{TP+FP}$$

*Precision** measures the **reliability** of the model : among all the positive predictions, how many are actually relevant ? Precision is important when you want to focus only on relevant instances in your predictions. Example : recommandation system.

$$\text{FPR} = \frac{FP}{TN+FN}$$

*False Positive Rate** measures, among all the irrelevant instances, the proportion of positive predictions.

$$\text{F}_1\text{-score} = 2. \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

**F1-score** is the harmonic mean between recall and precision, it is a trade-off between both quantities. It is quite **non-intuitive** metric but it encompasses a lot of information and is robust in case of unbalanced datasets, hence it is **widely used** by data scientists.

[Back to plan](#plan)

### Precision - Recall curve and threshold selection

[Back to plan](#plan)

## 3. Model calibration

See [model calibration](https://scikit-learn.org/stable/modules/calibration.html#calibrating-a-classifier).

[Back to plan](#plan)

## 4. Ensemble methods

### Bagging

See [Bagging](https://scikit-learn.org/stable/modules/ensemble.html#bagging-meta-estimator).

Bagging is the reduction of __B__oostrap __Agg__regation. It consists in fitting several instances of a base model on:

- random subsets of the original training set (sampled with replacement)
- random subsets of the list of features (with possible sampling with replacement)

It then aggregate the individual predictions by averaging the predicted regression value or classification probabilities, to form a final prediction.

Bagging reduces _variance_ of the base model, and as such it works best by using very capable base models that overfits: bagging retains the model's capability, while it reduces overfitting, thus making it more robust to noise.<br>
By contrast, the boosting approach enhances a weak, non-overfitting base model.

### Stacking

See [Stacking](https://scikit-learn.org/stable/modules/ensemble.html#stacked-generalization), and the simple [case study](https://scikit-learn.org/stable/auto_examples/ensemble/plot_stack_predictors.html#sphx-glr-auto-examples-ensemble-plot-stack-predictors-py).

Stacking consists in combining different base models by giving their individual predictions to a final estimator to compute the final prediction. 

- In [voting](https://scikit-learn.org/stable/modules/ensemble.html#voting-classifier), final prediction is computed based on rules that are independent from the point data point.
- In stacking, final decision depends on the imput data point, through a final estimator that was trained using cross-validation.

Stacking (and also voting) combines different models to _reduce their biases_. It can outperform each individual base model when the base models errors are only partially correlated, allowing the combination to reduce individual bias/variance.

### Boosting

See:

- [Adaboost](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html#sklearn.ensemble.AdaBoostClassifier)
- [Gradient boosting](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier)
- [Histogram gradient boosting](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingClassifier.html#sklearn.ensemble.HistGradientBoostingClassifier)

[Back to plan](#plan)

## 5. Non-binary classification

### Multiclass classification

See [mutliclass classification](https://scikit-learn.org/stable/modules/multiclass.html#multiclass-classification).

### Multilabel classification

See [multilabel classification](https://scikit-learn.org/stable/modules/multiclass.html#multilabel-classification).

### Multiclass/multioutput classification

See [multiclass/multioutput classification](https://scikit-learn.org/stable/modules/multiclass.html#multiclass-multioutput-classification).

[Back to plan](#plan)
