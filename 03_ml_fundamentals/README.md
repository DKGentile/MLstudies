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

## Working method

For each loss function, do these in order:

1. Write its scalar definition on paper, including where the batch average and
   regularization coefficient appear.
2. Annotate every intermediate with its shape.
3. Derive the gradient without code.
4. Implement the forward value first.
5. Implement the analytic gradient and compare it with finite differences.
6. Only then add the optimization loop.

Useful references from the source curriculum:

- [CS229 course materials](https://cs229.stanford.edu/)
- [CS231n Python/NumPy tutorial](https://cs231n.github.io/python-numpy-tutorial/)
- [CS231n optimization notes](https://cs231n.github.io/optimization-1/)
- [CS231n neural-network notes](https://cs231n.github.io/neural-networks-case-study/)

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
