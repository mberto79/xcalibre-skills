# <feature> — incorporation and structure

How this feature attaches to the code that already exists, and what it is made of. Read the host codebase BEFORE this file says anything: an incorporation written from the request alone is a guess.

## host survey

What is already there that this feature touches, read from the code and not from its documentation.

- **Entry points** — where the feature's behaviour will be reached from.
- **Components it touches** — each with what it currently owns.
- **Interfaces it must not break** — the contracts other code depends on, and how each is verified today (tests, gates, types, callers).
- **Conventions it must follow** — naming, layering, error handling, testing, as the surrounding code actually does them rather than as a style guide states them.

## attachment

Where the feature joins the existing shape, and why there rather than the alternatives considered. Name what would have to change if this attachment turns out wrong — that is the cost of the choice.

## shape

The feature's own components and what each owns, once built.

## flow

What enters and leaves each part, and the invariant each establishes.

## risks to the host

What this feature can break in code it did not write, and what makes each visible if it does.
