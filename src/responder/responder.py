from .normalizador import Normalizador
from .regras import Regras
from .respostas import RESPOSTAS

from ia.openai_service import OpenAIService

class Responder:

    def __init__(self,repository):
        
        self.ia = OpenAIService()
        self.repository = repository

    def responder(
            self, 
            conversation_id, 
            texto
    ):

        texto_original = texto

        texto = Normalizador.normalizar(texto)

        intent = Regras.descobrir_intent(texto)

        # encontrou regra simples
        if intent != "default":

            resposta = RESPOSTAS[intent]

            if len(texto_original.split()) <= 4:
                return resposta
        
        
        historico = self.repository.history(
            conversation_id,
            limite=10
        )

        print("\n====== HISTÓRICO ======")

        for item in historico:
            print(item)

        print("=======================\n")

    
        # não encontrou -> IA
        return self.ia.responder(
            mensagem=texto_original,
            historico=historico
        )