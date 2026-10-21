# Taylor Series

## Learning Goal

Understand how a complicated function can be rebuilt from simple pieces (a constant, a straight line, a parabola, and so on) using only what you know at one point. Then see why that idea is behind almost everything in option risk: delta and gamma, P&L attribution, Itô's lemma, and quick pricing rules of thumb.

The path:

```text
1. Series in general         adding infinitely many numbers; the geometric series
2. When series add up        convergence, and a series that doesn't
3. Power series              functions as "infinite polynomials"
4. Taylor's formula          where the coefficients f^(k)(a)/k! come from
5. Worked series             e^x, ln(1+x), 1/(1-x), N(x)
6. How good is a cut-off     the error term, proved
7. Two variables             price and time together
8. Options theory            Greeks, P&L explain, gamma, Ito, BSM shortcuts
```

Prerequisites: derivatives (power rule, chain rule), the integral as area, and `e_and_ln.md`.

---

# 1. Series: Adding Infinitely Many Numbers

**The problem.** Section 3 of `e_and_ln.md` wrote $e$ as $1 + 1 + \frac{1}{2!} + \frac{1}{3!} + \cdots$, a sum that never ends. What does it even mean to add infinitely many numbers? We need that idea before Taylor series make sense.

### Sequences, series, partial sums

- A **sequence** is a list of numbers: $a_0, a_1, a_2, \ldots$
- A **series** is what you get by adding the list: $a_0 + a_1 + a_2 + \cdots$, written $\sum_{k=0}^{\infty} a_k$.
- A **partial sum** $S_n$ adds just the first terms, through $a_n$: $S_n = a_0 + a_1 + \cdots + a_n$.

The value of an infinite series is *defined* as the limit of its partial sums: keep adding terms, and see whether the running total settles down to a number.

### The geometric series

Each term is the previous one times a fixed ratio $x$:

$$1 + x + x^2 + x^3 + \cdots$$

**Example, $x = \tfrac12$.** Add terms one at a time:

| $n$ | New term $x^n$ | Partial sum $S_n$ |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 0.5 | 1.5 |
| 2 | 0.25 | 1.75 |
| 3 | 0.125 | 1.875 |
| 4 | 0.0625 | 1.9375 |
| 5 | 0.03125 | 1.96875 |

The totals close in on 2. Each new term covers half the remaining gap, like walking halfway to a wall over and over.

### Proof of the formula

**Step 1.** Write the partial sum:

$$S_n = 1 + x + x^2 + \cdots + x^n$$

**Step 2.** Multiply every term by $x$:

$$x\,S_n = x + x^2 + x^3 + \cdots + x^{n+1}$$

**Step 3.** Subtract Step 2 from Step 1. Every term from $x$ through $x^n$ appears in both and cancels. Only the 1 from the first line and the $x^{n+1}$ from the second survive:

$$S_n - x\,S_n = 1 - x^{n+1}$$

**Step 4.** Factor the left side as $S_n(1 - x)$, then divide by $(1 - x)$, assuming $x \ne 1$:

$$S_n = \frac{1 - x^{n+1}}{1 - x}$$

**Step 5.** Let $n \to \infty$. If $-1 < x < 1$, then $x^{n+1}$ shrinks to 0 (for example $0.5^{11} = 0.0005$). So

$$\boxed{1 + x + x^2 + x^3 + \cdots = \frac{1}{1 - x}, \qquad -1 < x < 1}$$

**Checks.**

- $x = \tfrac12$: $\frac{1}{1 - 0.5} = \frac{1}{0.5} = 2$. Matches the table. ✓
- $x = -\tfrac12$: partial sums $1, 0.5, 0.75, 0.625, 0.6875, \ldots$ zigzag toward $\frac{1}{1.5} = 0.6667$. ✓
- $x = 2$: $1 + 2 + 4 + 8 + \cdots$ grows without bound. The formula would say $\frac{1}{1-2} = -1$, which is nonsense. The formula only holds for $-1 < x < 1$, because only then does $x^{n+1} \to 0$ in Step 5.

### A finance example: a perpetuity

A **perpetuity** pays $c$ dollars every year forever. At yield $y$, a payment $k$ years away is worth $\frac{c}{(1+y)^k}$ today. The total value is

$$PV = \frac{c}{1+y} + \frac{c}{(1+y)^2} + \frac{c}{(1+y)^3} + \cdots$$

**Step 1.** Let $x = \frac{1}{1+y}$. Then $PV = c\,(x + x^2 + x^3 + \cdots)$.

