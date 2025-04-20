#!/usr/bin/env python3
"""
MSAD - Punto de entrada principal
Ejecuta este script cuando quieras activar MSAD de forma independiente
"""
from msad.server.server_exports import MSADServer
from msad.config.config_exports import ensure_directories
from msad.core.core_exports import init as init_core

def main():
    """Función principal para ejecutar MSAD"""
    # Inicializar el núcleo
    init_core()
    
    # Asegurar que existan los directorios
    ensure_directories()
    
    # Iniciar servidor interactivo
    print("Iniciando servidor MSAD...")
    server = MSADServer()
    server.run_interactive()

if __name__ == "__main__":
    main() 