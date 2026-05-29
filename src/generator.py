import json
from typing import List
from .parser import JobDefinition


def _build_folder(folder_name: str, jobs: List[JobDefinition]) -> dict:
    folder: dict = {"Type": "Folder"}

    for job in jobs:
        entry: dict = {"Type": "Job:Dummy"}

        if job.folder_deps:
            entry[f"{job.job_name}-WaitForEvents"] = {
                "Type": "WaitForEvents",
                "Events": [f"{dep}_COMPLETE" for dep in job.folder_deps],
            }

        folder[job.job_name] = entry

    for job in jobs:
        for dep in job.job_deps:
            flow_key = f"{dep}-TO-{job.job_name}"
            folder[flow_key] = {
                "Type": "Flow",
                "Sequence": [dep, job.job_name],
            }

    return folder


def generate_json(jobs: List[JobDefinition]) -> str:
    folders: dict[str, List[JobDefinition]] = {}
    for job in jobs:
        folders.setdefault(job.workspace, []).append(job)

    output = {}
    for folder_name, folder_jobs in folders.items():
        output[folder_name] = _build_folder(folder_name, folder_jobs)

    return json.dumps(output, indent=2)
