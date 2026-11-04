# Demo security standard

This short policy applies to application code in this synthetic teaching repo.

1. **Keep user input out of SQL text.** Bind every user-supplied SQL value using
   SQLite `?` placeholders and a separate parameter tuple. Never concatenate,
   interpolate, or format user input into a query, even if it is "validated."
2. **Treat input as data, not code.** Never pass user input to `eval`, `exec`,
   a shell command, or another dynamic code execution mechanism.

A review passes only when all changed application code follows both rules.
For a violation, identify the rule, file and line, explain the input-to-sink
path, and suggest the smallest safe change. Do not modify the PR.