**Step 2.** Factor out one $x$: $x + x^2 + \cdots = x\,(1 + x + x^2 + \cdots) = \frac{x}{1 - x}$, by the geometric formula.

**Step 3.** Simplify. $1 - x = 1 - \frac{1}{1+y} = \frac{1 + y - 1}{1+y} = \frac{y}{1+y}$. So

$$\frac{x}{1 - x} = \frac{\frac{1}{1+y}}{\frac{y}{1+y}} = \frac{1}{y}$$

**Result:** $PV = \frac{c}{y}$. With $c = \$5$ and $y = 5\%$: $PV = \frac{5}{0.05} = \$100$. An infinite stream of payments has a finite price, because the far-off payments are worth almost nothing.

**High level:** an infinite sum can have a perfectly finite value, as long as the terms shrink fast enough. The geometric series is the simplest case, and it shows up again inside Taylor series.

---

# 2. When Does a Series Add Up?

A series **converges** if its partial sums settle on a number, and **diverges** if they don't.

**Requirement: the terms must shrink to 0.** If the terms stayed at, say, 0.01 forever, each one would add another 0.01, and the total would grow without limit.

**But shrinking terms are not enough.** The **harmonic series**

$$1 + \frac12 + \frac13 + \frac14 + \frac15 + \cdots$$

has terms that shrink to 0, yet it diverges.

**Proof by grouping.** Group the terms in blocks whose sizes double: 1 term, then 1, then 2, then 4, then 8, and so on:

$$1 + \frac12 + \left(\frac13 + \frac14\right) + \left(\frac15 + \frac16 + \frac17 + \frac18\right) + \cdots$$

In each bracket, every term is at least as big as the bracket's last term. So:

- $\frac13 + \frac14 \ge \frac14 + \frac14 = \frac12$
- $\frac15 + \frac16 + \frac17 + \frac18 \ge 4 \times \frac18 = \frac12$
- The next block, $\frac19$ through $\frac1{16}$, has 8 terms each at least $\frac1{16}$, so it adds at least $8 \times \frac{1}{16} = \frac12$.

Every block adds at least $\frac12$, and there are infinitely many blocks. Infinitely many halves add up to infinity.

**With numbers:** 1, 2, 4, 8, 16 and 1000 terms give partial sums 1.00, 1.50, 2.08, 2.72, 3.38 and 7.49. The total does grow forever, just very slowly. (It grows like $\ln n$: $\ln 1000 + 0.577 = 7.485$. That's no coincidence. $\ln x$ is the area under $\frac1t$ from 1 to $x$, and the harmonic sum is a staircase version of that area.)

**The contrast with $e$:** $\sum \frac{1}{k!}$ converges because factorials grow much faster than $k$. Its terms shrink fast enough. Terms like $\frac1k$ don't.

**High level:** to use an infinite series, check it converges, and usually for which inputs. The geometric series converges only for $-1 < x < 1$. That kind of restriction will come back with $\ln(1 + x)$.

---

# 3. Power Series: Functions as Infinite Polynomials

**The problem.** Polynomials like $3 + 2x - x^2$ are the easiest functions there are: you can evaluate them with just multiplication and addition, and differentiate them term by term with the power rule. Functions like $e^x$ and $\ln x$ are harder. Can we write a hard function as a polynomial with infinitely many terms?

A **power series** is a series whose terms are powers of $x$:

$$c_0 + c_1 x + c_2 x^2 + c_3 x^3 + \cdots = \sum_{k=0}^{\infty} c_k x^k$$

The numbers $c_k$ are the **coefficients**.

We've already seen one. The geometric series says

$$\frac{1}{1 - x} = 1 + x + x^2 + x^3 + \cdots \qquad (-1 < x < 1)$$

The left side is a hard-ish function. The right side is a power series with every $c_k = 1$. For $|x| < 1$ they're equal.

**The question for Section 4:** given any smooth function $f$, how do we find its coefficients $c_k$?

---

# 4. Taylor's Formula: Where the Coefficients Come From

### Step 1: assume a power series exists, and match values

Suppose

$$f(x) = c_0 + c_1 x + c_2 x^2 + c_3 x^3 + c_4 x^4 + \cdots$$

Plug in $x = 0$. Every term with an $x$ in it becomes 0:

$$f(0) = c_0$$

So $c_0 = f(0)$.

### Step 2: differentiate once, match slopes

Differentiate term by term with the power rule $\frac{d}{dx}x^k = k\,x^{k-1}$:

$$f'(x) = c_1 + 2c_2 x + 3c_3 x^2 + 4c_4 x^3 + \cdots$$

Plug in $x = 0$:

$$f'(0) = c_1$$

So $c_1 = f'(0)$.

### Step 3: differentiate again, match curvature

$$f''(x) = 2c_2 + 3\cdot2\,c_3 x + 4\cdot3\,c_4 x^2 + \cdots$$

Plug in $x = 0$: $f''(0) = 2c_2$. Divide by 2:

$$c_2 = \frac{f''(0)}{2}$$

### Step 4: once more

$$f'''(x) = 3\cdot2\cdot1\,c_3 + 4\cdot3\cdot2\,c_4 x + \cdots$$

Plug in $x = 0$: $f'''(0) = 3\cdot2\cdot1\,c_3 = 6\,c_3$. So

$$c_3 = \frac{f'''(0)}{6} = \frac{f'''(0)}{3!}$$

### The pattern

Differentiating $x^k$ a total of $k$ times gives $k \cdot (k-1) \cdots 2 \cdot 1 = k!$, and plugging in 0 wipes out every other term. So

$$c_k = \frac{f^{(k)}(0)}{k!}$$

where $f^{(k)}$ means the $k$-th derivative ($f^{(0)} = f$ itself).

$$\boxed{f(x) = f(0) + f'(0)\,x + \frac{f''(0)}{2!}x^2 + \frac{f'''(0)}{3!}x^3 + \cdots = \sum_{k=0}^{\infty}\frac{f^{(k)}(0)}{k!}x^k}$$

