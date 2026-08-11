import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)


logging.basicConfig(
    level=logging.INFO,

    format="%(asctime)s | %(levelname)s | %(message)s",

    datefmt="%d/%m/%Y %H:%M:%S",

    handlers=[

        logging.FileHandler(
            LOG_DIR / "bot.log",
            encoding="utf-8"
        ),

        logging.StreamHandler()

    ]
)


logger = logging.getLogger("whatsapp_bot")
