# A Markdown security policy, an AI review, and a merge gate

An intentionally small **GitHub Agentic Workflows** teaching demo. Copilot reads
the PR and [our two-rule security standard](SECURITY_STANDARD.md), then the
framework's built-in `create-check-run` handler publishes **Security review**.
A main-branch ruleset requires that result, not merely a successful workflow.

**Synthetic data only. Do not deploy this application. The intentionally unsafe
feature branch is an educational example, not production-ready code.**

## Which GitHub features do what?

| Feature | Role in this demo |
|---|---|
| **GitHub Agentic Workflows (`gh-aw`)** | GitHub's open-source framework, compiler, and runtime. Compiles our Markdown instructions plus YAML frontmatter into an Actions `.lock.yml` workflow. Its built-in safe-output `create-check-run` handler publishes the verdict without a custom reporter. |
| **Copilot CLI / engine** | Performs the LLM reasoning: reads candidate code against `SECURITY_STANDARD.md` and decides which policy findings to report. |
| **GitHub Actions** | Responds to PR events, orchestrates jobs on hosted runners, and supplies job permissions and the per-run `GITHUB_TOKEN`. Copilot entitlement and usage/billing requirements still apply; see prerequisites below. |
| **GitHub Checks** | Displays the named **Security review** success/failure and explanation on the PR's commit. A successful workflow execution is **not** necessarily a passing security verdict. |
| **Branch ruleset: required status check** | **Enforces the merge gate.** Requires **Security review** from the configured publishing App before merging to `main`, alongside the other rules. Neither Markdown nor the agent alone blocks merges; PR creation remains allowed. |
| **Our repository-authored configuration** | Supplies the policy, review instructions/frontmatter, sample app, and demo settings. Generated lock YAML and framework machinery are not hand-maintained custom gate code. |

**Flow:** PR -> Actions / Agentic Workflow -> Copilot policy review ->
native **Security review** check -> ruleset permits or blocks merge.

### Is this out of the box?

**Existing building blocks, yes; a zero-configuration policy gate, no.** This
uses GitHub features and a framework-provided output handler, with no custom
`.mjs` detector, parser, or reporter. It is not an automatically enabled or
one-toggle Copilot feature that enforces arbitrary Markdown security policies.
We install and compile `gh-aw`, configure the workflow and model access, author
the policy, and configure the required-check ruleset.

This is **not ordinary Copilot code-review comments, CodeQL, or Copilot
Autofix**. It is a configured agentic policy review feeding a native merge
requirement, with the trusted-writer scope and limitations documented below.

## Presenter walkthrough

1. Show `SECURITY_STANDARD.md`, then `directory.py`: a Python standard-library
   SQLite directory with three made-up employees and no network service.
2. Open [safe search PR #1](https://github.com/ShawnMcGough/agentic-security-gate-demo/pull/1)
   and [unsafe search PR #2](https://github.com/ShawnMcGough/agentic-security-gate-demo/pull/2).
   Both add the same exact-name search feature: `demo/safe-search` binds the
   name as a SQL parameter; `demo/unsafe-search` interpolates it into SQL.
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
- The framework keeps its firewall, threat detection, and output safety
  defaults. Its separate output/conclusion jobs receive `checks: write`;
  framework diagnostics also receive `issues: write`. The agent receives only
  read access plus permission to request Copilot inference.
- **Explicit, approved demo trade-off:** GitHub reads use `min-integrity: none`
  with an allowlist containing only this repository. The released framework
  labels PR diffs as untrusted even for the owner, so its public-repo default
  (`approved`) blocks code review. This exception lets the model inspect
  untrusted source; it does not authorize executing it or following embedded
  instructions. Do not copy this setting into a broader repository allowlist.
  A filtered read must still fail rather than be routed through another endpoint.
- The active main ruleset requires a PR and **Security review** from the
  observed publishing GitHub App, with no bypass actors, force pushes, or
  deletion. Branches must be up to date with main before merging. PR creation
  remains allowed; merging is the boundary.
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
[Copilot CLI in Actions](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli-in-actions),
[required status checks in rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-status-checks-to-pass).
