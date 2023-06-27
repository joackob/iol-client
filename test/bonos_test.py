import os
import asyncio
from src.api.client import IOLClient
from src.api.constants import Mercado
import pytest


@pytest.mark.asyncio
async def test_bonos():
    user = os.getenv("IOL_USER") or ""
    password = os.getenv("IOL_PASS") or ""
    client = IOLClient(username=user, password=password)
    titulo = await client.get_titulo("GGAL", Mercado.BCBA)
    assert titulo["message"] != "Authorization has been denied for this request."
