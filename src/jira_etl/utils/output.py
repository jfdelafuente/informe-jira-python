"""
Sistema de output centralizado con colores y thread-safety

Este módulo proporciona una clase OutputManager para manejar toda la salida
de los scripts de forma consistente, con soporte para colores y thread-safety.
"""
from threading import Lock
from typing import Dict, Any

# Intentar importar colorama para colores
try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    HAS_COLORS = True
except ImportError:
    HAS_COLORS = False

    class Fore:
        GREEN = CYAN = YELLOW = RED = WHITE = MAGENTA = BLUE = ""

    class Style:
        BRIGHT = RESET_ALL = DIM = ""

    class Back:
        GREEN = RED = BLUE = ""


class OutputManager:
    """
    Gestor centralizado de salida con colores y thread-safety.

    Proporciona métodos especializados para diferentes tipos de mensajes
    y garantiza salida consistente incluso en entornos multi-thread.

    Attributes:
        use_colors: Si debe usar colores (requiere colorama)
        lock: Lock para thread-safety

    Example:
        >>> output = OutputManager()
        >>> output.header("MI SCRIPT")
        >>> output.success("Operacion exitosa")
        >>> output.error("Hubo un error")
    """

    def __init__(self, use_colors: bool = True):
        """
        Inicializa el gestor de salida.

        Args:
            use_colors: Si debe intentar usar colores (default: True)
        """
        self.use_colors = use_colors and HAS_COLORS
        self.lock = Lock()  # Para thread-safety en prints

    def _print(self, msg: str, color: str = "", style: str = ""):
        """
        Print thread-safe con colores opcionales.

        Args:
            msg: Mensaje a imprimir
            color: Color del texto (Fore.*)
            style: Estilo del texto (Style.*)
        """
        with self.lock:
            if self.use_colors and color:
                print(f"{color}{style}{msg}{Style.RESET_ALL}")
            else:
                print(msg)

    def header(self, text: str):
        """
        Imprime un encabezado destacado.

        Args:
            text: Texto del encabezado
        """
        sep = "=" * 60
        if self.use_colors:
            self._print(f"\n{sep}", Fore.CYAN, Style.BRIGHT)
            self._print(text, Fore.CYAN, Style.BRIGHT)
            self._print(sep, Fore.CYAN, Style.BRIGHT)
        else:
            self._print(f"\n{sep}")
            self._print(text)
            self._print(sep)

    def section(self, text: str):
        """
        Imprime una sección con prefijo [+].

        Args:
            text: Texto de la sección
        """
        self._print(f"[+] {text}", Fore.YELLOW, Style.BRIGHT)

    def success(self, text: str):
        """
        Imprime un mensaje de éxito con [OK].

        Args:
            text: Mensaje de éxito
        """
        self._print(f"  [OK] {text}", Fore.GREEN)

    def skip(self, text: str):
        """
        Imprime un mensaje de skip con [SKIP].

        Args:
            text: Mensaje de skip
        """
        self._print(f"  [SKIP] {text}", Fore.YELLOW)

    def error(self, text: str):
        """
        Imprime un mensaje de error con [ERROR].

        Args:
            text: Mensaje de error
        """
        self._print(f"  [ERROR] {text}", Fore.RED)

    def warning(self, text: str):
        """
        Imprime un mensaje de advertencia con [WARN].

        Args:
            text: Mensaje de advertencia
        """
        self._print(f"  [WARN] {text}", Fore.YELLOW)

    def info(self, text: str):
        """
        Imprime un mensaje informativo.

        Args:
            text: Mensaje informativo
        """
        self._print(f"{text}", Fore.CYAN)

    def step(self, number: int, text: str):
        """
        Imprime un paso numerado.

        Args:
            number: Número del paso
            text: Descripción del paso
        """
        self._print(f"\n[{number}] {text}", Fore.MAGENTA, Style.BRIGHT)

    def progress(
        self,
        current: int,
        total: int,
        item: str,
        count: int = 0,
        status: str = "OK"
    ):
        """
        Muestra progreso con formato consistente.

        Args:
            current: Número actual
            total: Total de items
            item: Nombre del item
            count: Contador adicional (ej: bugs encontrados)
            status: Estado (OK, SKIP, ERROR)
        """
        percentage = (current / total * 100) if total > 0 else 0

        if status == "OK":
            color = Fore.GREEN
            symbol = "[OK]"
        elif status == "SKIP":
            color = Fore.YELLOW
            symbol = "[SKIP]"
        else:
            color = Fore.RED
            symbol = "[ERROR]"

        msg = f"  {symbol} [{current}/{total}] {item}: {count} items ({percentage:.1f}%)"
        self._print(msg, color)

    def summary(self, stats: Dict[str, Any], title: str = "RESUMEN FINAL"):
        """
        Imprime un resumen final con estadísticas.

        Args:
            stats: Diccionario con estadísticas
            title: Título del resumen
        """
        self.header(title)

        # Estadísticas comunes
        if 'processed' in stats:
            self.info(f"  Items procesados: {stats['processed']}")

        if 'success' in stats:
            color = Fore.GREEN if self.use_colors else ""
            reset = Style.RESET_ALL if self.use_colors else ""
            self.info(f"  Exitosos: {color}{stats['success']}{reset}")

        if 'failed' in stats:
            color = Fore.RED if self.use_colors else ""
            reset = Style.RESET_ALL if self.use_colors else ""
            self.info(f"  Fallidos: {color}{stats['failed']}{reset}")

        if 'total_bugs' in stats:
            self.info(f"  Total bugs: {stats['total_bugs']}")

        if 'duration' in stats:
            duration = stats['duration']
            self.info(f"  Duracion: {duration:.2f} segundos")

            # Calcular throughput si hay items procesados
            if 'processed' in stats and stats['processed'] > 0:
                throughput = stats['processed'] / duration
                self.info(f"  Rendimiento: {throughput:.2f} items/seg")

        if 'location' in stats:
            self.info(f"  Ubicacion: {stats['location']}")

    def separator(self):
        """Imprime una línea separadora"""
        self._print("=" * 60)

    def note(self, text: str):
        """
        Imprime una nota informativa.

        Args:
            text: Texto de la nota
        """
        if self.use_colors:
            self._print(f"Nota: {text}", Fore.CYAN, Style.DIM)
        else:
            self._print(f"Nota: {text}")
