import json
from datetime import datetime

def exportar_conversacion(messages):
    return json.dumps(messages, ensure_ascii=False, indent=2)

def nombre_archivo_chat():
    return f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json"