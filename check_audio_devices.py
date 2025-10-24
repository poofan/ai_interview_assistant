#!/usr/bin/env python3
"""
Проверка доступных аудиоустройств
"""

import sounddevice as sd
import sys

def check_audio_devices():
    """Проверяем доступные аудиоустройства"""
    print("Проверка аудиоустройств...")
    
    try:
        devices = sd.query_devices()
        print(f"\nНайдено {len(devices)} аудиоустройств:")
        
        for idx, device in enumerate(devices):
            name = device['name']
            input_channels = device.get('max_input_channels', 0)
            output_channels = device.get('max_output_channels', 0)
            
            print(f"\n[{idx}] {name}")
            print(f"    Входы: {input_channels}, Выходы: {output_channels}")
            
            # Проверяем на loopback устройства
            name_lower = name.lower()
            if any(keyword in name_lower for keyword in ['stereo mix', 'what u hear', 'monitor', 'loopback', 'stereo', 'mix']):
                print(f"    LOOPBACK УСТРОЙСТВО НАЙДЕНО!")
        
        # Проверяем устройство по умолчанию
        print(f"\nУстройство ввода по умолчанию:")
        try:
            default_input = sd.query_devices(kind='input')
            if default_input:
                print(f"    {default_input['name']} (каналов: {default_input.get('max_input_channels', 0)})")
            else:
                print("    Не найдено")
        except Exception as e:
            print(f"    Ошибка: {e}")
        
        print(f"\nУстройство вывода по умолчанию:")
        try:
            default_output = sd.query_devices(kind='output')
            if default_output:
                print(f"    {default_output['name']} (каналов: {default_output.get('max_output_channels', 0)})")
            else:
                print("    Не найдено")
        except Exception as e:
            print(f"    Ошибка: {e}")
        
        # Ищем loopback устройства
        print(f"\nПоиск loopback устройств...")
        loopback_found = False
        for idx, device in enumerate(devices):
            name = device['name'].lower()
            if any(keyword in name for keyword in ['stereo mix', 'what u hear', 'monitor', 'loopback']):
                print(f"    [{idx}] {device['name']} - LOOPBACK!")
                loopback_found = True
        
        if not loopback_found:
            print("    Loopback устройства не найдены")
            print("\nДля захвата системного аудио нужно:")
            print("    1. Включить 'Stereo Mix' в Windows:")
            print("       - Правый клик на иконку звука -> 'Открыть параметры звука'")
            print("       - 'Панель управления звуком' -> 'Запись'")
            print("       - Правый клик -> 'Показать отключенные устройства'")
            print("       - Правый клик на 'Stereo Mix' -> 'Включить'")
            print("    2. Или установить виртуальный аудио драйвер (VB-Cable, VoiceMeeter)")
        
    except Exception as e:
        print(f"Ошибка при проверке устройств: {e}")

if __name__ == "__main__":
    check_audio_devices()
