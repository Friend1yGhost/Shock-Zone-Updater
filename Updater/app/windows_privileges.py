import os
import sys
import ctypes


def _is_windows():
    return os.name == "nt"


def _is_admin():
    if not _is_windows():
        return True  # em outros SOs, ignora
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def ensure_admin_privileges():
    """
    Garante que o processo está rodando como administrador no Windows.
    Se não estiver, relança o próprio programa com 'runas' e encerra este.
    Funciona tanto com script .py quanto com .exe gerado por PyInstaller.
    """
    if not _is_windows():
        return

    if _is_admin():
        # Já está como admin, segue normal
        return

    # Se for um executável (PyInstaller, por exemplo), relança o próprio .exe
    if getattr(sys, "frozen", False):
        exe = sys.executable
        params = None  # sem parâmetros, o próprio exe já sabe o que fazer
    else:
        # Script .py: chama o python com o caminho do script + argumentos
        exe = sys.executable

        script_path = os.path.abspath(sys.argv[0])
        all_args = [script_path] + sys.argv[1:]
        params = " ".join(f'"{arg}"' for arg in all_args)

    try:
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",   # verbo que pede elevação (UAC)
            exe,
            params,
            None,
            1          # SW_SHOWNORMAL
        )
    except Exception:
        # Se der erro para elevar, simplesmente continua sem admin
        return

    # Sai do processo atual; o novo (elevado) assume
    sys.exit(0)
