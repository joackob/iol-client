from dataclasses import dataclass
from datetime import datetime

from .constants import Mercado, Plazo, TipoDeOrden


def validez_by_default():
    today = datetime.now()
    return datetime(today.year, today.month, today.day, 23, 59, 59)


class OrdenDeCompra:
    def __init__(
        self,
        mercado: Mercado,
        simbolo: str,
        validez: datetime | None = None,
        cantidad: int | None = None,
        monto: int | None = None,
        precio: int = 0,
        tipo_orden: TipoDeOrden = TipoDeOrden.PRECIO_LIMITE,
        plazo: Plazo = Plazo.T2,
    ) -> None:
        self.type = type
        self.mercado = mercado
        self.simbolo = simbolo
        self.cantidad = cantidad
        self.precio = precio
        self.validez = validez or validez_by_default()
        self.tipo_orden = tipo_orden
        self.plazo = plazo
        self.monto = monto
        self._validar()

    def _validar(self):
        if self.monto is not None and self.cantidad is not None:
            raise AttributeError(
                "Parametro monto y cantidad definidos, solo se puede usar uno de los dos parametros por orden"
            )

        if self.cantidad is not None and self.tipo_orden != TipoDeOrden.PRECIO_LIMITE:
            raise AttributeError("cantidad solo permite tipo_orden='precioLimite'")

        if self.tipo_orden == TipoDeOrden.PRECIO_MERCADO and self.precio > 0:
            raise AttributeError("Precio debe ser 0 para tipo_orden='precioMercado'")

        if self.tipo_orden == TipoDeOrden.PRECIO_LIMITE and self.precio <= 0:
            raise AttributeError(
                "Precio debe ser mayor que 0 para tipo_orden='precioLimite'"
            )

    def json(self):
        ord = {
            "mercado": self.mercado.value,
            "simbolo": self.simbolo,
            "tipoOrden": self.tipo_orden.value,
            "precio": self.precio,
            "plazo": self.plazo.value,
            "validez": self.validez.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        }

        if self.cantidad is not None:
            ord["cantidad"] = self.cantidad
        else:
            ord["monto"] = self.monto

        return ord


class OrdenDeVenta:
    def __init__(
        self,
        mercado: Mercado,
        simbolo: str,
        cantidad: int,
        validez: datetime | None = None,
        precio: int = 0,
        tipo_orden: TipoDeOrden = TipoDeOrden.PRECIO_LIMITE,
        plazo: Plazo = Plazo.T2,
    ) -> None:
        self.type = type
        self.mercado = mercado
        self.simbolo = simbolo
        self.cantidad = cantidad
        self.precio = precio
        self.validez = validez or validez_by_default()
        self.tipo_orden = tipo_orden
        self.plazo = plazo
        self._validar()

    def _validar(self):
        if self.cantidad is not None:
            raise AttributeError("Parametro cantidad no definido")

        if self.tipo_orden == TipoDeOrden.PRECIO_MERCADO and self.precio > 0:
            raise AttributeError("Precio debe ser 0 para tipo_orden='precioMercado'")

        if self.tipo_orden == TipoDeOrden.PRECIO_LIMITE and self.precio <= 0:
            raise AttributeError(
                "Precio debe ser mayor que 0 para tipo_orden='precioLimite'"
            )

    def json(self):
        ord = {
            "mercado": self.mercado.value,
            "simbolo": self.simbolo,
            "tipoOrden": self.tipo_orden.value,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "plazo": self.plazo.value,
            "validez": self.validez.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        }
        return ord


@dataclass
class OrdenFCI:
    simbolo: str = ""
    cantidad: int = 0
    solo_validar: bool = True

    def json(self):
        ord = {
            "simbolo": self.simbolo,
            "cantidad": self.cantidad,
            "soloValidar": self.solo_validar,
        }
        return ord