This is the **Taylor series of $f$ around 0** (also called the **Maclaurin series**).

### Around any point $a$

Usually we know $f$ well at some point $a$, like today's stock price, and want $f$ nearby. Repeat Steps 1–4 with powers of $(x - a)$ instead of $x$, plugging in $x = a$ instead of 0. The same argument gives

$$f(x) = \sum_{k=0}^{\infty}\frac{f^{(k)}(a)}{k!}(x - a)^k$$

Writing $h = x - a$ for the step away from $a$:

$$\boxed{f(a + h) = f(a) + f'(a)\,h + \frac{f''(a)}{2}h^2 + \frac{f'''(a)}{6}h^3 + \cdots}$$

**Read it as successive corrections:**

| Order | Term | What it captures |
|---|---|---|
| 0 | $f(a)$ | the starting value |
| 1 | $f'(a)\,h$ | the slope: "it's moving this fast" |
| 2 | $\frac12 f''(a)\,h^2$ | the curvature: "and the slope is changing" |
| 3 | $\frac16 f'''(a)\,h^3$ | the change in curvature |

Stopping after the $h^n$ term gives the **$n$-th order Taylor approximation** (or Taylor polynomial).

**High level:** everything about $f$ near $a$ is encoded in its derivatives at $a$. The value, slope and curvature at one point are often enough to predict nearby values very accurately.

---

# 5. Worked Series

### $e^x$

Every derivative of $e^x$ is $e^x$ (`e_and_ln.md`, Section 5). At 0, each is $e^0 = 1$. So every coefficient is $\frac{1}{k!}$:

$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \cdots$$

At $x = 1$ this is $e = 1 + 1 + \frac12 + \frac16 + \cdots$, the series from `e_and_ln.md`.

**Compute $e^{0.5}$:**

| Terms through | New term | Running total |
|---|---|---|
| $1$ | 1 | 1 |
| $x$ | 0.5 | 1.5 |
| $\frac{x^2}{2}$ | $\frac{0.25}{2} = 0.125$ | 1.625 |
| $\frac{x^3}{6}$ | $\frac{0.125}{6} = 0.020833$ | 1.645833 |
| $\frac{x^4}{24}$ | $\frac{0.0625}{24} = 0.002604$ | 1.648438 |
| $\frac{x^5}{120}$ | $\frac{0.03125}{120} = 0.000260$ | 1.648698 |
| exact | | 1.648721 |

Six terms give five correct digits. This series converges for every $x$, because $k!$ eventually beats $x^k$ however big $x$ is.

### $\ln(1 + x)$

Take derivatives of $f(x) = \ln(1+x)$, using $\frac{d}{dx}\ln(1+x) = \frac{1}{1+x}$ and then the power rule on $(1+x)^{-1}$:

| $k$ | $f^{(k)}(x)$ | $f^{(k)}(0)$ | $c_k = \frac{f^{(k)}(0)}{k!}$ |
|---|---|---|---|
| 0 | $\ln(1+x)$ | 0 | 0 |
| 1 | $(1+x)^{-1}$ | 1 | $\frac11 = 1$ |
| 2 | $-(1+x)^{-2}$ | −1 | $\frac{-1}{2} = -\frac12$ |
| 3 | $2(1+x)^{-3}$ | 2 | $\frac{2}{6} = \frac13$ |
| 4 | $-6(1+x)^{-4}$ | −6 | $\frac{-6}{24} = -\frac14$ |

The pattern: $c_k = \frac{(-1)^{k+1}}{k}$. So

$$\ln(1 + x) = x - \frac{x^2}{2} + \frac{x^3}{3} - \frac{x^4}{4} + \cdots \qquad (-1 < x \le 1)$$

**Compute $\ln(1.1)$**, so $x = 0.1$:

| Terms through | New term | Running total |
|---|---|---|
| $x$ | 0.1 | 0.1 |
| $-\frac{x^2}{2}$ | $-\frac{0.01}{2} = -0.005$ | 0.095 |
| $+\frac{x^3}{3}$ | $\frac{0.001}{3} = 0.000333$ | 0.095333 |
| $-\frac{x^4}{4}$ | $-\frac{0.0001}{4} = -0.000025$ | 0.095308 |
| exact | | 0.095310 |

**Another route to the same series**, through the geometric series. Replace $x$ with $-x$ in $\frac{1}{1-x} = 1 + x + x^2 + \cdots$:

$$\frac{1}{1 + x} = 1 - x + x^2 - x^3 + \cdots$$

The left side is the derivative of $\ln(1+x)$. Integrate both sides from 0 to $x$, term by term, using $\int_0^x t^k\,dt = \frac{x^{k+1}}{k+1}$:

$$\ln(1 + x) - \ln 1 = x - \frac{x^2}{2} + \frac{x^3}{3} - \cdots$$

Since $\ln 1 = 0$, that's the same series. It also explains the restriction: it inherits the geometric series' need for $|x| < 1$. Plug in $x = 2$ and the terms $2, -2, 2.67, -4, \ldots$ blow up, even though $\ln 3 = 1.0986$ is perfectly finite. **A Taylor series can describe a function only within a certain distance of the expansion point.**

### $\frac{1}{1-x}$: Taylor recovers the geometric series

$f(x) = (1-x)^{-1}$. Derivatives by the chain rule: $f' = (1-x)^{-2}$, $f'' = 2(1-x)^{-3}$, $f''' = 6(1-x)^{-4}$, and in general $f^{(k)} = k!\,(1-x)^{-(k+1)}$. At 0, $f^{(k)}(0) = k!$, so $c_k = \frac{k!}{k!} = 1$. That gives $1 + x + x^2 + \cdots$, the geometric series. Two completely different methods agree.

