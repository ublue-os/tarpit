import httpx
import jmespath


class MetalAPI:
    def __init__(self, api_key):
        self.client = httpx.AsyncClient(
            base_url="https://api.equinix.com/metal/v1",
            headers={"X-Auth-Token": api_key, "User-Agent": "armaphore/0.1.0"},
        )

    async def get(self, url: str, query: dict = None):
        resp = await self.client.get()
        return resp

    async def get_all(self, url: str, query: dict = None):
        resp = await self.get_all(url, query)
        content = resp.json()
        if next_url := jmespath.search("meta.next.href", content):
            pass

    async def get_all_devices_of_a_project(self, id: str, **kwargs):
        resp = await self.get(f"/projects/{id}/devices", query=kwargs)

    async def create_device(self, project_id: str, **kwargs):
        pass
