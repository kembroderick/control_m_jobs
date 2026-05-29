import json
from typing import List
from .parser import JobDefinition


def _build_folder(folder_name: str, jobs: List[JobDefinition]) -> dict:
    job_entries = []

    for job in jobs:
        entry = {
            "Type": "Job:Command",
            "Name": job.job_name,
            "Command": "",
        }

        if job.job_deps:
            entry["DependsOnJobs"] = {
                "Scope": "Global",
                "Jobs": [{"Name": dep} for dep in job.job_deps],
            }

        if job.folder_deps:
            entry["WaitForFolders"] = [{"Name": dep} for dep in job.folder_deps]

        job_entries.append(entry)

    return {
        "Type": "SimpleFolder",
        "Jobs": job_entries,
    }


def generate_json(jobs: List[JobDefinition]) -> str:
    folders: dict[str, List[JobDefinition]] = {}
    for job in jobs:
        folders.setdefault(job.workspace, []).append(job)

    output = {}
    for folder_name, folder_jobs in folders.items():
        output[folder_name] = _build_folder(folder_name, folder_jobs)

    return json.dumps(output, indent=2)
