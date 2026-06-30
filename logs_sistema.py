import logging
import os


_PASTA_LOG_PADRAO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
_ARQUIVO_LOG = os.environ.get(
    "SISTEMA_LOG_FILE", os.path.join(_PASTA_LOG_PADRAO, "sistema.log")
)


def obter_logger(nome: str) -> logging.Logger:
    logger = logging.getLogger(nome)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    formato = logging.Formatter(
        "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        os.makedirs(os.path.dirname(_ARQUIVO_LOG), exist_ok=True)
        arquivo = logging.FileHandler(_ARQUIVO_LOG, encoding="utf-8")
        arquivo.setFormatter(formato)
        logger.addHandler(arquivo)
    except OSError:
        pass

    tela = logging.StreamHandler()
    tela.setFormatter(formato)
    logger.addHandler(tela)
    return logger


def resumir_texto(texto, limite: int = 180) -> str:
    texto = str(texto).replace("\r", " ").replace("\n", " ").strip()
    if len(texto) <= limite:
        return texto
    return texto[: limite - 3] + "..."


def _formatar_campos(campos) -> str:
    partes = []
    for chave, valor in campos.items():
        if valor is None:
            continue
        partes.append(f"{chave}={resumir_texto(valor)}")
    return " | ".join(partes)


def registrar_info(logger: logging.Logger, evento: str, **campos) -> None:
    mensagem = f"evento={evento}"
    campos_formatados = _formatar_campos(campos)
    if campos_formatados:
        mensagem += f" | {campos_formatados}"
    logger.info(mensagem)


def registrar_erro(logger: logging.Logger, evento: str, excecao=None, **campos) -> None:
    if excecao is not None:
        campos.setdefault("tipo_erro", type(excecao).__name__)
        campos.setdefault("erro", excecao)

    mensagem = f"evento={evento}"
    campos_formatados = _formatar_campos(campos)
    if campos_formatados:
        mensagem += f" | {campos_formatados}"
    logger.error(mensagem)
