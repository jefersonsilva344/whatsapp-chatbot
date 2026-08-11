from collections import defaultdict


class Memoria:

    def __init__(self):

        self.conversas = defaultdict(list)


    def adicionar(self, contato, role, texto):

        self.conversas[contato].append({

            "role": role,

            "content": texto

        })

        # mantém somente as últimas 10 mensagens
        self.conversas[contato] = \
            self.conversas[contato][-10:]


    def obter(self, contato):

        return self.conversas[contato]