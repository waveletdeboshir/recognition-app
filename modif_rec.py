"""Консольное приложение для модификации wav файла, либо распознавание речи в wav файле"""
import os

from recognition import recognize, save_to_json
from effects import modify_audio

def main():

    # Запрос имени файла для обработки
    filepath = input("1. Введите путь до wav файла: ")

    while not (os.path.exists(filepath) == True and filepath.endswith(".wav")):
        filepath = input("\nВведен неверный путь, пожалуйста, введите существующий путь до wav файла: ")


    # Выбор функции приложения
    function = None
    while function not in (1, 2):
        function_str = input("\n2. Введите \n 1 - если хотите модифицировать файл \n 2 - если хотите распознать речь в файле: ")
        try:
            function = int(function_str)
        except:
            function = None
        
        if function not in (1, 2):
            print("\nВведено неверное число. Пожалуйста, введите 1 или 2.\n")

    # Модификация аудиозаписи
    if function == 1:
        # Скорость
        speed_rate = None
        speed_limits = (0, 5)
        while not speed_rate or speed_rate <= speed_limits[0] or speed_rate > speed_limits[1]:
            speed_rate_str = input(f"\n3. Введите 1, если не хотите изменить скорость записи;\n вещественное число > 0 и < 1, если хотите замедлить запись;\n вещественное число > 1 и <= {speed_limits[1]}, если хотите ускорить запись: ")
            try:
                speed_rate = float(speed_rate_str)
                
            except:
                speed_rate = None

            if not speed_rate or speed_rate <= speed_limits[0] or speed_rate > speed_limits[1]:
                    print(f"\nПожалуйста, введите число > {speed_limits[0]} и <= {speed_limits[1]}.\n")

        # Громкость
        gain = None
        gain_limits = (-10, 10)
        while gain is None or gain < gain_limits[0] or gain > gain_limits[1]:
            gain_str = input(f"\n4. Введите число децибел, на которое хотите изменить громкость записи (от {gain_limits[0]} до {gain_limits[1]}): ")
            try:
                gain = float(gain_str)
                
            except:
                gain = None

            if gain is None or gain < gain_limits[0] or gain > gain_limits[1]:
                    print(f"\nПожалуйста, введите число от {gain_limits[0]} до {gain_limits[1]}.\n")

        modify_audio(filepath=filepath, gain_in_db=gain, speed_rate=speed_rate)

    elif function == 2:
        transcription = recognize(filepath=filepath)
        print(f"\nРезультат распознавания: \n{transcription[:200]}")

        # Логирование в файл
        save_to_json(filepath=os.path.abspath(filepath), transcription=transcription)

if __name__ == "__main__":
    main()
    
