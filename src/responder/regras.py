from responder.intents import INTENTS


class Regras:

    @staticmethod
    def descobrir_intent(texto):

        for intent, palavras in INTENTS.items():

            for palavra in palavras:

                if palavra in texto:
                    return intent

        return "default"