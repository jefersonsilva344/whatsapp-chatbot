from models import Message
from datetime import datetime
import sqlite3


class MessageRepository:

    def __init__(self, db):

        self.db = db


    def exists_by_id(self, message_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM mensagens
            WHERE id = ?
            """,
            (message_id,)
        )

        return cursor.fetchone() is not None



    def save(self, mensagem: Message):

        cursor = self.db.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO mensagens
                (
                    id,
                    conversation_id,
                    autor,
                    role,
                    texto,
                    data_hora,
                    recebida,
                    respondida
                )

                VALUES (?, ?, ?, ?, ?, ?, ?,?)

                """,
                (
                    mensagem.id,
                    mensagem.conversation_id,
                    mensagem.autor,
                    mensagem.role,
                    mensagem.texto,
                    datetime.now().isoformat(),
                    int(mensagem.recebida),
                    0
                )
            )

            self.db.commit()

            return True


        except sqlite3.IntegrityError:

            return False



    def mark_answered(self, message_id):

        cursor = self.db.cursor()

        cursor.execute(
            """
            UPDATE mensagens
            SET respondida = 1
            WHERE id = ?
            """,
            (message_id,)
        )

        self.db.commit()



    def history(
            self,
            conversation_id, 
            limite=10):

        cursor = self.db.cursor()

        cursor.execute(
            """
            SELECT role, texto
            FROM mensagens

            WHERE conversation_id = ?

            ORDER BY data_hora DESC

            LIMIT ?

            """,
            (
                conversation_id,
                limite
            )
        )

        registros = cursor.fetchall()

        registros.reverse()


        return [
            {
                "role": role,
                "content": texto
            }

            for role, texto in registros
        ]