### The normal CDF $N(x)$ near 0

$N(x)$ is the standard normal CDF (the area under the bell curve to the left of $x$). Its derivative is the density: $N'(x) = n(x) = \frac{1}{\sqrt{2\pi}}e^{-x^2/2}$.

- $N(0) = 0.5$ (half the area is left of center).
- $N'(0) = n(0) = \frac{1}{\sqrt{2\pi}} = 0.3989$.
- $N''(x) = n'(x)$. By the chain rule, $\frac{d}{dx}e^{-x^2/2} = -x\,e^{-x^2/2}$, so $n'(x) = -x\,n(x)$, and $N''(0) = 0$.

So near 0, with no second-order term:

$$N(x) \approx 0.5 + 0.3989\,x$$

Check: $N(0.1) \approx 0.5 + 0.03989 = 0.53989$. The exact value is 0.53983. Section 8.6 uses this to derive a famous trading shortcut.

---

# 6. How Good Is a Cut-Off Series? The Error Term

**The problem.** In practice we stop after a few terms. How big is the error from the terms we dropped?

### See it with numbers

Approximate $e^h$ by its first- and second-order Taylor polynomials, $1 + h$ and $1 + h + \frac{h^2}{2}$:

| $h$ | Error of $1 + h$ | Error of $1 + h + \frac{h^2}{2}$ |
|---|---|---|
| 0.1 | 0.005171 | 0.000171 |
| 0.05 | 0.001271 | 0.0000211 |
| Ratio when $h$ halves | $\div 4.07$ | $\div 8.10$ |

Halving $h$ cuts the first-order error by about 4 ($= 2^2$), and the second-order error by about 8 ($= 2^3$). So the first-order error behaves like $h^2$ and the second-order error like $h^3$. **The error is about the size of the first term you dropped.**

### Proof: the exact error of a second-order approximation

We'll derive an exact formula for the error and then bound it. Take $h > 0$, and assume $f$ has three continuous derivatives.

