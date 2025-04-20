#!/usr/bin/env python3
"""
MSAD - Servidor de respaldos y acceso HTTP
Módulo principal con funcionalidades de servidor
"""
import os
import sqlite3
import datetime
import http.server
import socketserver
import threading
import sys
import shutil
import json
from queue import Queue
import time
import socket

# Importar configuración
from msad.config import (
    get_database_path,
    get_storage_dir,
    HTTP_PORT,
    get_backup_retention,
    ensure_directories,
    IS_WINDOWS
)

from msad.core.backup_manager import create_backup, cleanup_old_backups

class MSADServer:
    """Clase principal del servidor MSAD"""
    
    def __init__(self, start_http=True):
        """Inicializar el servidor MSAD"""
        # Asegurar que existen los directorios
        ensure_directories()
        
        # Variables de servidor
        self.server_thread = None
        self.httpd = None
        self.running = False
        
        # Cola de mensajes para comunicación entre hilos
        self.message_queue = Queue()
        
        # Iniciar servidor HTTP si se solicita
        if start_http:
            self.start_http_server()
    
    def start_http_server(self):
        """Iniciar el servidor HTTP"""
        def run():
            # Copiar el archivo index.html al directorio de almacenamiento
            index_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")
            storage_dir = get_storage_dir()
            
            if os.path.exists(index_path):
                shutil.copy2(index_path, os.path.join(storage_dir, "index.html"))
            
            os.chdir(storage_dir)
            handler = http.server.SimpleHTTPRequestHandler
            self.httpd = socketserver.TCPServer(("", HTTP_PORT), handler)
            
            # Obtener la IP local para mostrarla
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            
            print(f"\n[MSAD] Servidor HTTP iniciado en http://{ip}:{HTTP_PORT}")
            self.running = True
            
            # Añadir mensaje a la cola
            self.message_queue.put({
                "type": "server_started",
                "url": f"http://{ip}:{HTTP_PORT}"
            })
            
            self.httpd.serve_forever()
            
        self.server_thread = threading.Thread(target=run)
        self.server_thread.daemon = True
        self.server_thread.start()
        return True
    
    def stop_http_server(self):
        """Detener el servidor HTTP"""
        if self.httpd and self.running:
            self.httpd.shutdown()
            self.running = False
            self.message_queue.put({"type": "server_stopped"})
            print("[MSAD] Servidor HTTP detenido")
            return True
        return False
    
    def create_backup(self, notify=True):
        """Crear respaldo de la base de datos"""
        try:
            # Usar la función centralizada de respaldo
            result = create_backup()
            
            # Notificar del respaldo creado si es necesario
            if notify and result.get('success', False):
                self.message_queue.put({
                    "type": "backup_created",
                    "path": result.get('backup_path', ''),
                    "timestamp": result.get('timestamp', '')
                })
            elif notify:
                self.message_queue.put({
                    "type": "backup_error",
                    "error": result.get('error', 'Error desconocido')
                })
                
            return result
        except Exception as e:
            error_msg = f"Error al crear respaldo: {str(e)}"
            print(f"[MSAD] {error_msg}")
            
            if notify:
                self.message_queue.put({
                    "type": "backup_error",
                    "error": error_msg
                })
            
            return {
                "success": False,
                "error": error_msg
            }
    
    def get_server_status(self):
        """Obtener información del estado del servidor"""
        try:
            storage_dir = get_storage_dir()
            
            # Obtener la IP local
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            
            # Contar respaldos
            daily_count = len([f for f in os.listdir(os.path.join(storage_dir, "backups", "daily")) 
                              if f.endswith(".db")])
            weekly_count = len([f for f in os.listdir(os.path.join(storage_dir, "backups", "weekly")) 
                               if f.endswith(".db")])
            monthly_count = len([f for f in os.listdir(os.path.join(storage_dir, "backups", "monthly")) 
                                if f.endswith(".db")])
            
            # Calcular espacio utilizado
            if IS_WINDOWS:
                # Windows: usar os.path.getsize
                daily_size = sum(os.path.getsize(os.path.join(storage_dir, "backups", "daily", f)) 
                                for f in os.listdir(os.path.join(storage_dir, "backups", "daily")) 
                                if f.endswith(".db"))
                weekly_size = sum(os.path.getsize(os.path.join(storage_dir, "backups", "weekly", f)) 
                                 for f in os.listdir(os.path.join(storage_dir, "backups", "weekly")) 
                                 if f.endswith(".db"))
                monthly_size = sum(os.path.getsize(os.path.join(storage_dir, "backups", "monthly", f)) 
                                  for f in os.listdir(os.path.join(storage_dir, "backups", "monthly")) 
                                  if f.endswith(".db"))
            else:
                # Linux: usar comando du
                daily_size = os.popen(f"du -s {os.path.join(storage_dir, 'backups', 'daily')}").read().split()[0]
                weekly_size = os.popen(f"du -s {os.path.join(storage_dir, 'backups', 'weekly')}").read().split()[0]
                monthly_size = os.popen(f"du -s {os.path.join(storage_dir, 'backups', 'monthly')}").read().split()[0]
            
            return {
                "success": True,
                "server": {
                    "active": self.running,
                    "url": f"http://{ip}:{HTTP_PORT}" if self.running else None,
                    "port": HTTP_PORT
                },
                "storage": {
                    "path": storage_dir,
                    "database": get_database_path()
                },
                "backups": {
                    "daily": {
                        "count": daily_count,
                        "size": daily_size,
                        "retention": get_backup_retention("daily")
                    },
                    "weekly": {
                        "count": weekly_count,
                        "size": weekly_size,
                        "retention": get_backup_retention("weekly")
                    },
                    "monthly": {
                        "count": monthly_count,
                        "size": monthly_size,
                        "retention": get_backup_retention("monthly")
                    }
                }
            }
        except Exception as e:
            error_msg = f"Error al obtener estado del servidor: {str(e)}"
            print(f"[MSAD] {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }
    
    def run_interactive(self):
        """Ejecutar en modo interactivo con menú de consola"""
        while True:
            print("\n=== MSAD - Microservicio de Almacenamiento Distribuido ===")
            print("1. Crear respaldo manual")
            print("2. Ver información del servidor")
            print("3. Salir")
            
            try:
                option = input("\nSelecciona una opción: ")
                
                if option == "1":
                    print("\nCreando respaldo...")
                    result = self.create_backup()
                    if result["success"]:
                        print(f"Respaldo creado correctamente: {result['backup_path']}")
                    else:
                        print(f"Error: {result['error']}")
                    
                    input("\nPresiona Enter para continuar...")
                
                elif option == "2":
                    status = self.get_server_status()
                    
                    print("\n--- Estado del servidor ---")
                    if status["success"]:
                        print(f"Servidor HTTP: {'Activo' if status['server']['active'] else 'Inactivo'}")
                        if status["server"]["active"]:
                            print(f"URL: {status['server']['url']}")
                        print(f"Directorio de almacenamiento: {status['storage']['path']}")
                        print(f"Base de datos: {status['storage']['database']}")
                        
                        print("\n--- Respaldos ---")
                        print(f"Diarios: {status['backups']['daily']['count']} (se conservan {status['backups']['daily']['retention']})")
                        print(f"Semanales: {status['backups']['weekly']['count']} (se conservan {status['backups']['weekly']['retention']})")
                        print(f"Mensuales: {status['backups']['monthly']['count']} (se conservan {status['backups']['monthly']['retention']})")
                    else:
                        print(f"Error: {status.get('error', 'Error desconocido')}")
                    
                    input("\nPresiona Enter para continuar...")
                
                elif option == "3":
                    print("\nDeteniendo servidor MSAD...")
                    self.stop_http_server()
                    print("¡Hasta pronto!")
                    break
                
                else:
                    print("\nOpción no válida, inténtalo de nuevo.")
                    
            except KeyboardInterrupt:
                print("\n\nSaliendo...")
                self.stop_http_server()
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
                input("\nPresiona Enter para continuar...") 