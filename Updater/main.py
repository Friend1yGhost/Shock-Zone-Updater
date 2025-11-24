import os
import sys
import logging

from PyQt5.QtWidgets import QApplication, QMessageBox

from app.main_window import MainWindow
from app.windows_privileges import ensure_admin_privileges

LOGGING_ENABLED = True


def get_app_dir() -> str:
    """
    Retorna a pasta onde está o executável (no .exe) ou o arquivo main.py (em dev).

    - Quando estiver empacotado com PyInstaller (sys.frozen = True),
      usamos sys.executable.
    - Em modo desenvolvimento, usamos o próprio __file__.
    """
    if getattr(sys, "frozen", False):
        # caminho do .exe gerado pelo PyInstaller
        return os.path.dirname(os.path.abspath(sys.executable))
    # caminho do main.py quando rodando com "python main.py"
    return os.path.dirname(os.path.abspath(__file__))


def setup_logging(app_dir: str) -> None:
    logs_dir = os.path.join(app_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    log_file_path = os.path.join(logs_dir, "launcher.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file_path, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    logging.info("Logging iniciado.")
    logging.info(f"Diretório da aplicação: {app_dir}")


def main():
    # Garante privilégios administrativos no Windows (se possível)
    ensure_admin_privileges()

    app_dir = get_app_dir()

    if LOGGING_ENABLED:
        setup_logging(app_dir)

    app = QApplication(sys.argv)

    # config.json fica SEMPRE ao lado do .exe / main.py
    config_path = os.path.join(app_dir, "config.json")

    if not os.path.isfile(config_path):
        QMessageBox.critical(
            None,
            "Erro",
            f"Arquivo de configuração não encontrado:\n{config_path}",
        )
        sys.exit(1)

    try:
        window = MainWindow(config_path=config_path)
    except Exception:
        logging.exception("Falha ao iniciar a janela principal")
        QMessageBox.critical(
            None,
            "Erro",
            "Falha ao iniciar o launcher. Verifique o arquivo de configuração.",
        )
        sys.exit(1)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
