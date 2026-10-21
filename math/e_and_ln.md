# The Number $e$ and the Natural Log $\ln$

## Learning Goal

Understand what $e = 2.71828\ldots$ is, why it shows up everywhere growth happens, and what $\ln$ (the natural log) does. By the end, $e^{rT}$, $e^{-rT}$ and $\ln(S/K)$ in option formulas should read like plain English rather than symbols.

The path:

```text
1. Growth by multiplying          why exponents appear at all
2. Compounding faster and faster  where e comes from
3. Why the limit is a real number e = 1 + 1 + 1/2! + 1/3! + ...
4. Growth at any rate r           e^r, e^(rT)
5. e's special property           the slope of e^x equals e^x
6. Exponent rules                 the toolkit, each rule proved
7. ln, the undo button            definition, rules, slope of ln x
8. Intuition pumps                doubling time, small-x shortcuts
9. Options theory                 discounting, log returns, ln(S/K), lognormal prices
```

Prerequisites: high-school algebra and the idea of a derivative as a slope. Everything else is built here.

---

# 1. Growth by Multiplying

**The problem.** Some things grow by *adding* a fixed amount each period: a salary that rises \$1,000 a year. Others grow by *multiplying* by a fixed factor: money in a bank, a population, a stock price. Multiplicative growth is where exponents, and eventually $e$, come from.

**Example.** \$100 earns 10% a year. Each year the balance is multiplied by $1.10$:

| Year | Calculation | Balance |
|---|---|---|
| 0 | $100$ | 100.00 |
| 1 | $100 \times 1.10$ | 110.00 |
| 2 | $100 \times 1.10 \times 1.10 = 100 \times 1.10^2$ | 121.00 |
| 3 | $100 \times 1.10^3$ | 133.10 |
| $t$ | $100 \times 1.10^t$ | |

Multiplying by the same factor $t$ times is written as a power: $1.10^t$. In the expression $b^t$, $b$ is the **base** and $t$ is the **exponent**.

Notice the year-2 balance is 121, not 120. The extra \$1 is interest earned on the first year's interest. That "interest on interest" effect is **compounding**, and it's what the rest of this lesson is about.

---

# 2. Compounding Faster and Faster: Where $e$ Comes From

**The question.** A bank offers 100% interest per year. (Unrealistic, but it makes the numbers clean.) How much does \$1 become after one year? It depends on how often the bank pays the interest.

### The one rule we need: earning interest means multiplying by (1 + rate)

Say your balance is $B$ and the bank pays interest at rate $i$ for one period. The interest is $B \times i$. Your new balance is the old balance plus the interest:

$$\text{new balance} = B + B \times i$$

Both terms contain $B$, so factor it out:

$$\text{new balance} = B \times (1 + i)$$

**Paying interest at rate $i$ is the same as multiplying the balance by $(1 + i)$.** For example, 50% interest on \$1.50: the interest is $1.50 \times 0.5 = 0.75$, the new balance is $1.50 + 0.75 = 2.25$, and that equals $1.50 \times 1.5$. ✓

### Splitting the year into $n$ periods

If the bank pays $n$ times a year, it splits the 100% evenly into $n$ equal payments. Each payment's rate is $\frac{100\%}{n}$.

**Convert that percent to a decimal**, because the rule above needs $i$ as a plain number. "Percent" means "per hundred", so a percent becomes a decimal by dividing by 100:

$$100\% = \frac{100}{100} = 1$$

Replace $100\%$ with 1:

$$\frac{100\%}{n} = \frac{1}{n}$$

| Payments per year $n$ | Rate per payment as a percent, $\frac{100\%}{n}$ | Same rate as a decimal, $\frac{1}{n}$ | Multiply each period by $1 + \frac1n$ |
|---|---|---|---|
| 1 | 100% | 1 | 2 |
| 2 | 50% | 0.5 | 1.5 |
| 4 | 25% | 0.25 | 1.25 |
| 12 | 8.33% | 0.0833 | 1.0833 |

So each period has $i = \frac{1}{n}$, and by the rule above it multiplies the balance by $\left(1 + \frac{1}{n}\right)$. That happens $n$ times in a year. Every case below follows the same pattern:

$$\text{one dollar after one year} = \underbrace{\left(1 + \frac1n\right) \times \left(1 + \frac1n\right) \times \cdots \times \left(1 + \frac1n\right)}_{n \text{ times}} = \left(1 + \frac{1}{n}\right)^n$$

