import pandas as pd
from dataclasses import dataclass, field
from typing import List


@dataclass
class JobDefinition:
    workspace: str
    job_name: str
    folder_deps: List[str] = field(default_factory=list)
    job_deps: List[str] = field(default_factory=list)


def parse_excel(filepath: str) -> List[JobDefinition]:
    df = pd.read_excel(filepath)
    df.columns = [c.strip().lower() for c in df.columns]

    required = {"workspace", "job name", "dependency"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Excel file is missing required columns: {missing}")

    jobs = []
    for idx, row in df.iterrows():
        workspace = str(row["workspace"]).strip()
        job_name = str(row["job name"]).strip()
        dep_raw = str(row["dependency"]).strip() if pd.notna(row["dependency"]) else ""

        folder_deps = []
        job_deps = []

        for dep in dep_raw.split(","):
            dep = dep.strip()
            if not dep:
                continue
            if dep.startswith("Folder:"):
                folder_deps.append(dep[len("Folder:"):].strip())
            else:
                job_deps.append(dep)

        jobs.append(JobDefinition(
            workspace=workspace,
            job_name=job_name,
            folder_deps=folder_deps,
            job_deps=job_deps,
        ))

    return jobs
