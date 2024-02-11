"""Изменение громкости и скорости воспроизведения в аудиофайле"""
import os
import torchaudio

def change_volume(waveform, gain_in_db):
    """Изменение громкости"""
    if gain_in_db != 0:
        waveform = torchaudio.transforms.Vol(gain=gain_in_db, gain_type="db")(waveform)
    return waveform

def change_speed(waveform, sr, speed_rate):
    """Изменение скорости"""
    if speed_rate != 1.:
        waveform = torchaudio.transforms.Speed(orig_freq=sr, factor=speed_rate)(waveform)[0]
    return waveform

def modify_audio(filepath, gain_in_db=0., speed_rate=1.):
    """Модификация аудиозаписи"""
    waveform, sr = torchaudio.load(filepath)

    # Изменение скорости
    waveform = change_speed(waveform, sr, speed_rate)
    
    # Изменение громкости
    waveform = change_volume(waveform, gain_in_db)

    # Сохранение измененного файла
    init_filename = os.path.basename(filepath).split(".")[0]

    if not os.path.exists("./wavs_modified"):
        os.mkdir("wavs_modified")

    new_path = os.path.join("wavs_modified", f"{init_filename}_gain{gain_in_db}_speed{speed_rate}.wav")
    torchaudio.save(new_path, waveform, sr)
    print(f"Модифицированный файл сохранен: {new_path}")