Now plug in $n = 1, 2, 4$ and track the balance period by period.

**These are not two different formulas.** Each period you can get the end balance two ways, and they always give the same number:

- **Add:** end = start + interest, where interest = start × $i$.
- **Multiply:** end = start × $(1 + i)$.

The multiply version is just the add version with the start balance factored out (that's the rule $B + Bi = B(1 + i)$ above). The tables below show both columns side by side, so you can see they match. The add column is how a bank statement reads. The multiply column is what leads to the formula, because multiplying by the same factor every period stacks up into a power.

**Once a year, $n = 1$.** One payment at rate $i = \frac11 = 1$ (100%), so the factor is $1 + i = 2$:

| Period | Start | Interest = start × 1 | Add: start + interest | Multiply: start × 2 |
|---|---|---|---|---|
| Year | 1.00 | 1.00 | $1.00 + 1.00 = 2.00$ | $1.00 \times 2 = 2.00$ |

One multiplication by 2:

$$1 \times 2 = \left(1 + \frac{1}{1}\right)^1 = 2$$

**Twice a year, $n = 2$.** Two payments, each at rate $i = \frac12 = 0.5$ (50%), so the factor is $1 + i = 1.5$:

| Period | Start | Interest = start × 0.5 | Add: start + interest | Multiply: start × 1.5 |
|---|---|---|---|---|
| Months 1–6 | 1.00 | 0.50 | $1.00 + 0.50 = 1.50$ | $1.00 \times 1.5 = 1.50$ |
| Months 7–12 | 1.50 | 0.75 | $1.50 + 0.75 = 2.25$ | $1.50 \times 1.5 = 2.25$ |

Follow the multiply column from the top. The second row starts with the first row's result, 1.50, which was itself $1 \times 1.5$. So the year's end balance is

$$\underbrace{1 \times 1.5}_{\text{first half}} \times \underbrace{1.5}_{\text{second half}} = 1.5^2 = \left(1 + \frac{1}{2}\right)^2 = 2.25$$

The second half-year pays \$0.75, not \$0.50, because it pays 50% on \$1.50 instead of on \$1. The extra \$0.25 is interest on the first half-year's interest. That's why 2.25 beats 2.

**Four times a year, $n = 4$.** Four payments, each at rate $i = \frac14 = 0.25$ (25%), so the factor is $1 + i = 1.25$:

| Period | Start | Interest = start × 0.25 | Add: start + interest | Multiply: start × 1.25 |
|---|---|---|---|---|
| Quarter 1 | 1.000000 | 0.250000 | 1.250000 | 1.250000 |
| Quarter 2 | 1.250000 | 0.312500 | 1.562500 | 1.562500 |
| Quarter 3 | 1.562500 | 0.390625 | 1.953125 | 1.953125 |
| Quarter 4 | 1.953125 | 0.488281 | 2.441406 | 2.441406 |

The multiply column is $1 \times 1.25 \times 1.25 \times 1.25 \times 1.25$, four factors of 1.25:

$$1.25^4 = \left(1 + \frac{1}{4}\right)^4 = 2.4414$$

Each quarter's interest is bigger than the last, because the balance it's paid on keeps growing.

**Any $n$.** Same pattern: $n$ periods, each multiplying by $\left(1 + \frac1n\right)$:

$$\left(1 + \frac{1}{n}\right)^n$$

Plug in more and more frequent compounding:

| $n$ | Meaning | $\left(1 + \frac1n\right)^n$ |
|---|---|---|
| 1 | yearly | 2.000000 |
| 2 | half-yearly | 2.250000 |
| 4 | quarterly | 2.441406 |
| 12 | monthly | 2.613035 |
| 365 | daily | 2.714567 |
| 1,000,000 | a million times a year | 2.718280 |

Two things stand out:

1. **More frequent compounding always helps**, because interest starts earning interest sooner.
2. **But the gains shrink and the values settle down.** Monthly to daily adds 0.10. Daily to a million times a year adds only 0.004. The values approach a ceiling of about 2.71828.

That ceiling is the number $e$:

$$\boxed{e = \lim_{n \to \infty}\left(1 + \frac{1}{n}\right)^n = 2.718281828\ldots}$$

($\lim_{n\to\infty}$ means "the value this approaches as $n$ grows without bound.")

**High level:** $e$ is what \$1 becomes after one year at 100% interest, compounded *continuously*, meaning every instant. It's the natural upper limit of compounding.

---

# 3. Why the Limit Is a Real Number: $e = 1 + 1 + \frac{1}{2!} + \frac{1}{3!} + \cdots$

The table suggests the values settle near 2.71828, but a table isn't a proof. Let's show it, by expanding $\left(1 + \frac1n\right)^n$ term by term. This also gives a fast way to compute $e$.

### Tool: the binomial theorem

**Factorial.** $k!$ (read as $k$ factorial) is $1 \times 2 \times \cdots \times k$. So $1! = 1$, $2! = 2$, $3! = 6$, $4! = 24$, $5! = 120$. By convention $0! = 1$.

**Binomial theorem.** Expanding $(1 + y)^n$ gives

$$(1 + y)^n = \sum_{k=0}^{n} \binom{n}{k} y^k, \qquad \binom{n}{k} = \frac{n!}{k!\,(n-k)!}$$

$\binom{n}{k}$ (read as $n$ choose $k$) counts the ways to pick $k$ of the $n$ factors to contribute a $y$. Check with $n = 2$: $(1+y)^2 = 1 + 2y + y^2$, and the formula gives coefficients $\binom20 = 1$, $\binom21 = 2$, $\binom22 = 1$. ✓

A handy way to write $\binom nk$: cancel the $(n-k)!$ from the top and bottom of $\frac{n!}{k!(n-k)!}$, which leaves

$$\binom{n}{k} = \frac{n(n-1)(n-2)\cdots(n-k+1)}{k!}$$

with $k$ factors on top. For example, $\binom{10}{2} = \frac{10 \times 9}{2} = 45$.

### Step 1: expand

Use the binomial theorem with $y = \frac1n$:

$$\left(1 + \frac{1}{n}\right)^n = \sum_{k=0}^{n} \binom{n}{k}\frac{1}{n^k}$$

### Step 2: look at one term

The $k$-th term is

$$\binom{n}{k}\frac{1}{n^k} = \frac{n(n-1)\cdots(n-k+1)}{k!\; n^k}$$

There are $k$ factors on top and $k$ factors of $n$ in $n^k$ on the bottom. Pair them up:

$$= \frac{1}{k!}\cdot\frac{n}{n}\cdot\frac{n-1}{n}\cdot\frac{n-2}{n}\cdots\frac{n-k+1}{n}$$

Simplify each fraction, $\frac{n-j}{n} = 1 - \frac{j}{n}$:

$$= \frac{1}{k!}\cdot 1\cdot\left(1 - \frac1n\right)\left(1 - \frac2n\right)\cdots\left(1 - \frac{k-1}{n}\right)$$

### Step 3: let $n$ grow

As $n \to \infty$, each $\frac{j}{n} \to 0$, so each bracket $\to 1$. The $k$-th term approaches $\frac{1}{k!}$.

**With numbers, $n = 10$:**

| $k$ | Term with $n = 10$ | Limit $\frac{1}{k!}$ |
|---|---|---|
| 0 | $1$ | 1 |
| 1 | $\binom{10}{1}\frac{1}{10} = \frac{10}{10} = 1$ | 1 |
| 2 | $\binom{10}{2}\frac{1}{100} = \frac{45}{100} = 0.45$ | 0.5 |
| 3 | $\binom{10}{3}\frac{1}{1000} = \frac{120}{1000} = 0.12$ | 0.1667 |

Each term creeps up toward $\frac{1}{k!}$ as $n$ grows. Since every bracket is at most 1, each term is always **at most** $\frac{1}{k!}$. That makes it legitimate to take the limit term by term, and gives

$$\boxed{e = \sum_{k=0}^{\infty}\frac{1}{k!} = 1 + 1 + \frac{1}{2} + \frac{1}{6} + \frac{1}{24} + \frac{1}{120} + \cdots}$$

### Step 4: add it up

| Terms through $k$ | New term $\frac{1}{k!}$ | Running total |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 1 | 2 |
| 2 | 0.5 | 2.5 |
| 3 | 0.166667 | 2.666667 |
| 4 | 0.041667 | 2.708333 |
| 5 | 0.008333 | 2.716667 |
| 6 | 0.001389 | 2.718056 |
| 8 | 0.0000248 | 2.718279 |
| 10 | 0.000000276 | 2.718282 |

Ten terms give six correct decimal places. Factorials grow so fast that the terms shrink very quickly. Compare: compounding a million times a year only got 2.718280.

### Step 5: proof that the sum is finite (and $e < 3$)

From $k = 2$ on, $k! = 1 \times 2 \times 3 \times \cdots \times k$ has at least $k-1$ factors that are each 2 or more, so $k! \ge 2^{k-1}$. (Check: $3! = 6 \ge 2^2 = 4$; $4! = 24 \ge 2^3 = 8$.) Flip both sides: $\frac{1}{k!} \le \frac{1}{2^{k-1}}$. So

$$e = 1 + 1 + \frac{1}{2!} + \frac{1}{3!} + \cdots \le 1 + 1 + \frac12 + \frac14 + \frac18 + \cdots$$

The tail $1 + \frac12 + \frac14 + \cdots$ adds up to 2 (a geometric series; see `taylor_series.md`, Section 1). So $e \le 1 + 2 = 3$. The sum is finite, and $e$ is a genuine number between 2.5 and 3.

**High level:** $e$ is compounding in the limit, and that limit can be written as $1 + 1 + \frac{1}{2!} + \frac{1}{3!} + \cdots$. This series is the first example of a **Taylor series**, the subject of `taylor_series.md`.

---

# 4. Growth at Any Rate: $e^r$ and $e^{rT}$

Real interest rates aren't 100%. Repeat Section 2 with rate $r$: $n$ payments of $\frac{r}{n}$ each.

$$\text{value of one dollar after one year} = \left(1 + \frac{r}{n}\right)^n$$

**Claim:** as $n \to \infty$, this approaches $e^r$.

**Proof.**

1. Define $m = \frac{n}{r}$. Then $\frac{r}{n} = \frac{1}{m}$, and $n = mr$.
2. Substitute both:

$$\left(1 + \frac{r}{n}\right)^n = \left(1 + \frac{1}{m}\right)^{mr}$$

3. Use the exponent rule $a^{bc} = \left(a^b\right)^c$ (proved in Section 6):

$$= \left[\left(1 + \frac{1}{m}\right)^{m}\right]^{r}$$

4. As $n \to \infty$, $m = n/r \to \infty$ too, so the bracket approaches $e$:

$$\lim_{n\to\infty}\left(1 + \frac{r}{n}\right)^n = e^{r}$$

**Numbers, $r = 5\%$:** monthly compounding gives $\left(1 + \frac{0.05}{12}\right)^{12} = 1.051162$, daily gives $1.051267$, and continuous gives $e^{0.05} = 1.051271$.

**Over $T$ years**, compound the one-year growth $T$ times: $\left(e^r\right)^T = e^{rT}$.

**Example.** \$100 at 5% continuous for 3 years:

1. $rT = 0.05 \times 3 = 0.15$
2. $e^{0.15} = 1.161834$
3. $100 \times 1.161834 = \$116.18$

**High level:** $e^{rT}$ is the growth factor for continuous growth at rate $r$ for time $T$. The exponent $rT$ is the **total accumulated growth**: rate times time.

---

# 5. The Special Property: $e^x$ Is Its Own Slope

So far $e$ looks like a fact about banking. Here is why mathematicians care more about it than any other base.

**The question.** How fast is $b^x$ growing at a given $x$? That's its derivative, its slope.

### Step 1: every exponential's slope is proportional to itself

Use the definition of the derivative: the slope at $x$ is the limit of rise over run for a tiny step $h$:

$$\frac{d}{dx}b^x = \lim_{h\to0}\frac{b^{x+h} - b^x}{h}$$

Split $b^{x+h} = b^x\,b^h$ (exponent rule, Section 6) and factor out $b^x$:

$$= \lim_{h\to0}\frac{b^x\,b^h - b^x}{h} = b^x\cdot\lim_{h\to0}\frac{b^h - 1}{h}$$

The limit on the right doesn't depend on $x$. It's just a number that depends on the base $b$. Call it $c_b$. So

$$\frac{d}{dx}b^x = c_b\,b^x$$

**Every exponential grows at a rate proportional to its current size.** $c_b$ is the slope of $b^x$ at $x = 0$ (where $b^0 = 1$).

### Step 2: measure $c_b$ for some bases

Estimate $c_b = \frac{b^h - 1}{h}$ with small $h = 0.001$:

| Base $b$ | $\frac{b^{0.001} - 1}{0.001}$ | $c_b$ |
|---|---|---|
| 2 | $\frac{1.000693 - 1}{0.001}$ | 0.693 |
| $e$ | | **1.000** |
| 3 | $\frac{1.001099 - 1}{0.001}$ | 1.099 |

Base 2 grows too slowly ($c_2 = 0.693$), and base 3 a bit too fast ($c_3 = 1.099$). There's exactly one base in between where $c_b = 1$, and it's $e$.

### Step 3: check that the base is really $e$

For $b = e$, we need $\lim_{h\to0}\frac{e^h - 1}{h} = 1$. Numerically:

| $h$ | $e^h$ | $\frac{e^h - 1}{h}$ |
|---|---|---|
| 0.1 | 1.105171 | 1.0517 |
| 0.01 | 1.010050 | 1.0050 |
| 0.001 | 1.001000 | 1.0005 |

It's heading to 1. For a proof, use the series from Section 3 with $x$ in place of 1 (Section 5 of `taylor_series.md` shows that $e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$). With $x = h$:

1. $e^h - 1 = h + \frac{h^2}{2} + \frac{h^3}{6} + \cdots$
2. Divide by $h$: $\frac{e^h - 1}{h} = 1 + \frac{h}{2} + \frac{h^2}{6} + \cdots$
3. As $h \to 0$, every term but the 1 vanishes. The limit is 1. ✓

(Check against the table: at $h = 0.1$, $1 + 0.05 + 0.0017 = 1.0517$. ✓)

### Result

$$\boxed{\frac{d}{dx}e^x = e^x}$$

**Another way to see it.** Differentiate the series term by term, using $\frac{d}{dx}x^k = k\,x^{k-1}$ and $\frac{k}{k!} = \frac{1}{(k-1)!}$:

$$\frac{d}{dx}\left(1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \cdots\right) = 0 + 1 + \frac{2x}{2!} + \frac{3x^2}{3!} + \frac{4x^3}{4!} + \cdots = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$$

Each term turns into the one before it, so the series reproduces itself.

**High level:** $e^x$ grows at a rate *exactly equal to its current value*. A quantity that grows in proportion to its size, like money compounding continuously or a stock with a constant expected return, is naturally written as a power of $e$. With a rate $r$, the chain rule gives $\frac{d}{dt}e^{rt} = r\,e^{rt}$: growth at rate $r$ times the current size.

---

# 6. Exponent Rules, Each Proved

These rules get used constantly. Each follows from "an exponent counts how many times you multiply." The proofs below use whole numbers $p$ and $q$; the rules extend to all real exponents.

**Rule 1: $e^{p}\,e^{q} = e^{p+q}$.** Multiplying $p$ copies of $e$ by $q$ more copies gives $p + q$ copies.
Numbers: $e^{0.1}\,e^{0.2} = 1.10517 \times 1.22140 = 1.34986 = e^{0.3}$. ✓

**Rule 2: $e^{0} = 1$.** From Rule 1, $e^{0}\,e^{q} = e^{0+q} = e^{q}$. Divide both sides by $e^q$: $e^0 = 1$.

**Rule 3: $e^{-p} = \frac{1}{e^{p}}$.** From Rules 1 and 2, $e^{p}\,e^{-p} = e^{p - p} = e^0 = 1$. Divide both sides by $e^p$.
Numbers: $e^{-0.05} = \frac{1}{1.05127} = 0.95123$.

**Rule 4: $\frac{e^{p}}{e^{q}} = e^{p-q}$.** Write $\frac{e^p}{e^q} = e^{p}\,e^{-q}$ (Rule 3), then use Rule 1.

**Rule 5: $\left(e^{p}\right)^{q} = e^{pq}$.** Multiply $q$ copies of $e^p$: by Rule 1 the exponents add, $p + p + \cdots + p = pq$.

**Rule 6: $e^x > 0$ for every $x$.** For $x \ge 0$, $e^x \ge 1$ (a product of numbers bigger than 1). For $x < 0$, Rule 3 makes $e^x = 1/e^{-x}$, a positive number. This is why stock prices written as $S_0 e^{(\ldots)}$ can never go negative.

---

# 7. $\ln$: The Undo Button for $e^x$

**The problem.** Section 4 answers "grow at rate $r$ for time $T$: what's the factor?" Often we need the reverse: "this stock went from 100 to 110: what continuous growth rate does that mean?" That reverse question is what $\ln$ answers.

### Definition

$\ln(x)$, the **natural logarithm**, is the power you raise $e$ to in order to get $x$:

$$y = \ln(x) \quad\text{means}\quad e^{y} = x$$

| $x$ | $\ln x$ | because |
|---|---|---|
| 1 | 0 | $e^0 = 1$ |
| $e = 2.71828$ | 1 | $e^1 = e$ |
| 2 | 0.6931 | $e^{0.6931} = 2$ |
| 10 | 2.3026 | $e^{2.3026} = 10$ |
| 0.5 | −0.6931 | $e^{-0.6931} = 0.5$ |
| 1.10 | 0.0953 | $e^{0.0953} = 1.10$ |

Observations:

- $\ln$ is only defined for $x > 0$, because $e^y$ is always positive (Rule 6).
- $\ln x < 0$ when $0 < x < 1$, and $\ln x > 0$ when $x > 1$.
- $\ln(0.5) = -\ln(2)$. Halving is the exact opposite of doubling in log terms. (Proved by Rule L3 below.)

$\ln$ and $e^{(\cdot)}$ undo each other:

$$e^{\ln x} = x \qquad\text{and}\qquad \ln\left(e^{y}\right) = y$$

Graphically, $y = \ln x$ is the curve $y = e^x$ reflected across the diagonal line $y = x$.

### Log rules, each derived from an exponent rule

**L1: $\ln(ab) = \ln a + \ln b$.** Let $p = \ln a$ and $q = \ln b$, so $a = e^p$ and $b = e^q$. Then $ab = e^p\,e^q = e^{p+q}$ by Rule 1. Take $\ln$ of both sides: $\ln(ab) = p + q = \ln a + \ln b$.
Numbers: $\ln(2 \times 5) = \ln 10 = 2.3026$, and $\ln 2 + \ln 5 = 0.6931 + 1.6094 = 2.3026$. ✓

**L2: $\ln\frac{a}{b} = \ln a - \ln b$.** Same steps with Rule 4: $\frac{a}{b} = e^{p}/e^{q} = e^{p-q}$.

**L3: $\ln\frac1b = -\ln b$.** Use L2 with $a = 1$ and $\ln 1 = 0$: $\ln\frac1b = 0 - \ln b$.

**L4: $\ln\left(a^c\right) = c\ln a$.** Write $a = e^{p}$. Then $a^c = \left(e^p\right)^c = e^{pc}$ by Rule 5, so $\ln\left(a^c\right) = pc = c\ln a$.
Numbers: $\ln\left(2^{10}\right) = \ln 1024 = 6.931$, and $10\ln 2 = 10 \times 0.6931 = 6.931$. ✓

**The big idea:** logs turn multiplication into addition, division into subtraction, and powers into multiplication. Multiplicative growth becomes additive in log terms, and addition is much easier to do statistics on.

### Any base can be written with $e$

Any positive number $a$ equals $e^{\ln a}$. So by Rule 5,

$$a^x = \left(e^{\ln a}\right)^x = e^{x\ln a}$$

Every exponential is secretly a power of $e$. For example, $2^{10} = e^{10\ln2} = e^{10 \times 0.6931} = e^{6.931} = 1024$.

This also explains the slopes in Section 5. By the chain rule, $\frac{d}{dx}e^{x\ln a} = \ln a \cdot e^{x\ln a}$, so $\frac{d}{dx}a^x = (\ln a)\,a^x$. So $c_2 = \ln 2 = 0.693$ and $c_3 = \ln 3 = 1.099$, matching the table exactly.

### The slope of $\ln x$ is $\frac1x$

Let $y = \ln x$. Then $e^{y} = x$. Differentiate both sides with respect to $x$. The left side, by the chain rule, is $e^{y}\frac{dy}{dx}$. The right side is 1:

$$e^{y}\frac{dy}{dx} = 1$$

Divide by $e^{y}$, and remember $e^{y} = x$:

$$\frac{dy}{dx} = \frac{1}{e^{y}} = \frac{1}{x}$$

$$\boxed{\frac{d}{dx}\ln x = \frac{1}{x}}$$

Check at $x = 2$: $\frac{\ln 2.001 - \ln 2}{0.001} = 0.49988$, and $\frac12 = 0.5$. ✓

**What it means:** $d(\ln x) = \frac{dx}{x}$. A small change in $\ln x$ is the *percentage* change in $x$. That's why log returns behave like percentage returns for small moves (Section 8).

---

# 8. Intuition Pumps

### Doubling time and the rule of 70

How long until money doubles at continuous rate $r$?

1. We need $e^{rT} = 2$.
2. Take $\ln$ of both sides: $rT = \ln 2 = 0.693$.
3. Divide by $r$: $T = \frac{0.693}{r}$.

At 7%: $T = \frac{0.693}{0.07} = 9.9$ years. With $r$ written in percent, $T \approx \frac{69.3}{r\%}$, which is the "rule of 70". People often use 72 instead because 72 divides evenly by 2, 3, 4, 6, 8, 9 and 12, and because annual (not continuous) compounding needs a slightly bigger number.

### For small $x$: $e^x \approx 1 + x$ and $\ln(1+x) \approx x$

| $x$ | $e^x$ | $1 + x$ | $\ln(1 + x)$ |
|---|---|---|---|
| 0.01 | 1.010050 | 1.01 | 0.009950 |
| 0.05 | 1.051271 | 1.05 | 0.048790 |
| 0.10 | 1.105171 | 1.10 | 0.095310 |
| 0.20 | 1.221403 | 1.20 | 0.182322 |
| 0.50 | 1.648721 | 1.50 | 0.405465 |

For small $x$ the approximations are excellent. For big $x$ they drift. The reason is the series: $e^x = 1 + x + \frac{x^2}{2} + \cdots$, and the $\frac{x^2}{2}$ is negligible only when $x$ is small. `taylor_series.md` develops this fully.

**What it means for returns:** for a small move, the log return $\ln(1 + x)$ and the simple return $x$ are almost the same. For large moves they differ, and the log return is always the smaller of the two.

### Logs measure ratios, symmetrically

Going from 100 to 110 is a log return of $\ln\frac{110}{100} = +0.0953$. Going from 110 back to 100 is $\ln\frac{100}{110} = -0.0953$, by L3. Exactly opposite. In percentage terms the same trip is $+10\%$ then $-9.09\%$, which looks lopsided. Logs treat "up by a factor" and "down by the same factor" as equal and opposite moves.

### $\ln$ is the continuously compounded rate

If a stock goes from $S_0$ to $S_1$ in one year, which continuous rate $r$ does that? Solve $S_0\,e^{r} = S_1$:

1. Divide by $S_0$: $e^r = \frac{S_1}{S_0}$
2. Take $\ln$: $r = \ln\frac{S_1}{S_0}$

**The log return is the continuously compounded growth rate.** That's the deepest reason traders use it.

---

# 9. How This Shows Up in Options Theory

Each item below appears in `../options_theory/bsm_primer.md`.

### Discounting: $e^{-rT}$

Money paid at time $T$ is worth less today. If $P$ grows to $X$ at time $T$, then $P\,e^{rT} = X$. Divide by $e^{rT}$ and use Rule 3:

$$P = X\,e^{-rT}$$

In the BSM call formula $C = S\,N(d_1) - K e^{-rT} N(d_2)$, the term $K e^{-rT}$ is today's value of the strike, which you'd pay at expiry. With $K = 100$, $r = 5\%$, $T = 1$: $K e^{-rT} = 100 \times 0.951229 = 95.12$.

### Log returns add across time

For prices $S_0 \to S_1 \to S_2$:

$$\ln\frac{S_2}{S_0} = \ln\left(\frac{S_1}{S_0}\cdot\frac{S_2}{S_1}\right) = \ln\frac{S_1}{S_0} + \ln\frac{S_2}{S_1}$$

(by L1). A year's log return is the sum of about 252 daily log returns. Sums of many independent pieces are approximately normal (Central Limit Theorem), which is the starting assumption behind BSM.

### Prices are $e^{(\text{something normal})}$

The BSM stock model solves to

$$S_T = S_0\exp\left[\left(\mu - \tfrac12\sigma^2\right)T + \sigma\sqrt{T}\,Z\right]$$

where $Z$ is a standard normal random number. Rule 6 guarantees $S_T > 0$. Taking $\ln$ undoes the exponential:

$$\ln\frac{S_T}{S_0} = \left(\mu - \tfrac12\sigma^2\right)T + \sigma\sqrt{T}\,Z$$

which is normal. A variable whose log is normal is called **lognormal**.

### $\ln(S/K)$: moneyness in log units

The BSM formula contains

$$d_1 = \frac{\ln\frac{S}{K} + \left(r + \tfrac12\sigma^2\right)T}{\sigma\sqrt T}$$

$\ln\frac{S}{K}$ measures how far the stock is from the strike, as a continuously compounded percentage. $S = 110$, $K = 100$ gives $+0.0953$. $S = 90.91$, $K = 100$ gives $-0.0953$. Same distance in log terms, which makes sense because both are "off by a factor of 1.1."

Logs also tidy the formula. Define the **forward price** $F = S\,e^{rT}$: the stock price grown at the risk-free rate to expiry. By L1 and $\ln e^{rT} = rT$:

$$\ln\frac{F}{K} = \ln\frac{S\,e^{rT}}{K} = \ln\frac{S}{K} + rT$$

So the numerator of $d_1$ is $\ln\frac{F}{K} + \tfrac12\sigma^2T$: the distance from the strike to the forward, plus a volatility term. With $S = K = 100$, $r = 5\%$, $T = 1$: $F = 105.13$ and $\ln\frac{F}{K} = 0.05$.

### The convexity bonus: $E\left[e^{bZ}\right] = e^{b^2/2}$

Because $e^x$ curves upward, the average of $e^{(\text{random})}$ is bigger than $e^{(\text{average})}$. Example: $Z = \pm1$ with equal chance and $b = 0.2$ give $\frac{e^{0.2} + e^{-0.2}}{2} = \frac{1.2214 + 0.8187}{2} = 1.0201$, not $e^0 = 1$. The primer (Section 1.4) proves $E\left[e^{bZ}\right] = e^{b^2/2}$ for a standard normal, which here is $e^{0.02} = 1.0202$. This is where the $\tfrac12\sigma^2$ terms in BSM come from.

---

# Recap

1. $e = \lim\left(1 + \frac1n\right)^n = 2.71828\ldots$ is what continuous compounding at 100% produces. It also equals $\sum \frac{1}{k!}$.
2. Continuous growth at rate $r$ for time $T$ multiplies by $e^{rT}$. Discounting multiplies by $e^{-rT}$.
3. $e^x$ is the unique exponential whose slope equals its value: $\frac{d}{dx}e^x = e^x$. Every other exponential is $a^x = e^{x\ln a}$.
4. $\ln$ undoes $e^{(\cdot)}$. It turns products into sums, so log returns add across time. Its slope is $\frac1x$, so a change in $\ln x$ is a percentage change in $x$.
5. In BSM: $e^{-rT}$ discounts, $\ln(S/K)$ measures moneyness, prices are $e^{(\text{normal})}$, and the convexity of $e^x$ produces the $\tfrac12\sigma^2$ terms.

---

# Check Your Understanding

**1. Why does compounding more often increase the final amount, but never past $e^r$?**
Interest starts earning interest sooner. But each refinement adds less, and the values approach the limit $e^r$ from below.

**2. A stock goes from 50 to 60, then from 60 to 45. What's the total log return, computed two ways?**
Directly, $\ln\frac{45}{50} = -0.1054$. As a sum, $\ln\frac{60}{50} + \ln\frac{45}{60} = 0.1823 - 0.2877 = -0.1054$, the same, by L1.

**3. Why is the slope of $3^x$ at $x = 0$ equal to $\ln 3$?**
$3^x = e^{x\ln3}$, and the chain rule gives slope $\ln 3 \cdot e^{x\ln3}$. At $x = 0$ that's $\ln 3 = 1.099$.

**4. In $d_1$, why measure moneyness as $\ln(S/K)$ instead of $S - K$?**
The model's randomness is in log returns, so log distance is the natural unit. It's also scale-free: a \$10 gap means much more on a \$20 stock than on a \$2,000 stock, but $\ln(S/K)$ treats equal ratios equally.

---

# Vocabulary

```text
Base:                 The number being raised to a power; in b^x, b is the base.
Compounding:          Earning interest on previously earned interest.
Continuous compounding: The limit of compounding infinitely often; grows $1 to e^(rT).
Discount factor:      e^(-rT); converts money at time T into money today.
e:                    2.71828..., the limit of (1 + 1/n)^n; the base whose exponential is its own slope.
Factorial (k!):       1 x 2 x ... x k, with 0! = 1.
Forward price:        F = S e^(rT), the stock price grown at the risk-free rate.
ln (natural log):     The inverse of e^x: ln(x) is the power of e that gives x.
Log return:           ln(S1/S0), the continuously compounded growth rate between two prices.
Lognormal:            A variable whose log is normally distributed.
```
