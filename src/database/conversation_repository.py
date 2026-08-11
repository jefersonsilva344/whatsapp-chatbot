from datetime import datetime

from models import Conversation
from logger import logger


class ConversationRepository:
    """
    Responsável pela persistência das conversas no SQLite.

    Regra importante:
    - A aplicação trabalha com datetime.
    - O SQLite recebe a data como string ISO 8601.
    - Na leitura, a string volta para datetime.
    """


    def __init__(
        self,
        db
    ):

        self.db = db


    # ==================================================
    # BUSCAR CONVERSA POR CONTATO
    # ==================================================

    def buscar_por_contato(
        self,
        contato
    ):
        """
        Busca uma conversa pelo contato.

        O valor de atualizada_em armazenado no SQLite
        é convertido novamente para datetime.
        """

        cursor = self.db.cursor()


        # ==================================================
        # DEBUG: MOSTRA QUAL BANCO ESTÁ SENDO USADO
        # ==================================================

        cursor.execute(
            "PRAGMA database_list"
        )

        logger.info(
            f"SQLite databases: "
            f"{cursor.fetchall()}"
        )


        # ==================================================
        # BUSCA CONVERSA
        # ==================================================

        cursor.execute(
            """
            SELECT
                id,
                contato,
                ultima_mensagem,
                atualizada_em,
                ativa

            FROM conversas

            WHERE contato = ?

            LIMIT 1
            """,
            (
                contato,
            )
        )


        resultado = cursor.fetchone()


        logger.info(
            f"Busca conversa: "
            f"contato={contato} | "
            f"resultado={resultado}"
        )


        # ==================================================
        # CONVERSA NÃO ENCONTRADA
        # ==================================================

        if not resultado:

            return None


        # ==================================================
        # CONVERTE DATA DO SQLITE
        # ==================================================

        atualizada_em = resultado[3]


        if atualizada_em:

            atualizada_em = (
                datetime.fromisoformat(
                    atualizada_em
                )
            )


        # ==================================================
        # RECONSTRÓI O MODELO
        # ==================================================

        return Conversation(

            id=resultado[0],

            contato=resultado[1],

            ultima_mensagem=resultado[2],

            atualizada_em=atualizada_em,

            ativa=bool(
                resultado[4]
            )

        )


    # ==================================================
    # SALVAR CONVERSA
    # ==================================================

    def salvar(
        self,
        conversa
    ):
        """
        Salva uma nova conversa ou atualiza uma conversa
        existente pelo contato.

        Antes de enviar os dados para o SQLite,
        datetime é convertido para ISO 8601.
        """

        cursor = self.db.cursor()


        logger.info(
            f"Salvando conversa: "
            f"contato={conversa.contato} | "
            f"id={conversa.id}"
        )


        # ==================================================
        # DEBUG: MOSTRA CONVERSAS ANTES DO INSERT
        # ==================================================

        cursor.execute(
            """
            SELECT
                id,
                contato

            FROM conversas
            """
        )

        logger.info(
            f"Conversas no banco antes do save: "
            f"{cursor.fetchall()}"
        )


        # ==================================================
        # CONVERTE DATETIME PARA ISO 8601
        # ==================================================

        atualizada_em = (
            conversa.atualizada_em
        )


        if isinstance(
            atualizada_em,
            datetime
        ):

            atualizada_em = (
                atualizada_em.isoformat()
            )


        # ==================================================
        # SALVA / ATUALIZA
        # ==================================================

        cursor.execute(
            """
            INSERT INTO conversas
            (
                id,
                contato,
                ultima_mensagem,
                atualizada_em,
                ativa
            )

            VALUES (?, ?, ?, ?, ?)

            ON CONFLICT(contato)
            DO UPDATE SET

                ultima_mensagem =
                    excluded.ultima_mensagem,

                atualizada_em =
                    excluded.atualizada_em,

                ativa =
                    excluded.ativa
            """,
            (
                conversa.id,

                conversa.contato,

                conversa.ultima_mensagem,

                # IMPORTANTE:
                # usamos a variável convertida,
                # e não conversa.atualizada_em
                atualizada_em,

                int(
                    conversa.ativa
                )
            )
        )


        # ==================================================
        # CONFIRMA A TRANSAÇÃO
        # ==================================================

        self.db.commit()


        # ==================================================
        # DEBUG: CONFIRMA O REGISTRO SALVO
        # ==================================================

        cursor.execute(
            """
            SELECT
                id,
                contato

            FROM conversas

            WHERE contato = ?
            """,
            (
                conversa.contato,
            )
        )

        resultado = cursor.fetchone()


        logger.info(
            f"Conversa salva no banco: "
            f"{resultado}"
        )


        logger.info(
            f"Conversa salva: "
            f"{conversa.contato} | "
            f"id={conversa.id}"
        )


        return conversa

