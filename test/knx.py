import asyncio
from xknxproject.models import KNXProject
from xknxproject import KNXProj
import json


async def main():
    """Extract and parse a KNX project file."""
    knxproj: KNXProj = KNXProj("VillaWeber.knxproj")
    project: KNXProject = await knxproj.parse()

    with open('project.json', 'w') as file:
        file.write(json.dumps(project))

asyncio.run(main())