"""Распознавание речи с помощью whisper-base"""
import os
import json
import uuid
from datetime import datetime

import torch, torchaudio
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from transformers import logging

logging.set_verbosity_error()

# Частота дискретизации
TARGET_SR = 16000
# Директория с транскрипциями
TRANSCRIPTIONS_PATH = "transcriptions"

# Инициализация модели
whisper_processor = WhisperProcessor.from_pretrained("models/whisper-base", )
whisper_model = WhisperForConditionalGeneration.from_pretrained("models/whisper-base", )

def _gen_id():
    """Генерация случайной строки для использования в имени файла"""
    return str(uuid.uuid4())[:8]

def resample_if_necessary(waveform, sr):
    """Приведение частоты дискретизации к 16kHz"""
    if sr != TARGET_SR:
        waveform = torchaudio.transforms.Resample(sr, TARGET_SR)(waveform)
    return waveform

def to_mono_if_necessary(waveform):
    """Усреднение по каналам записи"""
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)
    return waveform

def save_to_json(filepath, transcription):
    """Сохранение результата распознавания в json файл"""
    if not os.path.exists(TRANSCRIPTIONS_PATH):
        os.mkdir(TRANSCRIPTIONS_PATH)

    now = datetime.now()
    dt_str = now.strftime("%d.%m.%Y %H:%M:%S")

    # Записываем информацию в словарь    
    info = {"filepath": filepath, "text": transcription, "created_at": dt_str}

    # Создаем имя для json файла
    json_name = f"transcription_{os.path.basename(filepath).split('.')[0]}_{_gen_id()}.json"

    # Запись в файл
    with open(os.path.join(TRANSCRIPTIONS_PATH, json_name), "w") as f:
        json.dump(info, f)
    
    print(f"\nРезультат был записан в файл {os.path.join(TRANSCRIPTIONS_PATH, json_name)}")


def recognize(filepath):
    """Распознавание речи из файла с помощью Whisper"""
    waveform, sr = torchaudio.load(filepath)

    # Приводим к mono 16kHz
    waveform = to_mono_if_necessary(waveform)
    waveform = resample_if_necessary(waveform, sr)

    # Вычисление мелспектрограммы
    input_features = whisper_processor(
        waveform[0], sampling_rate=TARGET_SR, return_tensors="pt"
    ).input_features

    # Генерация токенов
    predicted_ids = whisper_model.generate(input_features, max_new_tokens=448)

    # Декодирование токенов в текст
    transcription = whisper_processor.batch_decode(predicted_ids, skip_special_tokens=True)

    return transcription[0]

