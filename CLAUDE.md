# options_theory_and_math

Personal study notes for learning options theory (Black-Scholes-Merton, volatility trading) and the math underneath it. The reader has taken calculus and statistics but wants every idea built up slowly. The main companion text is Euan Sinclair, *Volatility Trading* (2nd ed., Wiley, 2013).

## Layout

```text
math/             general math and statistics lessons (variance, correlation, e and ln, Taylor series, ...)
options_theory/   options-specific lessons (bsm_primer.md, ...)
```

- One lesson per Markdown file, named in `snake_case.md`.
- Cross-link related lessons with relative links, e.g. `../math/taylor_series.md` from `options_theory/`.
- When a math lesson has an options application, end it with a section tying it to `options_theory/bsm_primer.md`, and vice versa.

## How to write math in this repo

The reader's main complaint about textbooks is skipped steps. These rules exist to prevent that. Follow them for every lesson and every edit.

### 1. Motivate before you formalize

Open each concept with **the problem** it solves, in plain words, before any notation. The reader should know why they're about to see an equation before they see it.

### 2. Concrete before abstract

Show a small numeric example first, then the pattern, then the general formula. Example: compound \$1 monthly for a year in a table, *then* write $\left(1 + \frac{r}{n}\right)^n$.

### 3. Define every term and symbol before using it

Never assume the reader knows a word, symbol or Greek letter. If a symbol has two meanings (e.g. $\Delta$ as "change in" vs. the Greek delta), say so explicitly.

### 4. One step per line, with the reason

In a derivation, each line does one thing, and the text says what and why:

```text
Bad:   x + 4 = 10  →  x = 6

Good:  x + 4 = 10
       Subtract 4 from both sides:
       x + 4 - 4 = 10 - 4
       x = 6
```

- Name the rule being used ("use $\ln(ab) = \ln a + \ln b$", "expand $(a+b)^2 = a^2 + 2ab + b^2$", "divide by $\sigma\sqrt T$, which is positive, so the inequality keeps its direction").
- Never write "it can be shown", "clearly", "obviously" or "after some algebra". Show it.
- When a step uses a fact from elsewhere, point to it ("from Section 1.4", "see `variance_covariance.md`").
- If a fact genuinely can't be proved at this level (e.g. $E[Z^4] = 3$), say that it's being taken as given and where it comes from.

### 5. Plug in numbers, step by step

After a formula, work at least one example with real numbers, showing each intermediate value. Number the steps when there are several. Use tables when comparing several inputs.

### 6. Check results

- Verify a derived formula numerically whenever possible ("check: $90.48 \times e^{0.10} = 100.00$ ✓").
- Compute every number in a lesson with a script (e.g. a short Python one-off in a scratch directory) before writing it down. Don't do arithmetic in your head.
- Reuse running examples across lessons so numbers can be cross-checked. The standard option example is $S = 100$, $K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$: $C = 10.4506$, $P = 5.5735$, $\Delta = 0.6368$, $\Gamma = 0.01876$, vega $= 37.52$ per 1.00 vol, $\Theta = -6.414$ per year.

### 7. Say what it means

End each concept with a short **High level:** paragraph: what the result says in plain words, and why a trader would care.

### 8. Lesson shape

For a substantial lesson: Learning Goal → sections (problem → example → derivation → numbers → high level) → connection to options → Recap → Check Your Understanding (questions with answers right below) → Vocabulary.

## Markdown and LaTeX formatting rules

Lessons use GitHub-flavored Markdown with LaTeX math. These rules keep the math rendering in GitHub, VS Code and the Claude app's file panel.

- Inline math: `$...$`. Display math: `$$...$$` on its own line, with blank lines around it.
- **Never put `$` math directly next to a quote mark.** `"$S$"` renders as raw text in some viewers. Rephrase instead.
- Literal dollar amounts are written `\$100`. Never write `\$$x$` (an escaped dollar touching math): use "an amount $X$" instead.
- Use `\lbrace` / `\rbrace` rather than `\{` / `\}` inside math.
- Code blocks tagged `text` are fine for ASCII diagrams and short pseudo-calculations.
- After editing, check that `$$` occurs an even number of times and that no line has an odd number of inline `$` outside display blocks.

## Workflow

- When you finish a change, commit and push to `main` on GitHub (`origin`). The owner has asked for this as standing practice.
- End commit messages with the attribution line the harness provides.
