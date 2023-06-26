import os
import asyncio
from src.api.client import IOLClient
from src.api.constants import Mercado


async def test_bonos():
    user = os.getenv("IOL_USER") or ""
    password = os.getenv("IOL_PASS") or ""
    client = IOLClient(username=user, password=password)
    titulo = await client.get_titulo("GGAL", Mercado.BCBA)
    assert titulo.json != {}
