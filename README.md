# A Markdown security policy, an AI review, and a merge gate

An intentionally small **GitHub Agentic Workflows** teaching demo. Copilot reads
the PR and [our two-rule security standard](SECURITY_STANDARD.md), then the
framework's built-in `create-check-run` handler publishes **Security review**.
A main-branch ruleset requires that result, not merely a successful workflow.

**Synthetic data only. Do not deploy this application. The intentionally unsafe
feature branch is an educational example, not production-ready code.**

## Presenter walkthrough

1. Show `SECURITY_STANDARD.md`, then `directory.py`: a Python standard-library
   SQLite directory with three made-up employees and no network service.
2. Open the two [demo PRs](https://github.com/ShawnMcGough/agentic-security-gate-demo/pulls).
   Both add the same exact-name search feature:
   `demo/safe-search` binds the name as a SQL parameter;
   `demo/unsafe-search` interpolates it into SQL.
3. In each PR, open **Checks > Security review**. Read the model's policy
   reasoning and reviewed commit SHA. The safe PR should be merge-eligible;
   the unsafe PR should be blocked with a SQL-injection finding.
4. Show the [Agentic security gate runs](https://github.com/ShawnMcGough/agentic-security-gate-demo/actions)
   and the [main ruleset](https://github.com/ShawnMcGough/agentic-security-gate-demo/settings/rules).
   A framework run can succeed while its separate policy check fails.
   **Leave both PRs open and unmerged** so the comparison remains available.

## Files worth explaining

| Human-maintained file | Purpose |
|---|---|
| `directory.py` | Small, in-memory application |
| `test_directory.py` | Basic local smoke test; not the security gate |
| `SECURITY_STANDARD.md` | Two specific review rules |
| `.github/workflows/security-review.md` | Trigger, permissions, tools, review instructions, output |
| `README.md`, `.gitignore` | Walkthrough and Python housekeeping |

`.github/workflows/security-review.lock.yml`, `.github/aw/actions-lock.json`,
and `.gitattributes` are **generated framework configuration**, not a custom
checker or presenter-maintained implementation. Do not edit the locks by hand.
There is no custom parser, reporter, regex detector, or admin script.

## Local use and workflow maintenance

Requires Python 3 (no packages), GitHub Actions enabled, and a Copilot entitlement
with available usage/budget. Runs consume Actions resources and Copilot usage.
Inference uses the per-run `GITHUB_TOKEN` with `copilot-requests: write`; no
repository PAT or model API secret is part of this demo. For personally owned
repositories, Copilot usage is billed to the owner's eligible seat.

```shell
python directory.py
python -m unittest -v
```

On either feature branch, `python directory.py --name Ada` searches for Ada.
Only use synthetic input/data when demonstrating the unsafe branch.

To edit the workflow, use the released compiler used for this demo:

```shell
gh extension install github/gh-aw --pin v1.0.1
gh aw compile security-review
```

Commit the Markdown and all generated changes together. The release compiler
works natively on Windows; WSL is not needed for this demo's compilation.
Ordinary maintenance goes through a new PR and the same required check.
Workflow changes take effect after merging; PRs are reviewed with trusted
base-branch workflow and policy, not proposed replacements.

To repeat a review without changing code, open its Actions run and choose
**Re-run all jobs** (or `gh run rerun RUN_ID`). To review new code, push a commit
to the PR branch; `synchronize` starts a fresh review. Re-running an obsolete
event cannot approve a newer commit. If the PR moved since the event, the agent
is instructed to fail that old review; use the new commit's run instead.

## Trust boundaries and limitations

- Only same-repository PRs by trusted writers are admitted. `pull_request_target`
  loads the workflow from the base branch. Candidate code is read through
  read-only GitHub tools, never checked out or executed. Shell tools are disabled.
- The model reads policy at the event's base SHA and code at the event's head
  SHA. Omitting the check handler's `target` binds its output to that same
  immutable head, rather than looking up a possibly newer head at publish time.
- The framework keeps its firewall, integrity filtering, and output safety
  defaults. Its separate output/conclusion jobs receive `checks: write`;
  framework diagnostics also receive `issues: write`. The agent receives only
  read access plus permission to request Copilot inference.
- The active main ruleset requires a PR and **Security review** from the
  observed publishing GitHub App, with no bypass actors, force pushes, or
  deletion. PR creation remains allowed; merging is the boundary.
- **This is a trusted-maintainer teaching demo, not tamper-proof enforcement.**
  LLM findings can vary or miss vulnerabilities. The prompt requires success
  or failure, but the native handler also accepts neutral/skipped conclusions,
  which GitHub may consider passing. A prompt is not a deterministic constraint.
  App pinning identifies GitHub Actions, not this particular workflow; a
  malicious writer could spoof a same-name check through another workflow.
  Maintainers can change policy, workflows, or repository settings. Stronger
  production controls and human review are outside this small demo.
- A missing result or runtime failure is **not** a policy finding. Inspect the
  Actions logs and restore access/budget; never bypass the rules to simulate
  success. Missing required checks block merging.

References: [Agentic Workflows](https://github.github.com/gh-aw/),
[native check output](https://github.github.com/gh-aw/reference/safe-outputs/#check-run-creation-create-check-run),
[Copilot CLI in Actions](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-in-actions).
