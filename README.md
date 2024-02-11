# recognition-app
Консольное приложение на Python для распознавания речи и модификации аудиофайлов.

Примеры аудиозаписей на русском и английском языках расположены в директории `wavs`.

## Установка

```sh
sudo apt update && sudo apt install ffmpeg

pip install torch torchvision torchaudio
pip install transformers
```

## Использование
```sh
python modif_rec.py
```
### Распознавание речи
Предварительно файл приводится к формату mono, 16kHz.

Распознавание осуществляется с помощью загруженной в директорию `models` модели `whisper-base`.

Результат распознавания записывается в json файл, сохраняющийся в директории `transcriptions`
```json
{"filepath": "/path/to/file.wav", "text": "text transcription", "created_at": "DD.MM.YYYY HH:MM"}
```

### Модификация аудиофайла
Изменение громкости и скорости воспроизведения осуществляется с помощью `torchaudio.transforms`.

Измененный файл записывается в директорию `wavs_modified/` с указанием параметров модификации.