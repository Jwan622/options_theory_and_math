# Variance and Covariance

## Learning Goal

Variance tells you how much one thing moves around its average. Covariance tells you whether two things tend to move together, and in which direction. On a desk, these are the building blocks behind portfolio risk, hedging, and correlation.

---

# Variance

## The problem

A stock can average 0% daily return whether it usually moves 0.2% or 3%. The average alone is not risk. Variance answers: how far do outcomes typically sit from the mean?

## Intuition

Variance summarizes scatter around the mean. Large swings raise variance; values near the mean keep it small. Squaring makes +3% and -3% count the same: only size matters, not direction.

## Example

```text
r = [1, -1, 2, -2, 0]
mean = (1 - 1 + 2 - 2 + 0) / 5 = 0

squared gaps from mean: 1, 1, 4, 4, 0
Var = (1 + 1 + 4 + 4 + 0) / 5 = 2
SD  = sqrt(2) ≈ 1.41%
```

Standard deviation is the square root of variance. It is in the same units as returns, so people often quote it as "volatility." Variance is still what shows up inside most risk formulas.

## Formulas

`E[...]` means **average**. So `E[X]` is the mean of X. People also write that mean as `mu`.

```text
Var(X) = E[(X - mu)^2]
```

That says: for each outcome, subtract the mean, square the gap, then average those squared gaps. One formula, many outcomes inside the average, one variance number out.

Same idea with raw data `x_1, ..., x_n`. First the sample average:

```text
x_bar = (x_1 + ... + x_n) / n
```

Then sample variance (usual textbook version):

```text
s^2 = [ (x_1 - x_bar)^2 + ... + (x_n - x_bar)^2 ] / (n - 1)
```

Dividing by `n - 1` instead of `n` is a convention when the mean was estimated from the sample. Same squared gaps as above; only the divisor changes. For `[1,-1,2,-2,0]`:

```text
s^2 = 10 / 4 = 2.5    (divide by n-1)
Var = 10 / 5 = 2      (divide by n)
```

## What can go wrong

Variance is in squared units (percent-squared if returns are in percent). It also ignores skew and crash risk: two series can share a variance and still feel very different to trade.

---

# Covariance

## The problem

Trading usually involves more than one series: a stock and a hedge, a basket and an index. The question is: when A moves up, does B tend to move with it, against it, or independently?

## Intuition

Each day, measure how far A is from its mean and how far B is from its mean. Multiply those two gaps.

- Both above mean, or both below -> product positive (same direction)
- One above, one below -> product negative (opposite direction)

Average those products. That average is covariance.

```text
same-direction days          opposite-direction days
A high, B high  -> +         A high, B low  -> -
A low,  B low   -> +         A low,  B high -> -

average of these products = covariance
```

## Example, step by step

Data:

```text
day:     1    2    3    4    5
A:       1   -1    2   -2    0
B:       2   -1    3   -3    1
```

**Step 1 — means**

```text
mean_A = (1 - 1 + 2 - 2 + 0) / 5 = 0
mean_B = (2 - 1 + 3 - 3 + 1) / 5 = 0.4
```

**Step 2 — demean** (subtract each mean; "demean" = turn raw values into gaps from average)

```text
A - mean_A = [1, -1, 2, -2, 0]
B - mean_B = [1.6, -1.4, 2.6, -3.4, 0.6]
```

**Step 3 — multiply gaps day by day, then average**

```text
day1:  1 * 1.6   =  1.6
day2: -1 * -1.4  =  1.4
day3:  2 * 2.6   =  5.2
day4: -2 * -3.4  =  6.8
day5:  0 * 0.6   =  0.0
                      ----
sum                   15.0

Cov(A, B) = 15.0 / 5 = 3.0
```

That sum of products is also the **dot product** of the two demeaned vectors:

```text
Cov(A, B) = (dev_A · dev_B) / n = 15 / 5 = 3
```

Positive Cov: A and B tended to move together.

## Formulas — and what `E[...]` is doing

In this example, `X` is A's return, `Y` is B's return, `mu_X = 0`, `mu_Y = 0.4`.

The standard written form is:

```text
Cov(X, Y) = E[(X - mu_X)(Y - mu_Y)]
```

How to read it without getting lost:

1. `(X - mu_X)(Y - mu_Y)` is the **recipe for one day**: multiply that day's two gaps.
2. You do that recipe for **every day** (here: five products).
3. `E[...]` means **average those products**. That average is **one number**: the covariance.

So `E[...]` does not mean "one mysterious value instead of the data." It means: run the inside on all the values, then take the average. The example above *is* that formula.

Same thing written without `E`:

```text
Cov(A, B) = (1/n) * sum over days of (A_t - mean_A) * (B_t - mean_B)
```

People use `E[...]` because it is short, and it works the same way for a theoretical distribution as for a sample average.

### Shortcut (same answer, no demeaning by hand)

```text
Cov(X, Y) = E[XY] - E[X] E[Y]
```

Check on the same A, B data:

```text
E[A]  = 0
E[B]  = 0.4
E[AB] = (1*2 + (-1)*(-1) + 2*3 + (-2)*(-3) + 0*1) / 5
      = (2 + 1 + 6 + 6 + 0) / 5
      = 15 / 5 = 3

Cov = 3 - (0)(0.4) = 3
```

Same 3 as before. This is algebraically the same definition after expanding `(X - mu_X)(Y - mu_Y)` and averaging.

### Two useful identities

```text
Cov(X, X) = Var(X)
```

Covariance of a series with itself is variance: the gaps are multiplied by themselves, so you get squared gaps, which is variance.

```text
Var(X + Y) = Var(X) + Var(Y) + 2 Cov(X, Y)
```

Portfolio risk is not just "add the variances." The Cov term says whether the risks reinforce or cancel.

## Correlation

Covariance mixes co-movement with each series' own size. Correlation scales that out:

```text
Corr(X, Y) = Cov(X, Y) / (sqrt(Var(X)) * sqrt(Var(Y)))
```

Correlation sits between -1 and 1. Desks often quote correlation; risk algebra usually still runs through variance and covariance.

## Desk intuition

A hedge works when you take the opposite side of something that co-moves with your risk (high Cov, opposite position). Two longs diversify when their Cov is low or negative. Covariance is about co-movement of **returns around their means**, not about whether both names are "expensive."

---

## Recap

Variance is average squared gap from the mean. Covariance is average product of two series' gaps from their means. In formulas, `E[...]` means that average: many day-level pieces go in, one number comes out. Correlation is scaled covariance. Portfolio variance depends on the Cov term, not only on each asset's own variance.

## New Terms

- **`E[...]` / expectation:** average of what is inside the brackets.
- **`mu` / `x_bar`:** the mean. `mu` in formulas; `x_bar` for a sample average `(x_1+...+x_n)/n`.
- **Demean:** subtract the mean so you work with gaps from average.
- **Variance:** average squared gap from the mean.
- **Covariance:** average product of two series' gaps from their means.
- **Correlation:** covariance scaled by the two standard deviations; between -1 and 1.

## Checks

1. In `E[(X - mu_X)(Y - mu_Y)]`, what does the inside produce, and what does `E` do to it?
2. Why can `E[XY] - E[X]E[Y]` replace the demeaned formula?
3. Why is `Cov(X, X)` equal to `Var(X)`?

### Answers

1. The inside is one day's product of gaps; you get one product per day. `E` averages those products into the single covariance number.
2. It is the same expression after expanding `(X - mu_X)(Y - mu_Y)` and averaging; on the A/B example both give 3.
3. Multiplying X's gap by itself gives a squared gap; averaging squared gaps is variance.
