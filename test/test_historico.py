import datetime
import logging
import os
import time
from iol_client import IOLClient
from iol_client.constants import Ajustada, Mercado
import pytest


@pytest.mark.asyncio
async def test_get_hisctorico_del_ultimo_mes():
    user = os.getenv("IOL_USER") or ""
    password = os.getenv("IOL_PASS") or ""
    client = IOLClient(username=user, password=password, logging_level=logging.DEBUG)
    hoy = datetime.datetime.now()
    hace_un_mes = hoy - datetime.timedelta(days=30)
    historico = await client.get_titulo_historicos(
        simbolo="GGAL",
        mercado=Mercado.BCBA,
        ajustada=Ajustada.SIN_AJUSTAR,
        fecha_desde=hace_un_mes,
        fecha_hasta=hoy,
    )
    assert len(historico) > 0


@pytest.mark.asyncio
async def test_get_hisctorico_de_dos_simbolos_distintos():
    user = os.getenv("IOL_USER") or ""
    password = os.getenv("IOL_PASS") or ""
    client = IOLClient(username=user, password=password, logging_level=logging.DEBUG)
    hoy = datetime.datetime.now()
    hace_un_mes = hoy - datetime.timedelta(days=30)
    historico_ggal = await client.get_titulo_historicos(
        simbolo="GGAL",
        mercado=Mercado.BCBA,
        ajustada=Ajustada.SIN_AJUSTAR,
        fecha_desde=hace_un_mes,
        fecha_hasta=hoy,
    )
    historico_ae38 = await client.get_titulo_historicos(
        simbolo="GGAL",
        mercado=Mercado.BCBA,
        ajustada=Ajustada.SIN_AJUSTAR,
        fecha_desde=hace_un_mes,
        fecha_hasta=hoy,
    )
    assert len(historico_ggal) > 0 and len(historico_ae38) > 0


@pytest.mark.asyncio
async def test_get_hisctorico_de_dos_simbolos_distintos_con_un_delta_t_entre_cada_consulta():
    user = os.getenv("IOL_USER") or ""
    password = os.getenv("IOL_PASS") or ""
    client = IOLClient(username=user, password=password, logging_level=logging.DEBUG)
    hoy = datetime.datetime.now()
    hace_un_mes = hoy - datetime.timedelta(days=30)
    historico_ggal = await client.get_titulo_historicos(
        simbolo="GGAL",
        mercado=Mercado.BCBA,
        ajustada=Ajustada.SIN_AJUSTAR,
        fecha_desde=hace_un_mes,
        fecha_hasta=hoy,
    )
    time.sleep(3)
    historico_ae38 = await client.get_titulo_historicos(
        simbolo="GGAL",
        mercado=Mercado.BCBA,
        ajustada=Ajustada.SIN_AJUSTAR,
        fecha_desde=hace_un_mes,
        fecha_hasta=hoy,
    )
    assert len(historico_ggal) > 0 and len(historico_ae38) > 0
