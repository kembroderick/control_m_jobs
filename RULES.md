# Control-M Job Definition Parser — Rules

## Excel Input Format

The input is an Excel file with the following required columns (case-insensitive, whitespace-trimmed):

| Column | Description |
|---|---|
| `workspace` | Groups jobs into a Control-M folder |
| `job name` | Unique name for the job |
| `dependency` | Comma-separated list of prerequisites (upstream dependencies) |

## Dependency Rules

Dependencies in the `dependency` column are **prerequisites** — they must complete before the current job runs.

- **Job dependency**: plain job name, e.g. `Extract_Sales`
- **Folder dependency**: prefixed with `Folder:`, e.g. `Folder:ETL_Daily` — the job waits for the entire named folder to complete
- Multiple dependencies are comma-separated, e.g. `Transform_Sales, Transform_Inventory`
- Empty = no dependencies

## Output Format

Control-M Automation API JSON (flat top-level dict). Top-level keys are folder names (from `workspace`).

```json
{
  "FolderName": {
    "Type": "Folder",
    "JobA": { "Type": "Job:Dummy" },
    "JobB": {
      "Type": "Job:Dummy",
      "JobB-WaitForEvents": {
        "Type": "WaitForEvents",
        "Events": ["OtherFolder_COMPLETE"]
      }
    },
    "JobA-TO-JobB": {
      "Type": "Flow",
      "Sequence": ["JobA", "JobB"]
    }
  }
}
```

- Top level is a **flat dict** — no `{"Folders": [...]}` wrapper
- Jobs are **dict keys** inside the folder — no `"Name"` field, no array
- Intra-folder job dependencies use `Flow` objects named `"Upstream-TO-Downstream"`
- Each `Flow` has `"Sequence": ["upstream_job", "downstream_job"]` — one edge per Flow
- Fan-in (multiple prerequisites) is expressed as multiple Flow objects converging on the same downstream job
- Cross-folder (folder-level) dependencies use a `WaitForEvents` sub-object on the waiting job, with event name `{FolderName}_COMPLETE`

## Project Structure

- `src/parser.py` — reads Excel into `List[JobDefinition]`
- `src/generator.py` — converts job list to Control-M JSON
- `src/main.py` — CLI entry point

## CLI Usage

```
python3 -m src.main <input.xlsx> [-o output.json]
```

## Known Gaps (first pass — to refactor)

- `Command` field is hardcoded to empty string; Excel has no command column yet
- No agent/host assignment
- No schedule or run-as fields
