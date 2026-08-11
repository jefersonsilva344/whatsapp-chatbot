import re
import unicodedata


class Normalizador:

    @staticmethod
    def normalizar(texto):

        texto = texto.lower().strip()

        texto = unicodedata.normalize(
            "NFD",
            texto
        )

        texto = texto.encode(
            "ascii",
            "ignore"
        ).decode("utf-8")

        texto = re.sub(
            r"[^\w\s]",
            "",
            texto
        )

        texto = re.sub(
            r"\s+",
            " ",
            texto
        )

        return texto