# Chapter 3: ML Fundamentals from Scratch

This chapter turns the CS229/CS231n topics in the curriculum into small,
test-driven NumPy exercises. The point is not to build a framework. It is to
make every tensor shape, loss term, and gradient concrete before PyTorch hides
the bookkeeping.

## Outcomes

By the end of this chapter, you should be able to:

- reshape, broadcast, index, and normalize arrays without accidental copies or
  Python loops;
- fit linear and binary logistic regression with gradient descent;
- compare an analytic gradient with a finite-difference estimate;
- explain what L2 regularization changes and recognize under/overfitting;
- implement the forward and backward passes of a two-layer classifier; and
- diagnose a failed optimization run from loss history and gradient checks.

## Setup

Use an isolated environment. NumPy and pytest are the only dependencies.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r 03_ml_fundamentals/requirements.txt
python -m pytest 03_ml_fundamentals/tests
```

The last command is a scaffold smoke test. Challenge tests are skipped until
you explicitly enable them. This keeps the repository green while preserving
a test-first workflow.

To work an exercise in PowerShell:

```powershell
$env:RUN_ML_EXERCISES = "1"
python -m pytest 03_ml_fundamentals/tests/test_numpy_fluency.py -q
```

On bash/zsh, use `RUN_ML_EXERCISES=1 python -m pytest ...`. A failing challenge
test is the starting line, not a broken setup. Implement one function at a
time, rerun the smallest relevant test, then run the whole chapter.

## Route through the chapter

| Stop | Starter file | What to build | Suggested time |
|---|---|---|---:|
| 1 | `ml_fundamentals/numpy_fluency.py` | Standardization, indexed lookup, stable softmax, rolling windows | 2-3 h |
| 2 | `ml_fundamentals/linear_regression.py` | MSE loss/gradient and a gradient-descent loop | 2-3 h |
| 3 | `ml_fundamentals/logistic_regression.py` | Stable sigmoid/BCE, logistic gradient, classifier training | 3-4 h |
| 4 | `ml_fundamentals/gradient_checks.py` | Central differences and reusable gradient checks | 2 h |
| 5 | `ml_fundamentals/regularization.py` | Ridge gradients, polynomial features, bias/variance measurements | 3-4 h |
| 6 | `ml_fundamentals/two_layer_net.py` | Affine-ReLU-affine forward pass and full backprop | 5-8 h |

The tests define edge cases and shape contracts, but they intentionally do not
show implementations. Search each starter file for `TODO`.

## Preparation at the point of use

Do not read this table front to back. **Core before coding** is the minimum
conceptual preparation for that stop. **Extension after first attempt** is for
checking your mental model after you have written a derivation or produced a
specific failing test. External examples explain concepts; the local docstrings
and tests remain the implementation contract.

| Stop | Core before coding | Ready-to-code check | Extension after first attempt |
|---:|---|---|---|
| 1 | NumPy's [broadcasting rules](https://numpy.org/doc/stable/user/basics.broadcasting.html) and [indexing rules](https://numpy.org/doc/stable/user/basics.indexing.html) | For an `(n, d)` matrix, predict the shapes of column means and standard deviations. State when indexing returns a view versus a copy. | Read the official [`sliding_window_view` contract](https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.sliding_window_view.html), then explain why this exercise must return an independent writable array. |
| 2 | The linear-regression chapter of Stanford's [CS229 notes](https://cs229.stanford.edu/main_notes.pdf) | Write the scalar and matrix forms of `0.5 * mean((Xw - y)^2)`, annotate every shape, and derive the gradient before opening the starter. | Use the [CS231n optimization note](https://cs231n.github.io/optimization-1/) to diagnose learning-rate or loss-history behavior, not to replace your derivation. |
| 3 | The classification and logistic-regression chapter of the same [CS229 notes](https://cs229.stanford.edu/main_notes.pdf) | Explain the Bernoulli model behind binary cross-entropy, derive the batch gradient, and identify where naive exponentials or logarithms can overflow. | Compare your explanation with Google's official [logistic-regression module](https://developers.google.com/machine-learning/crash-course/logistic-regression) after your first implementation. |
| 4 | CS231n's [gradient-checking guidance](https://cs231n.github.io/neural-networks-3/#gradcheck) | Write the central-difference formula and explain why absolute error alone is misleading near different gradient scales. | Deliberately omit a batch average or flip a sign, then predict how the relative error should change before running the failure clinic. |
| 5 | CS231n's [regularization discussion](https://cs231n.github.io/neural-networks-2/) and Google's [train/validation/test split lesson](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets) | Explain why an intercept is normally excluded from L2, distinguish bias from variance, and state why model choices must not be made on the test set. | Run the polynomial resampling lab, then revisit the readings to account for the observed coefficient magnitudes and train/validation gap. |
| 6 | CS231n's [backpropagation note](https://cs231n.github.io/optimization-2/) and [two-layer case study](https://cs231n.github.io/neural-networks-case-study/) | Annotate the shapes of both affine layers, list the values needed by backward, and derive the ReLU mask and softmax-logit gradient. | After local gradient checks pass, compare the design with Stanford's [official Assignment 1](https://cs231n.github.io/assignments2026/assignment1/) without copying implementations between them. |

For each row, close the source and answer the ready-to-code check in your own
notes. Then enable only the smallest relevant test. Return to the extension only
when you have a concrete result to explain: a failed assertion, a gradient
mismatch, or a loss curve.

## Working method

For each loss function, do these in order:

1. Write its scalar definition on paper, including where the batch average and
   regularization coefficient appear.
2. Annotate every intermediate with its shape.
3. Derive the gradient without code.
4. Implement the forward value first.
5. Implement the analytic gradient and compare it with finite differences.
6. Only then add the optimization loop.

## Labs and reflection prompts

### Lab A: linear versus logistic objectives

Create the same two-cluster synthetic dataset for both models. Plot or print
the first and last five loss values. Explain why treating binary labels as a
linear-regression target is a different probabilistic claim from logistic
regression, even if both happen to classify the tiny dataset.

### Lab B: gradient-check failure clinic

After your logistic gradient passes, introduce one bug at a time in a temporary
copy: omit the batch average, flip a sign, and regularize the bias. Record how
the relative error changes. Restore the correct implementation afterward.

### Lab C: bias, variance, and regularization

Fit polynomial models of degrees 1, 3, 8, and 14 to several resamples of a
small noisy dataset. Compare training error, validation error, squared bias,
and variance for at least three ridge strengths. Answer:

- Which model underfit?
- Which model was most sensitive to the sampled training points?
- Did a lower training loss imply a lower validation loss?
- What did regularization do to coefficient magnitudes?

### Lab D: tiny neural net

Overfit a dataset of five examples before training on a larger dataset. This is
a debugging test: if a network cannot memorize five examples, inspect shapes,
the ReLU mask, label indexing, and gradient signs before tuning anything.

## Completion gate

You are done when all opt-in tests pass and you can answer these without notes:

- Why does subtracting the largest logit improve numerical stability?
- What exactly is compared in a finite-difference gradient check?
- Why is the intercept usually excluded from L2 regularization?
- How can training loss fall while validation loss rises?
- Which cached values are required to backpropagate through ReLU?

Do not copy an implementation from a solution repository. If stuck, reduce the
problem to a single example and print shapes before looking for more code.
