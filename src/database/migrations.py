from uuid import uuid4

class Migration:

    """
    Responsável por criar e atualizar
    a estrutura do banco SQLite.
    """

    def __init__(self, db):

        self.db = db

        self.cursor = db.cursor()

    def run(self):

        """
        Executa todas as migrações
        necessárias.
        """

        # =====================================
        # 1 - CRIA TABELAS
        # =====================================

        self._criar_tabela_conversas()

        self._criar_tabela_mensagens()

        # =====================================
        # 2 - CRIA ÍNDICES
        # =====================================

        self._criar_indices()

        # =====================================
        # 3 - MIGRA ESTRUTURA
        # (compatibilidade com bancos antigos)
        # =====================================

        self._migrar_colunas()

        # =====================================
        # 4 - MIGRA DADOS
        # =====================================

        self._migrar_dados()

        # =====================================
        # 5 - SALVA ALTERAÇÕES
        # =====================================

        self.db.commit()

    def _criar_tabela_conversas(self):

        """
        Armazena cada conversa
        existente no WhatsApp.
        """

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS conversas (

            id TEXT PRIMARY KEY NOT NULL,

            contato TEXT UNIQUE NOT NULL UNIQUE,

            ultima_mensagem TEXT,

            atualizada_em TEXT,

            ativa INTEGER NOT NULL DEFAULT 1

        )

        """)

    def _criar_tabela_mensagens(self):

        """
        Armazena todas as mensagens
        da conversa.
        """

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS mensagens (

            id TEXT PRIMARY KEY NOT NULL,

            conversation_id TEXT NOT NULL,

            autor TEXT NOT NULL,

            role TEXT NOT NULL,

            texto TEXT NOT NULL,

            data_hora TEXT NOT NULL,

            recebida INTEGER NOT NULL DEFAULT 0,

            respondida INTEGER NOT NULL DEFAULT 0,

            FOREIGN KEY (conversation_id)
                REFERENCES conversas(id)

        )

        """)

    def _criar_indices(self):

        """
        Cria índices para melhorar
        a performance das consultas.
        """

        self.cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_mensagem_id

        ON mensagens(id)

        """)

        self.cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_historico

        ON mensagens(

            conversation_id,

            data_hora

        )

        """)

        self.cursor.execute("""

        CREATE INDEX IF NOT EXISTS idx_mensagem_data

        ON mensagens(data_hora)

        """)

    def _migrar_colunas(self):

        """
        Adiciona colunas novas em
        bancos criados em versões
        anteriores.
        """

        self.cursor.execute(

            "PRAGMA table_info(mensagens)"

        )

        colunas = [

            coluna[1]

            for coluna in self.cursor.fetchall()

        ]

        if "conversation_id" not in colunas:

            self.cursor.execute("""

            ALTER TABLE mensagens

            ADD COLUMN conversation_id TEXT

            """)

    def _migrar_dados(self):

        # =====================================
        # CORRIGE IDs DAS CONVERSAS
        # =====================================

        self.cursor.execute("""
            SELECT contato
            FROM conversas
            WHERE id IS NULL
        """)

        conversas = self.cursor.fetchall()


        for (contato,) in conversas:

            novo_id = str(uuid4())

            self.cursor.execute(
                """
                UPDATE conversas

                SET id = ?

                WHERE contato = ?
                AND id IS NULL
                """,
                (
                    novo_id,
                    contato
                )
            )


        # =====================================
        # CORRIGE ROLE DAS MENSAGENS
        # =====================================

        self.cursor.execute("""
            UPDATE mensagens

            SET role =
                CASE
                    WHEN recebida = 1
                        THEN 'user'

                    ELSE 'assistant'
                END

            WHERE role IS NULL
        """)