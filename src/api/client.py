from enum import Enum
import aiohttp
import json
import logging
from datetime import date
from urllib.parse import urljoin

from .ordenes import OrdenDeCompra, OrdenDeVenta, OrdenFCI

from .utils import get_logger, iol_decoder_hook
from .token_manager import TokenManager
from .constants import (
    Administradora,
    Ajustada,
    EstadoDeOperaciones,
    Instrumento,
    Mercado,
    Pais,
    Panel,
    TipoFondo,
)


BASE_URL = "https://api.invertironline.com/api/v2/"


def format_date(date):
    return date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


class MethodRequest(Enum):
    def __str__(self) -> str:
        return self.value

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class IOLClient:
    """
    Cliente para obtner datos de cuenta y mercado utilizando la API de Invertir Online
    https://api.invertironline.com
    """

    def __init__(
        self, username: str, password: str, logging_level=logging.NOTSET
    ) -> None:
        self.logger = get_logger(__name__, logging_level)
        self.base_url = BASE_URL
        self.token_manager = TokenManager(
            username, password, logging_level=logging_level
        )

    async def _get_headers(self):
        header = {"Authorization": await self.token_manager.ensure_access_token()}
        return header

    async def _request(
        self, method: MethodRequest, url: str, data_body=None, json_body=None
    ):
        url = urljoin(self.base_url, url)

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method.value,
                url=url,
                headers=await self._get_headers(),
                data=data_body,
                json=json_body,
            ) as resp:
                if resp.status != 200 and resp.status != 202:
                    self.logger.warning(f"{resp.method} {resp.url} {resp.status}")
                else:
                    self.logger.info(f"{resp.method} {resp.url} {resp.status}")

                data = await resp.text()

        return json.loads(data, object_hook=iol_decoder_hook)
        # return json.loads(data)

    # ----------------------------
    # AsesoresTestInversor
    # obtiene las preguntas del test inversor
    async def get_asesores_test_inversor(self):
        path = "asesores/test-inversor"
        return await self._request(method=MethodRequest.GET, url=path)

    # envia las respuestas del test inversor
    async def post_asesores_test_inversor(
        self, respuesta_inversor, id_cliente_asesorado: int | None = None
    ):
        path = (
            f"asesores/test-inversor/{id_cliente_asesorado}"
            if id_cliente_asesorado is not None
            else "asesores/test-inversor"
        )
        return await self._request(
            method=MethodRequest.POST, url=path, json_body=respuesta_inversor
        )

    # ----------------------------
    # MiCuenta
    # Datos del estado de la cuenta del cliente autenticado
    async def get_estado_cuenta(self):
        path = f"estadocuenta"
        return await self._request(method=MethodRequest.GET, url=path)

    # Datos del portafolio del cliente autenticado para un pais determinado
    async def get_portafolio(self, pais: Pais):
        path = f"portafolio/{pais}"
        return await self._request(method=MethodRequest.GET, url=path)

    # Datos de las operaciones del cliente autenticado de acuerdo a los filtros propuestos
    async def get_operaciones(
        self,
        estado: EstadoDeOperaciones,
        pais: Pais,
        fecha_desde: date,
        fecha_hasta: date,
    ):
        path = "operaciones"
        return await self._request(
            method=MethodRequest.GET,
            url=path,
            json_body={
                "estado": estado.value,
                "pais": pais.value,
                "fechaDesde": format_date(fecha_desde),
                "fechaHasta": format_date(fecha_hasta),
            },
        )

    # Datos de las operaciones del cliente autenticado en el ultimo mes
    async def get_operaciones_del_mes(self):
        path = "operaciones"
        return await self._request(method=MethodRequest.GET, url=path)

    # Datos de una determinada operación realizada por un cliente autenticado
    async def get_operacion(self, id_operacion: int):
        path = f"operaciones/{id_operacion}"
        return await self._request(method=MethodRequest.GET, url=path)

    # Cancela una determinada operación realizada por un cliente autenticado
    async def delete_operaciones(self, id_operacion: int):
        path = f"operaciones/{id_operacion}"
        return await self._request(method=MethodRequest.DELETE, url=path)

    # ----------------------------
    # Operar
    async def post_operar_vender(self, orden_venta: OrdenDeVenta):
        path = "operar/Vender"
        return await self._request(
            method=MethodRequest.POST,
            url=path,
            json_body=orden_venta.json(),
        )

    async def post_operar_comprar(self, orden_compra: OrdenDeCompra):
        path = "operar/Comprar"
        return await self._request(
            method=MethodRequest.POST,
            url=path,
            json_body=orden_compra.json(),
        )

    async def post_operar_rescate_fci(self, orden_fci: OrdenFCI):
        path = "operar/rescate/fci"
        return await self._request(
            method=MethodRequest.POST,
            url=path,
            json_body=orden_fci.json(),
        )

    async def post_operar_suscripcion_fci(self, orden_fci: OrdenFCI):
        path = "operar/suscripcion/fci"
        return await self._request(
            method=MethodRequest.POST,
            url=path,
            json_body=orden_fci.json(),
        )

    # ----------------------------
    # Titulos
    # consultar mas tarde por información
    async def get_fci_por_simbolo(self, simbolo: str):
        path = f"Titulos/FCI/{simbolo}"
        return await self._request(method=MethodRequest.GET, url=path)

    async def get_fci(self):
        path = "Titulos/FCI"
        return await self._request(method=MethodRequest.GET, url=path)

    async def get_fci_tipo_fondos(self):
        path = "Titulos/FCI/TipoFondos"
        return await self._request(method=MethodRequest.GET, url=path)

    async def get_fci_administradoras(self):
        path = "Titulos/FCI/Administradoras"
        return await self._request(method=MethodRequest.GET, url=path)

    async def get_fci_tipo_fondos_administradoras_por_administradora(
        self, administradora: Administradora
    ):
        path = f"Titulos/FCI/Administradoras/{administradora}/TipoFondos"
        return await self._request(method=MethodRequest.GET, url=path)

    async def get_fci_tipo_fondos_administradoras_por_administradora_y_tipo_de_fondo(
        self, administradora: Administradora, tipo_fondo: TipoFondo
    ):
        path = f"Titulos/FCI/Administradoras/{administradora}/TipoFondos/{tipo_fondo}"
        return await self._request(method=MethodRequest.GET, url=path)

    # ----------------------------
    # Obtener los instrumentos segun el pais
    async def get_instrumentos(self, pais: Pais):
        path = f"{pais}/Titulos/Cotizacion/Instrumentos"
        return await self._request(method=MethodRequest.GET, url=path)

    # Obtener los paneles segun el pais e instrumento
    async def get_paneles(self, pais: Pais, instrumento: Instrumento):
        path = f"{pais}/Titulos/Cotizacion/Paneles/{instrumento}"
        return await self._request(method=MethodRequest.GET, url=path)

    # Obtener un titulo
    async def get_titulo(self, simbolo: str, mercado: Mercado):
        path = f"{mercado}/Titulos/{simbolo}"
        return await self._request(method=MethodRequest.GET, url=path)

    # Obtener las opciones de un titulo
    async def get_titulo_opciones(self, simbolo: str, mercado: Mercado):
        path = f"{mercado}/Titulos/{simbolo}/Opciones"
        return await self._request(method=MethodRequest.GET, url=path)

    # Obtener la cotizacion de un titulo
    async def get_titulo_cotizacion(self, simbolo: str, mercado: Mercado):
        path = f"{mercado}/Titulos/{simbolo}/Cotizacion"
        return await self._request(method=MethodRequest.GET, url=path)

    # Obtener la serie historica de un titulo
    async def get_titulo_historicos(
        self,
        simbolo: str,
        mercado: Mercado,
        ajustada: Ajustada,
        fecha_desde: date = date(1970, 1, 1),
        fecha_hasta: date = date.today(),
    ):
        path = f'{mercado}/Titulos/{simbolo}/Cotizacion/seriehistorica/{fecha_desde.strftime("%Y-%m-%d")}/{fecha_hasta.strftime("%Y-%m-%d")}/{ajustada}'
        return await self._request(method=MethodRequest.GET, url=path)

    # Obtener el panel de cotizaciones
    async def get_panel_cotizaciones(
        self, pais: Pais, instrumento: Instrumento, panel: Panel
    ):
        path = f"Cotizaciones/{instrumento}/{panel}/{pais}"
        return await self._request(method=MethodRequest.GET, url=path)
