from neo4j.time import Date, DateTime

import asyncio
from typing import Awaitable, Any

async def run_parallel(*funcs: Awaitable[Any]) -> None:
    """
    Runs a list of functions in parallel
    """
    await asyncio.gather(*funcs)

async def run_sequential(*funcs: Awaitable[Any]) -> None:
    """
    Runs a list of functions sequentially
    """
    for func in funcs:
        await func


class PropertiesDict(dict):
    def __repr__(self):
        s = "{"
        for key in self:
            if key in ["created_at", "updated_at"]:
                s += f"""{key}:apoc.date.parse('{str(DateTime.from_native(self[key]))}', 's', "yyyy-MM-dd'T'HH:mm:ss"), """

            elif key in ["date_of_birth"]:
                s += f"""{key}:apoc.Date.parse('{str(Date.from_native(self[key]))}', 'd', "yyyy-MM-dd'T'HH:mm:ss"), """

            else:
                if type(self[key]) == str:
                    s += '{0}:"{1}", '.format(key, self[key].replace('"', '\\"'))
                else:
                    s += "{0}:{1}, ".format(key, self[key])
        if len(s) > 1:
            s = s[0:-2]
        s += "}"
        return s
