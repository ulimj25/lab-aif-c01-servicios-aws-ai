"""
=============================================================================
Ejercicio 5: Pipeline de Audio - Polly + Transcribe (Python boto3)
Nivel: AUTONOMO
Duracion: ~20 minutos
=============================================================================

Objetivo: Construir un pipeline de audio completo que:

  1. Lea el titulo y texto de la primera noticia de data/noticias.json
  2. Use Amazon Polly (synthesize_speech) para generar un archivo MP3
     con la lectura del titulo
  3. Guarde el audio en data/output/noticia_audio.mp3
  4. (Bonus) Sube el MP3 a un bucket S3 y usa Amazon Transcribe
     (start_transcription_job) para transcribirlo de vuelta a texto

Servicios AWS:
  - Amazon Polly: Texto → Voz (TTS - Text to Speech)
  - Amazon Transcribe: Voz → Texto (STT - Speech to Text)

Parametros utiles de Polly:
  - VoiceId: 'Mia' (espanol mexicano), 'Lupe' (espanol US), 'Conchita' (espanol ES)
  - OutputFormat: 'mp3', 'ogg_vorbis', 'pcm'
  - Engine: 'neural' (mejor calidad) o 'standard'

Relacion con AIF-C01:
  - Task 1.2: Servicios de AI para procesamiento de voz
  - Polly y Transcribe son servicios complementarios (texto↔audio)
  - Concepto: pipeline de servicios AI encadenados

=============================================================================
"""

import boto3
import json

from pathlib import Path

# Configuración
bucket = "audio-pipeline-2026-04-21-12-40" 
region = "us-east-1"
polly_voz = "Mia"
formato = "mp3"
engine = "neural"

# Carga de las noticias
with open('data/noticias.json', 'r', encoding='utf-8') as f:
    noticias = json.load(f)

# Servicios AWS

polly = boto3.client("polly", region_name=region)
s3 = boto3.client("s3", region_name=region)
transcribe = boto3.client("transcribe", region_name=region)

# Obtener audio-stream de Polly

def sintetizar_speech(texto, voz_id=polly_voz, metodo=engine):

    respuesta = polly.synthesize_speech(
        Engine = metodo,
        VoiceId = voz_id,
        OutputFormat = formato,
        Text = texto
    )

    audio_bytes = respuesta["AudioStream"].read()

    print("Audio Generado:", len(audio_bytes)/1024)

    return audio_bytes

# Guardar el audio

def guardar_audio(audio_bytes, nombre):

    titulo_limpio = "".join(car if car.isalnum() else "_" for car in nombre)

    directorio = Path("data/output/"+titulo_limpio+".mp3")

    directorio.write_bytes(audio_bytes)

    return directorio

def pipeline_audio(noticias, nombre):

    titulo = noticias[0]['titulo']
    noticia = noticias[0]['texto']

    texto = f"{titulo}{": "}{noticia}"

    bytes_audio = sintetizar_speech(texto)

    archivo_audio = guardar_audio(bytes_audio, nombre)

    print("Archivo guardado en: ", archivo_audio)

pipeline_audio(noticias, "noticia_1_speech")
