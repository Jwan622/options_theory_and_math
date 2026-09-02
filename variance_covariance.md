# Variance and Covariance

## Learning Goal

Variance tells you how much one thing moves around its average. Covariance tells you whether two things tend to move together, and in which direction. On a desk, these are the building blocks behind portfolio risk, hedging, and correlation: if you do not understand how much each asset swings and whether those swings line up, you cannot reason about total risk.

---

# Variance

## The problem

Suppose a stock's daily return averages 0%. That average alone does not tell you whether the stock usually moves by 0.2% or by 3%. Two assets can have the same average return and still be completely different risks. Variance answers: how far do outcomes typically sit from the mean?

## Intuition

Think of a return series as points scattered around a horizontal line at the average. Variance is a single number that summarizes that scatter. Large swings in either direction increase variance. Outcomes that hug the mean keep variance small.

A subtle point: variance squares the deviations, so a +3% day and a -3% day both add the same amount. Direction is thrown away. Only size of the miss matters.

## Small example

Five daily returns (in percent):

```text
r = [1, -1, 2, -2, 0]
```

The mean is:

```text
mean = (1 - 1 + 2 - 2 + 0) / 5 = 0
```

Deviations from the mean are the same as the returns themselves here: `1, -1, 2, -2, 0`.

Square them:

```text
1, 1, 4, 4, 0
```

Average of the squared deviations (population variance):

```text
Var = (1 + 1 + 4 + 4 + 0) / 5 = 2
```

So the variance is 2 (in percent-squared units). The square root of variance is the standard deviation:

```text
SD = sqrt(2) ≈ 1.41%
```

Standard deviation is usually easier to talk about because it is in the same units as the original data. Variance is still the more natural object in formulas, especially when risks are added.

## Equation

For a random variable \(X\) with mean \(\mu = E[X]\):

\[
\operatorname{Var}(X) = E[(X - \mu)^2]
\]

Equivalently:

\[
\operatorname{Var}(X) = E[X^2] - (E[X])^2
\]

For a sample of observations \(x_1, \ldots, x_n\) with sample mean \(\bar{x}\), people often use:

\[
s^2 = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2
\]

The \(n-1\) version is the usual sample variance estimator. The idea is the same either way: average squared distance from the mean.

## What can go wrong

A common mistake is to treat variance as if it lived in the same units as returns. It does not. If returns are in percent, variance is in percent-squared. That is why people quote volatility as standard deviation.

Another trap: variance only measures spread around the mean. It does not tell you whether the distribution is skewed, whether crashes are more common than rallies, or whether risk is concentrated in rare events. Two return series can share the same variance and still feel very different to trade.

---

# Covariance

## The problem

Variance describes one series. But trading problems almost always involve more than one thing: a stock and its hedge, a basket and the index, two names in a portfolio. The question becomes: when A moves up, does B tend to move up too, move down, or wander independently?

Covariance answers that joint question with a signed number.

## Intuition

For each day, look at how far A is above or below its mean, and how far B is above or below its mean. Multiply those two deviations.

- If both are above their means on the same day, the product is positive.
- If both are below their means on the same day, the product is also positive.
- If one is above and the other is below, the product is negative.

Average those products and you get covariance. Positive covariance means the two series tend to move in the same direction relative to their means. Negative covariance means they tend to move in opposite directions. Covariance near zero means no linear co-movement on average.

ASCII picture:

```text
same-direction days          opposite-direction days
A high, B high  -> +         A high, B low  -> -
A low,  B low   -> +         A low,  B high -> -

average of these products = covariance
```

## Small example

Two assets, five days:

```text
A = [1, -1, 2, -2, 0]     mean_A = 0
B = [2, -1, 3, -3, 1]     mean_B = (2-1+3-3+1)/5 = 0.4
```

Deviations for B:

```text
B - mean_B = [1.6, -1.4, 2.6, -3.4, 0.6]
```

Day-by-day products of deviations:

```text
day1: 1 * 1.6  =  1.6
day2: -1 * -1.4 = 1.4
day3: 2 * 2.6  =  5.2
day4: -2 * -3.4 = 6.8
day5: 0 * 0.6  =  0
```

Average (population covariance):

```text
Cov(A,B) = (1.6 + 1.4 + 5.2 + 6.8 + 0) / 5 = 3.0
```

The positive number says A and B tended to move together in this sample. That matches the eye test: big up days in A lined up with big up days in B, and the same for down days.

## Equation

For random variables \(X\) and \(Y\) with means \(\mu_X\) and \(\mu_Y\):

\[
\operatorname{Cov}(X,Y) = E[(X - \mu_X)(Y - \mu_Y)]
\]

Equivalently:

\[
\operatorname{Cov}(X,Y) = E[XY] - E[X]E[Y]
\]

Useful identities:

\[
\operatorname{Cov}(X,X) = \operatorname{Var}(X)
\]

\[
\operatorname{Var}(X+Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) + 2\operatorname{Cov}(X,Y)
\]

That last identity is why covariance matters for portfolios. Adding two risky assets does not just add their variances. The co-movement term can increase total risk (positive covariance) or reduce it (negative covariance / hedging).

## Correlation is the scaled version

Covariance depends on the units and sizes of the two series. A stock that moves 3% a day and one that moves 0.3% a day can have a large or small covariance just because of scale. Correlation removes that:

\[
\operatorname{Corr}(X,Y) = \frac{\operatorname{Cov}(X,Y)}{\sqrt{\operatorname{Var}(X)}\sqrt{\operatorname{Var}(Y)}}
\]

Correlation always sits between -1 and 1. Covariance does not. In desk conversation people often quote correlation, but the algebra of risk usually runs through covariance and variance first.

## Desk intuition

If you hold a long portfolio and hedge with another instrument, you care whether the hedge moves with the risk you are trying to cancel. High positive covariance between the position and the hedge instrument is useful for hedging only if you take the opposite side in the hedge. Negative covariance between two longs is what diversifies: losses in one are more often offset by gains in the other.

Covariance is about co-movement around means, not about levels. Two stocks can both be expensive and still have low covariance of returns if their day-to-day changes do not line up.

---

## Recap

Variance measures how far one variable tends to sit from its mean, using squared deviations so every large miss counts positively. Covariance measures whether two variables tend to deviate from their means in the same direction or opposite directions, by averaging the product of those deviations. Portfolio variance is not just the sum of individual variances; the covariance term decides whether risks reinforce or cancel. Correlation is covariance after scaling each series by its own volatility, which makes co-movement comparable across assets.

## New Terms

- **Mean (expected value):** the average level of a random variable.
- **Deviation:** how far an outcome sits above or below the mean.
- **Variance:** expected squared deviation from the mean; a measure of spread.
- **Standard deviation (volatility):** the square root of variance; spread in the original units.
- **Covariance:** expected product of two variables' deviations from their means; a signed measure of co-movement.
- **Correlation:** covariance scaled by the two standard deviations; co-movement on a -1 to 1 scale.

## Checks

1. Why can two stocks with the same average return still have very different risk?
2. If \(\operatorname{Cov}(X,Y)\) is negative, what does that say about a portfolio that is long both \(X\) and \(Y\)?
3. Why is correlation often quoted instead of raw covariance?

### Answers

1. Risk depends on how far returns wander from the mean, not only on the mean itself; different variances mean different typical swing sizes.
2. Negative covariance means the two longs often move in opposite directions relative to their means, so the \(2\operatorname{Cov}\) term reduces total portfolio variance.
3. Covariance mixes co-movement with each series' own scale; correlation divides that out so the number is comparable across pairs.
