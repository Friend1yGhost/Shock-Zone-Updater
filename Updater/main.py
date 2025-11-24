import os
import sys
import logging

from PyQt5.QtWidgets import QApplication, QMessageBox

from app.main_window import MainWindow
from app.windows_privileges import ensure_admin_privileges

LOGGING_ENABLED = True


def setup_logging():
    logs_dir = os.path.join(os.getcwd(), "logs")
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


def get_base_path():
    # compatível com PyInstaller
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def main():
    # Garante privilégios administrativos no Windows (se possível)
    ensure_admin_privileges()

    if LOGGING_ENABLED:
        setup_logging()

    app = QApplication(sys.argv)

    base_path = get_base_path()
    config_path = os.path.join(base_path, "config.json")

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
