#!/usr/bin/env python3
import sys
import os
from google import genai

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dotenv import load_dotenv
load_dotenv("env_vars/.env")

from services.knowledge_base_service import KnowledgeBaseService

def list_kb_files():
    print("🚀 Listando archivos en KB...")
    
    svc = KnowledgeBaseService()
    store_name = svc.get_or_create_store(display_name="Znuny_Tickets_KB")
    print(f"Store: {store_name}")
    
    if not store_name:
        return

    try:
        # Use the client to list files in this store
        # Note: The specific API method might vary, we inspect the available methods
        # It seems we can query using filter or just list files generally if bound
        
        # Let's try listing files and checking metadata
        print("Consultando lista de archivos...")
        # Based on SDK, typically client.files.list() but filtered by store?
        # Or client.file_search_stores.list_files(name=...)
        
        # We will try the most likely method:
        pager = svc.client.files.list()
        found = False
        for f in pager:
            print(f" - {f.name} | {f.display_name} | {f.mime_type}")
            # Check if this file is the one we want
            if "reglas_analisis_visual.md" in f.display_name:
                found = True
                print("   ✅ ESTE ES EL DOCUMENTO!")
        
        if not found:
            print("❌ No se encontró 'reglas_analisis_visual.md' en la lista general de archivos.")
            
    except Exception as e:
        print(f"Error listando: {e}")

if __name__ == "__main__":
    list_kb_files()
