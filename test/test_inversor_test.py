import os
import asyncio
from src.api.client import IOLClient
from src.api.constants import Mercado
import pytest


@pytest.mark.asyncio
async def test_get_asesores_test_inversor():
    user = os.getenv("IOL_USER") or ""
    password = os.getenv("IOL_PASS") or ""
    client = IOLClient(username=user, password=password)
    test = await client.get_asesores_test_inversor()
    assert test["message"] != "Authorization has been denied for this request."
