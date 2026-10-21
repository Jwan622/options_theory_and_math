# Correlation and Independence

## Learning Goal

Correlation measures one specific kind of co-movement: linear co-movement on a -1 to 1 scale. Independence is a stronger idea: knowing X tells you nothing about Y. The goal of this lesson is to understand the correlation formula, and to see why "correlation is zero" does **not** mean "the two variables are independent."

This matters on a desk because risk tools often lean on correlation. Zero correlation can still hide dependence that shows up in options, hedges, or stress days.

---

## The problem

Covariance already tells you whether two series tend to move together, but its size depends on each series' own volatility. A pair of wild names can have a huge covariance just because both swing a lot. A pair of quiet names can have a tiny covariance even if they move in lockstep.

You want a number that answers: how tightly do these two line up, after scaling out each one's own size? That number is correlation.

A second problem sits next to it. People often treat "uncorrelated" as if it meant "unrelated" or "independent." Those are not the same. Correlation can miss relationships that are real but not linear.

---

## Intuition: what correlation is

Start from covariance:

```text
Cov(X, Y) = E[(X - mu_X)(Y - mu_Y)]
```

That is the average product of gaps from each mean. Correlation divides by the two standard deviations:

```text
Corr(X, Y) = Cov(X, Y) / (SD(X) * SD(Y))
```

where `SD(X) = sqrt(Var(X))`.

What this does:

- If X and Y usually sit on the same side of their means, Cov is positive, so Corr is positive.
- If they usually sit on opposite sides, Corr is negative.
- Dividing by the two SDs puts the answer on a fixed scale from -1 to 1.

Mental model: correlation asks how well a straight-line relationship describes the co-movement. It is a scaled covariance, not a full description of every possible link between X and Y.

```text
raw co-movement (Cov)
        |
        v
divide out each series' own volatility
        |
        v
Corr between -1 and 1
```

---

## Example: computing correlation

Five days of returns:

```text
day:     1    2    3    4    5
A:       1   -1    2   -2    0
B:       2   -1    3   -3    1
```

### Step 1: covariance formula

```text
Cov(A, B) = E[(A - mean_A)(B - mean_B)]
          = (1/n) * sum over days of (A_t - mean_A) * (B_t - mean_B)
```

`E[...]` means average over all the observations here — all 5 days. It is not one day. You form the product of gaps on each day, then average those 5 products.

With the numbers from this example (`n = 5`, `mean_A = 0`, `mean_B = 0.4`):

```text
Cov(A, B)
  = (1/5) * [
        (1 - 0)(2 - 0.4)
      + (-1 - 0)(-1 - 0.4)
      + (2 - 0)(3 - 0.4)
      + (-2 - 0)(-3 - 0.4)
      + (0 - 0)(1 - 0.4)
    ]
  = (1/5) * [ (1)(1.6) + (-1)(-1.4) + (2)(2.6) + (-2)(-3.4) + (0)(0.6) ]
  = (1/5) * [ 1.6 + 1.4 + 5.2 + 6.8 + 0 ]
  = (1/5) * 15
  = 3
```

So the formula comes out to `Cov(A, B) = 3`. Same steps below, written out one piece at a time.

### Step 2: means

```text
mean_A = (1 + (-1) + 2 + (-2) + 0) / 5 = 0 / 5 = 0
mean_B = (2 + (-1) + 3 + (-3) + 1) / 5 = 2 / 5 = 0.4
```

### Step 3: demean

```text
A - mean_A = [1-0, -1-0, 2-0, -2-0, 0-0] = [1, -1, 2, -2, 0]
B - mean_B = [2-0.4, -1-0.4, 3-0.4, -3-0.4, 1-0.4]
           = [1.6, -1.4, 2.6, -3.4, 0.6]
```

### Step 4: multiply gaps, then average

```text
day1:  1 * 1.6  =  1.6
day2: -1 * -1.4 =  1.4
day3:  2 * 2.6  =  5.2
day4: -2 * -3.4 =  6.8
day5:  0 * 0.6  =  0.0
                     ----
sum                  15.0

Cov(A, B) = 15.0 / 5 = 3.0
```

### Step 5: variances and standard deviations

```text
Var(A) = (1^2 + (-1)^2 + 2^2 + (-2)^2 + 0^2) / 5
       = (1 + 1 + 4 + 4 + 0) / 5
       = 10 / 5 = 2

Var(B) = (1.6^2 + (-1.4)^2 + 2.6^2 + (-3.4)^2 + 0.6^2) / 5
       = (2.56 + 1.96 + 6.76 + 11.56 + 0.36) / 5
       = 23.2 / 5 = 4.64

SD(A) = sqrt(2)    ≈ 1.414
SD(B) = sqrt(4.64) ≈ 2.154
```

### Step 6: correlation

```text
Corr(A, B) = Cov(A, B) / (SD(A) * SD(B))
           = 3.0 / (1.414 * 2.154)
           ≈ 3.0 / 3.045
           ≈ 0.985
```

So A and B are strongly positively correlated in this sample: almost a straight-line same-direction relationship after scaling.

---

## Independence is a different idea

Two random variables are **independent** if learning the value of one gives no information about the other.

In plain terms: the joint behavior factors into separate behaviors. Knowing X does not change what you should expect for Y.

Correlation is weaker. It only tracks average linear co-movement of gaps from the means. So:

