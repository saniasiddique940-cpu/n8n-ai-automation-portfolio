# Export routine (5 minutes per workflow)

Do this every time a workflow works, not at the end of the month.

1. **Download** the workflow from n8n (workflow menu > Download) into `raw/` (git-ignored).
2. **Sanitize:**
   ```bash
   python scripts/sanitize_workflow.py raw/my-flow.json workflows/my-flow/workflow.json
   ```
3. **Read the output.** Search it for names, phone numbers, client data and anything inside prompts.
4. **Document:** copy `docs/project-readme-template.md` to `workflows/my-flow/README.md` and fill every heading. Be honest in "Status".
5. **Check:** `python scripts/check_exports.py`
6. **Commit and push:**
   ```bash
   git add workflows/my-flow
   git commit -m "feat: add my-flow workflow"
   git push
   ```
7. **Prove it imports:** import the committed JSON into a clean n8n instance and run the sample request. Then update "Status" to "Tested".

## Self-hosted n8n shortcut

```bash
n8n export:workflow --all --separate --output=raw/
```

This exports every workflow to `raw/`; run step 2 on each file.

## Naming and commits

- Folders: `kebab-case`, descriptive (`email-triage-gemini`, not `my-workflow-2`).
- Commits: `feat:` new workflow, `fix:` bug fix, `docs:` README change.
- Rename workflows inside n8n too, so exports are self-explanatory.

## Avoid losing work

Use an n8n setup that does not expire (self-hosted, or a paid plan) and export after every milestone. The repository is your backup, so a missing export is lost work.
