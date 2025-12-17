#!/usr/bin/env python3
"""Script para sincronizar las reglas de análisis visual al Knowledge Base"""
import sys
import os

# Agregamos el path del proyecto para importar los servicios
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv("env_vars/.env")

from services.knowledge_base_service import KnowledgeBaseService

def sync_rules():
    print("🚀 Iniciando sincronización de Reglas Visuales...")
    
    file_path = os.path.join(os.path.dirname(__file__), "../docs/reglas_analisis_visual.md")
    if not os.path.exists(file_path):
        print(f"❌ No se encontró el archivo: {file_path}")
        return

    kb_service = KnowledgeBaseService()
    
    # 1. Obtener ID del Store
    store_name = kb_service.get_or_create_store(display_name="Znuny_Tickets_KB")
    if not store_name:
        print("❌ No se pudo conectar al Store.")
        return

    # 2. Subir e indexar archivo
    print(f"📄 Archivo a subir: {file_path}")
    success = kb_service.upload_and_index_file(store_name, file_path)
    
    if success:
        print("\n✅ ¡Reglas sincronizadas con éxito!")
    else:
        print("\n❌ Falló la sincronización o indexado.")

if __name__ == "__main__":
    sync_rules()