```text
independent  =>  correlation is zero
                  (under ordinary finite-variance conditions)

correlation zero  =/>  independent
```

Zero correlation means: the average product of demeaned values is zero. It does **not** mean there is no relationship of any kind.

---

## Why zero correlation is not independence

Correlation multiplies gaps and averages them. Relationships that are symmetric in a special way can cancel in that average even though Y still depends on X.

Classic pattern: Y is a function of X, but when X is high, Y's gap and X's gap do not keep a stable linear sign. Positive products and negative products cancel, so Corr ≈ 0, while Y is still completely determined by X.

```text
X large positive  ->  product of gaps one sign
X large negative  ->  product of gaps opposite sign
average product   ->  near zero
but Y still depends on X
```

That is the trap: correlation asks about a straight-line link. Dependence can be curved, U-shaped, clustered, or conditional on regimes.

---

## Example: Corr = 0, but not independent

Let X take three values with equal probability:

```text
X:  -2,  0,  2     each with probability 1/3
```

Define Y by a rule that depends entirely on X:

```text
Y = X^2
```

So the three equally likely outcomes are:

```text
X    Y = X^2
-2    4
 0    0
 2    4
```

Y is not free of X. If you know X = 0, you know Y = 0. If you know |X| = 2, you know Y = 4. They are dependent.

Now check correlation.

Means:

```text
E[X] = (-2 + 0 + 2) / 3 = 0
E[Y] = (4 + 0 + 4) / 3 = 8/3 ≈ 2.667
```

Gaps and products:

```text
outcome   X-mu_X   Y-mu_Y              product
-2,4      -2       4 - 8/3 = 4/3       (-2)*(4/3) = -8/3
 0,0       0       0 - 8/3 = -8/3       (0)*(-8/3) = 0
 2,4       2       4 - 8/3 = 4/3        (2)*(4/3) =  8/3
```

Average product:

```text
Cov(X, Y) = [ (-8/3) + 0 + (8/3) ] / 3 = 0 / 3 = 0
```

So:

```text
Corr(X, Y) = 0 / (SD(X) * SD(Y)) = 0
```

Correlation is exactly zero. Independence fails completely: Y is a deterministic function of X.

Picture of why the cancel happens:

```text
X = -2  (left)     X = 0      X = +2 (right)
Y = 4              Y = 0      Y = 4

U-shape: Y large when |X| is large.
Left side: X below mean, Y above mean  -> negative product
Right side: X above mean, Y above mean -> positive product
Those cancel in the average -> Cov = 0
```

**Common mistake:** "Corr = 0, so X and Y are unrelated."

**Why it is tempting:** in many Gaussian / linear settings, zero correlation and independence coincide, so the shortcut often works in classroom examples.

**Correct mental model:** correlation is a linear summary. Dependence is about information. Zero correlation only says the linear summary is zero.

---

## Desk intuition

A hedge sized off correlation assumes the main co-movement looks roughly linear in the returns you measured. That can be fine day to day.

It can fail when the real link is nonlinear or regime-dependent: vol-of-vol, options, "both names blow up together in a crash even though quiet-day correlation was low," or a factor that maps into a U-shaped residual. You can print Corr ≈ 0 in a calm sample and still be tightly linked in the way that hurts P&L.

So:

- Use correlation as a scaled linear co-movement number.
- Do not treat "uncorrelated" as a synonym for "safe to ignore joint risk."

---

## Formulas

```text
Corr(X, Y) = Cov(X, Y) / (SD(X) * SD(Y))

Cov(X, Y) = E[(X - mu_X)(Y - mu_Y)]
SD(X)     = sqrt(Var(X))
```

Also written with the shortcut covariance:

```text
Corr(X, Y) = (E[XY] - E[X]E[Y]) / (SD(X) * SD(Y))
```

Bounds:

```text
-1 <= Corr(X, Y) <= 1
```

Useful links:

```text
Corr(X, X) = 1
independent (with finite variance)  =>  Corr = 0
Corr = 0  does not imply  independent
```

---

## Recap

Correlation is covariance divided by the two standard deviations, so co-movement is measured on a -1 to 1 scale after removing each series' own volatility. It tracks linear co-movement of gaps from the means. Independence means knowing one variable gives no information about the other. Independent variables are uncorrelated (under standard conditions), but uncorrelated variables need not be independent, because nonlinear links can cancel in the average product of gaps. The example Y = X^2 with symmetric X has Corr = 0 even though Y is fully determined by X.

## Vocabulary

- **Correlation:** scaled covariance; linear co-movement on a -1 to 1 scale.
- **Independence:** knowing X gives no information about Y.
- **Uncorrelated:** correlation is zero; the average product of demeaned values is zero.
- **Nonlinear dependence:** a real link between X and Y that is not a straight-line co-movement of gaps (for example Y = X^2).
- **Standard deviation (SD):** square root of variance; used to scale covariance into correlation.

## Checks

1. What does dividing covariance by `SD(X) * SD(Y)` buy you?
2. In the `Y = X^2` example, why is correlation zero even though Y depends on X?
3. Does zero correlation mean a hedge has no joint risk left?

### Answers

1. It removes each series' own volatility so co-movement is comparable on a -1 to 1 scale.
2. The left-side and right-side products of gaps cancel, so the average product is zero, while Y is still a function of X.
3. No. Zero correlation only kills average linear co-movement; nonlinear or regime dependence can remain.
