from typing import Optional
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from aredis_om import HashModel, NotFoundError


class WorkflowJob(HashModel):
    pass


class Job(HashModel):
    action: str
    repo: str
    organization: Optional[str]
    sender: str
    workflow_job = WorkflowJob


app = FastAPI()


@app.post("/webhook/github")
async def add_job(job: Job):
    return await job.save()


@app.get("/jobs")
async def list_jobs(request: Request, response: Response):
    return [j async for j in await Job.all_pks()]


@app.get("/job/{pk}")
async def get_job(pk: str, request: Request, response: Response) -> Job:
    try:
        return await Job.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Job not found")