**Tool 1, the Fundamental Theorem of Calculus:** integrating a derivative gives back the total change.

$$f(a + h) - f(a) = \int_0^h f'(a + s)\,ds$$

(Here $s$ runs from 0 to $h$, and $\frac{d}{ds}f(a+s) = f'(a+s)$.)

**Tool 2, integration by parts:** $\int_0^h u\,dv = \Big[u\,v\Big]_0^h - \int_0^h v\,du$.

**Step 1: get the first-order term.** In $\int_0^h f'(a+s)\,ds$, choose

- $u = f'(a + s)$, so $du = f''(a + s)\,ds$
- $dv = ds$, and pick $v = -(h - s)$. (Check: $\frac{dv}{ds} = 1$. ✓ This particular choice makes $v = 0$ at $s = h$, which simplifies the boundary term.)

Boundary term: at $s = h$, $v = 0$; at $s = 0$, $v = -h$. So

$$\Big[u\,v\Big]_0^h = f'(a+h)\cdot 0 - f'(a)\cdot(-h) = f'(a)\,h$$

Integral term: $-\int_0^h v\,du = -\int_0^h -(h - s)\,f''(a+s)\,ds = \int_0^h (h - s)\,f''(a+s)\,ds$.

Put together with Tool 1:

$$f(a + h) = f(a) + f'(a)\,h + \int_0^h (h - s)\,f''(a+s)\,ds$$

The integral is the **exact** error of the first-order approximation.

**Step 2: get the second-order term.** Integrate by parts again, with

- $u = f''(a + s)$, so $du = f'''(a + s)\,ds$
- $dv = (h - s)\,ds$, and pick $v = -\frac{(h-s)^2}{2}$. (Check: $\frac{d}{ds}\left[-\frac{(h-s)^2}{2}\right] = -\frac{2(h-s)\cdot(-1)}{2} = h - s$. ✓)

Boundary term:

$$\Big[u\,v\Big]_0^h = f''(a+h)\cdot0 - f''(a)\cdot\left(-\frac{h^2}{2}\right) = \frac{f''(a)}{2}h^2$$

Integral term: $-\int_0^h v\,du = \int_0^h \frac{(h-s)^2}{2}\,f'''(a+s)\,ds$.

Substitute back into Step 1's result:

$$\boxed{f(a + h) = f(a) + f'(a)\,h + \frac{f''(a)}{2}h^2 + R_2}, \qquad R_2 = \int_0^h \frac{(h-s)^2}{2}\,f'''(a+s)\,ds$$

This proves the second-order Taylor formula, with an exact expression for the error $R_2$.

**Step 3: bound the error.** Suppose $|f'''| \le M$ everywhere between $a$ and $a + h$. Then

$$|R_2| \le M\int_0^h \frac{(h-s)^2}{2}\,ds$$

Compute the integral. An antiderivative of $(h - s)^2$ is $-\frac{(h-s)^3}{3}$ (differentiate it to check). So

$$\int_0^h (h-s)^2\,ds = \left[-\frac{(h-s)^3}{3}\right]_0^h = 0 - \left(-\frac{h^3}{3}\right) = \frac{h^3}{3}$$

Divide by 2 for the $\frac12$:

$$|R_2| \le M\,\frac{h^3}{6}$$

**The error of a second-order approximation is at most (biggest third derivative) × $h^3$ / 6.** That's why the error shrinks by a factor of 8 when $h$ halves, as in the table.

**Check with $e^h$ at $h = 0.1$.** Here $f''' = e^{s}$, which is at most $e^{0.1} = 1.10517$ on $[0, 0.1]$. Bound: $1.10517 \times \frac{0.001}{6} = 0.000184$. Actual error from the table: 0.000171. Below the bound. ✓

**High level:** a Taylor approximation is excellent for small steps and gets worse as the step grows, at a rate you can predict. In options terms: delta and gamma describe small stock moves very well and large ones poorly (Section 8.3).

---

# 7. Two Variables: Price and Time Together

An option's value depends on both the stock price $S$ and time $t$. We need Taylor for a function of two variables, $f(x, y)$, stepping by $h$ in $x$ and $k$ in $y$.

### Reduce it to one variable

Walk in a straight line from $(x, y)$ to $(x + h, y + k)$. Define

$$g(s) = f(x + sh,\ y + sk)$$

so $g(0) = f(x, y)$ is the start and $g(1) = f(x + h, y + k)$ is the end. $g$ is a function of the single variable $s$, so the one-variable result applies, with step 1:

$$g(1) \approx g(0) + g'(0) + \tfrac12 g''(0)$$

### Compute $g'$ and $g''$ by the chain rule

Write $f_x = \frac{\partial f}{\partial x}$, $f_{xy} = \frac{\partial^2 f}{\partial x\,\partial y}$, and so on. As $s$ increases, $x$ moves at speed $h$ and $y$ at speed $k$, so

$$g'(s) = f_x\,h + f_y\,k$$

Differentiate again. Each of $f_x$ and $f_y$ itself changes in both directions:

$$g''(s) = \big(f_{xx}h + f_{xy}k\big)h + \big(f_{yx}h + f_{yy}k\big)k = f_{xx}h^2 + 2f_{xy}hk + f_{yy}k^2$$

(For smooth functions, $f_{xy} = f_{yx}$: the order of differentiation doesn't matter.)

### Result

Put $s = 0$ and substitute:

$$\boxed{f(x + h,\ y + k) \approx f + f_x h + f_y k + \tfrac12\left(f_{xx}h^2 + 2f_{xy}hk + f_{yy}k^2\right)}$$

with every derivative evaluated at the starting point $(x, y)$.

**Check with $f(x, y) = xy$.** Exactly, $(x + h)(y + k) = xy + yh + xk + hk$. Derivatives: $f_x = y$, $f_y = x$, $f_{xx} = 0$, $f_{yy} = 0$, $f_{xy} = 1$. Taylor gives $xy + yh + xk + \tfrac12(2hk) = xy + yh + xk + hk$. Exact. ✓

---

# 8. How This Shows Up in Options Theory

Running example (from `../options_theory/bsm_primer.md`, Part 7): a 1-year at-the-money call with $S = 100$, $K = 100$, $r = 5\%$, $\sigma = 20\%$. Its value and Greeks:

| Quantity | Value |
|---|---|
| Call value $C$ | 10.4506 |
| Delta $\Delta = \frac{\partial C}{\partial S}$ | 0.6368 |
| Gamma $\Gamma = \frac{\partial^2 C}{\partial S^2}$ | 0.01876 |
| Theta $\Theta = \frac{\partial C}{\partial t}$ | −6.414 per year |
| Vega $\mathcal V = \frac{\partial C}{\partial \sigma}$ | 37.52 per 1.00 of vol (0.3752 per vol point) |

### 8.1 The Greeks are Taylor coefficients

Apply the multi-variable Taylor expansion to $C(S, t, \sigma)$, keeping the important terms:

$$\delta C \approx \underbrace{\Delta\,\delta S}_{\text{delta}} + \underbrace{\tfrac12\Gamma\,(\delta S)^2}_{\text{gamma}} + \underbrace{\Theta\,\delta t}_{\text{theta}} + \underbrace{\mathcal V\,\delta\sigma}_{\text{vega}}$$

Delta, gamma, theta and vega are nothing more than the coefficients in this expansion. Desks use exactly this to explain each day's P&L (**P&L attribution**, or "P&L explain").

**Scenario:** one trading day passes ($\delta t = \frac{1}{252}$), the stock rises \$2, and implied vol rises one point ($\delta\sigma = 0.01$).

| Term | Calculation | Value |
|---|---|---|
| Delta | $0.6368 \times 2$ | $+1.2737$ |
| Gamma | $\tfrac12 \times 0.01876 \times 2^2$ | $+0.0375$ |
| Theta | $-6.414 \times \frac{1}{252}$ | $-0.0255$ |
| Vega | $37.52 \times 0.01$ | $+0.3752$ |
| **Taylor total** | | **+1.6610** |
| Exact repricing | $12.1034 - 10.4506$ | +1.6528 |

The expansion explains the day's P&L to within a cent. The small leftover comes from cross terms we dropped, like $\frac{\partial^2 C}{\partial S\,\partial\sigma}\,\delta S\,\delta\sigma$ (called **vanna**).

### 8.2 Why gamma is the interesting term

The gamma term $\tfrac12\Gamma(\delta S)^2$ contains $(\delta S)^2$, which is positive whether the stock goes up or down. If you hedge away the delta term by shorting $\Delta$ shares, gamma is what's left:

- Stock $+2$: gamma term $= \tfrac12(0.01876)(4) = +0.0375$
- Stock $-2$: gamma term $= \tfrac12(0.01876)(4) = +0.0375$

A long option position makes money on moves in either direction, and pays theta for the privilege. That trade-off is the core of volatility trading (primer, Part 9).

### 8.3 When the approximation breaks: big moves

From Section 6, the error grows like the cube of the step. Try large stock moves with the second-order approximation $C + \Delta h + \tfrac12\Gamma h^2$:

| Stock moves to | Taylor estimate | Exact BSM | Error |
|---|---|---|---|
| 102 | 11.7618 | 11.7611 | 0.0007 |
| 120 | $10.4506 + 12.7366 + 3.7524 = 26.94$ | 26.17 | 0.77 |
| 80 | $10.4506 - 12.7366 + 3.7524 = 1.47$ | 1.86 | −0.39 |

For a \$2 move the error is a tenth of a cent. For a \$20 move it's tens of cents. Gamma itself changes as the stock moves, so a single gamma number can't describe a big move. This is why risk managers also run full-repricing **scenario** tests for crashes and gaps, not just Greeks.

### 8.4 Itô's lemma is a second-order Taylor expansion

Expand the option value $V(S, t)$ with Section 7's formula, with $h = dS$ and $k = dt$:

$$dV \approx V_t\,dt + V_S\,dS + \tfrac12 V_{SS}(dS)^2 + V_{St}\,dS\,dt + \tfrac12 V_{tt}(dt)^2$$

In ordinary calculus you'd drop $(dS)^2$ as tiny. But a stock's move over time $dt$ has size about $\sqrt{dt}$, so $(dS)^2$ is about $dt$ in size: the same order as terms we keep. Precisely, $(dS)^2 = \sigma^2S^2\,dt$, while $dS\,dt$ and $(dt)^2$ really are negligible. Keeping only the survivors gives **Itô's lemma**:

$$dV = V_t\,dt + V_S\,dS + \tfrac12\sigma^2S^2\,V_{SS}\,dt$$

The full derivation is in the primer, Part 3.

### 8.5 The theta–gamma trade-off

Itô's lemma plus delta hedging leads to the Black-Scholes equation (primer, Part 5). With interest rates set to zero it says

$$\Theta = -\tfrac12\sigma^2S^2\,\Gamma$$

In Taylor language: on a day when the stock moves exactly as much as implied volatility predicts, the gamma term gained exactly cancels the theta lost. Make more than that from gamma and the hedged option makes money; less, and it loses (primer, Part 9).

### 8.6 Deriving a trading shortcut: an at-the-money call is about $0.4\,S\,\sigma\sqrt{T}$

Traders estimate at-the-money option prices in their heads. Here's where the rule comes from.

**Setup.** At the money ($K = S$) with $r = 0$, the BSM formula $C = S\,N(d_1) - K e^{-rT}N(d_2)$ simplifies.

1. $\ln\frac{S}{K} = \ln 1 = 0$ and $r = 0$, so

$$d_1 = \frac{0 + \tfrac12\sigma^2T}{\sigma\sqrt T} = \tfrac12\sigma\sqrt T, \qquad d_2 = d_1 - \sigma\sqrt T = -\tfrac12\sigma\sqrt T$$

2. With $K = S$ and $e^{-rT} = 1$:

$$C = S\left[N\left(\tfrac12\sigma\sqrt T\right) - N\left(-\tfrac12\sigma\sqrt T\right)\right]$$

3. Use Section 5's expansion $N(x) \approx 0.5 + 0.3989\,x$ (accurate for small $x$; the next term is $x^3$):

$$N\left(\tfrac12\sigma\sqrt T\right) \approx 0.5 + 0.3989\cdot\tfrac12\sigma\sqrt T$$
$$N\left(-\tfrac12\sigma\sqrt T\right) \approx 0.5 - 0.3989\cdot\tfrac12\sigma\sqrt T$$

4. Subtract. The 0.5s cancel, and the two halves add to a whole:

$$N\left(\tfrac12\sigma\sqrt T\right) - N\left(-\tfrac12\sigma\sqrt T\right) \approx 0.3989\,\sigma\sqrt T$$

5. Multiply by $S$:

$$\boxed{C_{\text{ATM}} \approx 0.3989\,S\,\sigma\sqrt{T} \approx 0.4\,S\,\sigma\sqrt T}$$

**Check** with $S = 100$, $\sigma = 20\%$:

| $T$ | Shortcut $0.3989 \times 100 \times 0.2 \times \sqrt T$ | Exact BSM ($r = 0$) |
|---|---|---|
| 1 month | 2.3033 | 2.3030 |
| 3 months | 3.9894 | 3.9878 |
| 1 year | 7.9788 | 7.9656 |
| 4 years | 15.9576 | 15.8519 |

Excellent for short-dated options, and slowly worse for long ones. That's exactly what Section 6 predicts, since the step $x = \tfrac12\sigma\sqrt T$ grows with $T$.

**What it teaches:** an at-the-money option's price is roughly **linear in volatility** and in $\sqrt{\text{time}}$. Double the vol, double the price. Four times the time, double the price.

### 8.7 Volatility drag from the second-order term of $\ln(1 + x)$

A stock's simple return over a period is $R$, with mean $\mu$ and standard deviation $\sigma$. Its log return is $\ln(1 + R)$. Expand to second order (Section 5):

$$\ln(1 + R) \approx R - \frac{R^2}{2}$$

Take averages of both sides. Averages add, so

$$E[\ln(1 + R)] \approx E[R] - \tfrac12 E[R^2]$$

Use $E[R^2] = \operatorname{Var}(R) + (E[R])^2 = \sigma^2 + \mu^2$. Over short periods $\mu^2$ is tiny next to $\sigma^2$ (for a day, roughly $0.0000002$ versus $0.00016$), so

$$E[\ln(1 + R)] \approx \mu - \tfrac12\sigma^2$$

**The typical compounded growth rate is the average return minus half the variance.** Check with returns of $+10\%$ and $-10\%$, so $\mu = 0$ and $\sigma = 0.10$: the formula predicts $-\tfrac12(0.01) = -0.005$ per period. Actual: $\frac{\ln(1.10) + \ln(0.90)}{2} = \frac{\ln 0.99}{2} = -0.00503$. ✓ This is the $\mu - \tfrac12\sigma^2$ in the BSM stock model (primer, Section 3.3).

---

# Recap

1. An infinite series means the limit of its partial sums. The geometric series $1 + x + x^2 + \cdots = \frac{1}{1-x}$ converges only for $|x| < 1$, and shrinking terms alone don't guarantee convergence.
2. Matching derivatives at a point forces the coefficients $\frac{f^{(k)}(a)}{k!}$. The $k!$ comes from differentiating $x^k$ $k$ times.
3. A cut-off Taylor series has an error about the size of the first dropped term. For second order it's at most $M h^3/6$, which was proved by integrating by parts twice.
4. The Greeks are the Taylor coefficients of the option price. P&L ≈ $\Delta\,\delta S + \tfrac12\Gamma(\delta S)^2 + \Theta\,\delta t + \mathcal V\,\delta\sigma$, and it works for small moves but not for big ones.
5. Itô's lemma is second-order Taylor plus the fact that $(dS)^2 \propto dt$. Taylor also gives the shortcut $C_{\text{ATM}} \approx 0.4\,S\sigma\sqrt T$ and the volatility drag $\mu - \tfrac12\sigma^2$.

---

# Check Your Understanding

**1. Why does the coefficient of $x^3$ contain $3! = 6$?**
Differentiating $c_3x^3$ three times gives $3\cdot2\cdot1\cdot c_3 = 6c_3$, and every other term vanishes at 0. Matching $f'''(0)$ forces $c_3 = f'''(0)/6$.

**2. The series for $\ln(1 + x)$ fails at $x = 2$, though $\ln 3$ exists. Why?**
The series comes from the geometric series for $\frac{1}{1+x}$, which needs $|x| < 1$. Beyond that the terms grow instead of shrinking.

**3. Your delta-gamma estimate is great for a \$1 move but off by \$0.77 for a \$20 move. Why?**
The error of a second-order approximation grows like the cube of the step. Gamma itself changes over a big move, which a single gamma number can't capture.

**4. Why does a delta-hedged long option profit from a big move in either direction?**
After the hedge removes $\Delta\,\delta S$, the main term left is $\tfrac12\Gamma(\delta S)^2$. It's positive for any nonzero move, because a square is never negative.

---

# Vocabulary

```text
Coefficient:          The number multiplying a power of x in a series.
Converge / diverge:   Partial sums settle on a number / don't.
Geometric series:     1 + x + x^2 + ...; equals 1/(1-x) when |x| < 1.
Harmonic series:      1 + 1/2 + 1/3 + ...; diverges even though its terms shrink.
Maclaurin series:     A Taylor series around 0.
Partial sum:          The total of the first n terms of a series.
P&L attribution:      Splitting a position's P&L into delta, gamma, theta, vega (and so on) pieces.
Power series:         A series of the form c0 + c1 x + c2 x^2 + ...
Remainder (R_n):      The error of an n-th order Taylor approximation.
Taylor polynomial:    A Taylor series cut off after the h^n term.
Taylor series:        f(a+h) = sum of f^(k)(a) h^k / k!; builds f from its derivatives at one point.
Vanna:                d^2C / dS dsigma; how delta changes with vol (a cross term).
```
