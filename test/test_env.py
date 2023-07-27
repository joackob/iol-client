import os
from iol_client.client import IOLClient


def test_get_asesores_test_inversor():
    user = os.getenv("IOL_USER") or ""
    password = os.getenv("IOL_PASS") or ""
    assert user != "" and password != ""
