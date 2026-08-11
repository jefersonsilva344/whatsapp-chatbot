from container import Container
from logger import logger



def main():


    container = Container()


    try:

        container.iniciar()

        container.executar()

    except Exception as erro:

        logger.exception(
            f"Erro na aplicação:{erro}"
        )


    finally:

        container.fechar()




if __name__ == "__main__":

    main()