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

Control-M Automation API JSON. Top-level keys are folder names (from `workspace`).

```json
{
  "FolderName": {
    "Type": "SimpleFolder",
    "Jobs": [
      {
        "Type": "Job:Command",
        "Name": "JobName",
        "Command": "",
        "DependsOnJobs": {
          "Scope": "Global",
          "Jobs": [{ "Name": "UpstreamJob" }]
        },
        "WaitForFolders": [{ "Name": "UpstreamFolder" }]
      }
    ]
  }
}
```

- `Jobs` is an **array** (not an object)
- Each job carries a `"Name"` field
- `DependsOnJobs` is present only if the job has job-level prerequisites
- `WaitForFolders` is present only if the job has folder-level prerequisites

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
