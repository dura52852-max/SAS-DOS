import os
import sys
import time
import urllib.request
import urllib.error

# Глобальная настройка - имя папки, куда ставится ОС
BASE_DIR = "SAS-DOS_Virtual_Drive"

# ==========================================
# 1. УТИЛИТЫ И СИСТЕМНЫЕ ЭКРАНЫ
# ==========================================

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_bsod(error_type="disk"):
    clear_screen()
    print("\033[44;37m", end="")  # Синий фон, белый текст
    print("=" * 60)
    print(" SAS-DOS FATAL ERROR ".center(60, "="))
    print("=" * 60)
    
    if error_type == "disk":
        print("\nПроизошла критическая ошибка при попытке записи в сектор.")
        print("Инсталлятор экстренно остановлен во избежание повреждения.\n")
        print("STOP: 0x0005670 (0x00000001, 0x000003E8, 0x00000000)\n")
        print("*** Instaler crash 0x0005670\n")
        print("Критический сбой дисковой подсистемы.")
    elif error_type == "sys32":
        print("\nCRITICAL PROCESS DIED: Системный файл не найден!")
        print("Ядро операционной системы было повреждено или удалено.\n")
        print("STOP: 0x000000EF (0x00000000, 0x00000000, 0x00000000)\n")
        print("*** MISSING_OR_CORRUPT_KERNEL\n")
        print("Невозможно продолжить выполнение процессов.")

    print("Вы можете найти .log с ошибкой.")
    print("\n" + "=" * 60)
    print("\033[0m", end="")  # Сброс цвета
    
    print("\n[L] Открыть log файл")
    print("[Enter] Выйти")
    choice = input("\nВаш выбор: ").strip().lower()
    
    if choice == 'l':
        show_log(error_type)
    else:
        sys.exit()

def show_log(error_type):
    clear_screen()
    print("=== crash_report.log ===")
    print("TIME: 03:14:07 | KERNEL: PANIC")
    
    if error_type == "disk":
        print("[INFO] Target drive: india disk 1000gb")
        print("[INFO] Initializing partition table... OK.")
        print("[INFO] Starting low-level format...")
        print("\033[31m[ERROR] WRITE FAULT AT LBA 2097152 (Exactly 1GB boundary)\033[0m")
        print("\033[31m[CRITICAL] Drive firmware spoofing detected!\033[0m")
        print("[DEBUG] Real capacity: 1.00 GB (1024 MB)")
        print("[DEBUG] Spoofed capacity: 1000.00 GB")
        print("[FATAL] Instaler crash 0x0005670: Attempted to format non-existent memory.\n")
        print("=== КАК РЕШИТЬ ===")
        print("1. Извлеките этот диск из материнской платы.")
        print("2. Выбросьте его в окно.")
        print("3. В следующий раз не покупайте дешевые диски на blacktrade.ch.")
        print("4. Перезапустите инсталлятор и выберите нормальный HDD.")
    
    elif error_type == "sys32":
        print("[INFO] System running normally...")
        print("[WARN] File system change detected.")
        print("\033[31m[ERROR] system/kernel32.dll OR sas_main.exe IS MISSING!\033[0m")
        print("\033[31m[CRITICAL] Kernel memory space collapsed.\033[0m")
        print("[FATAL] MISSING_OR_CORRUPT_KERNEL\n")
        print("=== КАК РЕШИТЬ ===")
        print("1. Зачем вы удалили системные файлы?!")
        print("2. Система полностью уничтожена.")
        print("3. Удалите папку SAS-DOS_Virtual_Drive в Windows и запустите установку заново.")

    print("========================\n")
    input("Нажмите Enter для выхода...")
    sys.exit()

# Проверка жизненно важных файлов ядра
def check_system_integrity():
    critical_files = [
        os.path.join("system", "kernel32.dll"),
        "sas_main.exe"
    ]
    for file in critical_files:
        if not os.path.exists(file):
            return False
    return True


# ==========================================
# 2. ПРОГРАММЫ ОБОЛОЧКИ (БРАУЗЕР, РЕДАКТОР)
# ==========================================

def text_editor():
    print("\n--- SAS-DOS Text Editor ---")
    filename = input("Введите имя файла (например, note.txt): ").strip()
    if not filename:
        return

    print("\nВведите текст. Чтобы сохранить, введите 'SAVE' с новой строки.")
    print("-" * 30)

    lines = []
    while True:
        line = input("")
        if line.strip() == "SAVE":
            break
        lines.append(line)

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        print(f"\n[OK] Файл '{filename}' успешно сохранен!")
    except Exception as e:
        print(f"\n[ОШИБКА] Не удалось сохранить: {e}")

def text_browser():
    print("\n--- SAS-NET EXPLORER v1.0 ---")
    print("Внимание: Браузер работает в текстовом режиме.")
    url = input("Введите URL (например, example.com): ").strip()
    
    if not url:
        return

    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    print(f"\nУстановка соединения с {url}...")
    time.sleep(0.5)

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            clear_screen()
            print(f"--- РЕЗУЛЬТАТ ОТ: {url} ---\n")
            print(html[:2000])
            if len(html) > 2000:
                print("\n... [КОД ОБРЕЗАН ДЛЯ ЭКОНОМИИ ПАМЯТИ SAS-DOS] ...")
            
            print("\n" + "-" * 30)
            print("Соединение закрыто. Нажмите Enter для возврата.")
            input()

    except urllib.error.URLError as e:
        print(f"\n[ОШИБКА СЕТИ] Не удалось подключиться: {e.reason}")
    except Exception as e:
        print(f"\n[ОШИБКА] Что-то пошло не так: {e}")

# Сама оболочка (командная строка)
def sas_shell(username):
    clear_screen()
    print("SAS-DOS v1.1345.01 [Version 1.0.0.1]")
    print("(c) SAS Corporation. Core initialized.")
    print("Lead Coder: Maxim | Team: Saveliy, Matvey, Alice\n")
    print("Введите 'help' для списка команд.")

    while True:
        # ПРОВЕРКА ЦЕЛОСТНОСТИ ПРИ КАЖДОМ ДЕЙСТВИИ
        if not check_system_integrity():
            time.sleep(0.5)
            show_bsod("sys32")

        current_dir = os.getcwd()
        command_input = input(f"\n{username}@{current_dir}> ").strip()
        
        if not command_input:
            continue
            
        args = command_input.split()
        command = args[0].lower()

        if command == 'help':
            print("\nДоступные команды:")
            print("  help        - показать это сообщение")
            print("  clear       - очистить экран")
            print("  dir / ls    - показать файлы в текущей папке")
            print("  edit        - создать новый текстовый файл")
            print("  web         - открыть текстовый браузер")
            print("  del [файл]  - удалить файл (ОСТОРОЖНО!)")
            print("  exit        - выключить систему")
        
        elif command == 'clear':
            clear_screen()
            
        elif command == 'dir' or command == 'ls':
            print("\nСодержимое директории:")
            files = os.listdir('.')
            for f in files:
                if os.path.isdir(f):
                    print(f"  [DIR]   {f}")
                else:
                    print(f"  [FILE]  {f}")
                
        elif command == 'edit':
            text_editor()
            
        elif command == 'web':
            text_browser()
            
        elif command == 'del' or command == 'rm':
            if len(args) < 2:
                print("Синтаксис: del [имя_файла]")
                continue
            
            target = args[1]
            if os.path.exists(target) and os.path.isfile(target):
                os.remove(target)
                print(f"Файл {target} удален.")
            else:
                print(f"Файл '{target}' не найден или это директория.")
            
        elif command == 'exit':
            print("Завершение работы SAS-DOS...")
            time.sleep(1)
            sys.exit()
            
        else:
            print(f"'{command}' не является внутренней или внешней командой.")


# ==========================================
# 3. ГЛАВНЫЙ ИНСТАЛЛЯТОР
# ==========================================

def run_installer():
    # --- ЭТАП 1: ВЫБОР ЖЕЛЕЗА ---
    clear_screen()
    print("=== УСТАНОВЩИК SAS-DOS 1.1345.01 ===\n")
    print("[ЭТАП 1/3] Выбор оборудования")
    print("-" * 30)
    
    print("ВЫБЕРИТЕ ЖЕСТКИЙ ДИСК (HDD):")
    print("1. Super Mge disk 100gb")
    print("2. China disk free blacktrade.ch 230gb")
    print("3. American disk 300gb")
    print("4. india disk 1000gb")
    print("5. SumSung disk 500 gb")
    
    hdd_choice = input("\nВаш выбор (1-5): ").strip()
    
    clear_screen()
    print("=== УСТАНОВЩИК SAS-DOS 1.1345.01 ===\n")
    print("[ЭТАП 1/3] Выбор оборудования")
    print("-" * 30)
    print("ВЫБЕРИТЕ ОПЕРАТИВНУЮ ПАМЯТЬ (RAM):")
    print("1. operativka china free 5 gb")
    print("2. american chtyka 12 gb")
    print("3. sumsung 20 gb")
    
    ram_choice = input("\nВаш выбор (1-3): ").strip()

    # --- ЭТАП 1.5: АКТИВАЦИЯ КЛЮЧОМ ---
    clear_screen()
    print("=== УСТАНОВЩИК SAS-DOS 1.1345.01 ===\n")
    print("[ЭТАП 1.5] Активация продукта")
    print("-" * 30)
    print("Для продолжения установки введите ваш 12-значный лицензионный ключ.")
    print("Формат: XXXX-XXXX-XXXX")
    
    attempts = 0
    while True:
        key = input("\nВведите ключ: ").strip()
        
        if len(key) == 14 and key[4] == '-' and key[9] == '-' and key.replace('-', '').isdigit():
            print("\n\033[32m[OK] Ключ принят. Активация прошла успешно!\033[0m")
            time.sleep(1)
            break
        else:
            attempts += 1
            print(f"\n\033[31m[ОШИБКА] Неверный ключ. Попытка {attempts}/3\033[0m")
            if attempts >= 3:
                print("\nСлишком много неверных попыток. Защита от пиратства сработала.")
                time.sleep(1)
                show_bsod("disk") 
                return

    # --- ФОРМАТИРОВАНИЕ ---
    clear_screen()
    print("Инициализация разметки диска...\n")
    time.sleep(1)
    
    print("Подготовка структуры разделов:")
    for i in range(1, 101):
        if hdd_choice == '4' and i > 1:
            time.sleep(1)
            show_bsod("disk")
            return
            
        bar = '#' * (i // 5) + '.' * (20 - (i // 5))
        sys.stdout.write(f"\r[{bar}] {i}% Форматирование носителя...")
        sys.stdout.flush()
        time.sleep(0.04)
    
    print("\n\nДиск успешно подготовлен!")
    time.sleep(1)

    # --- ЭТАП 2: РАСПАКОВКА ФАЙЛОВ ---
    clear_screen()
    print("=== УСТАНОВЩИК SAS-DOS 1.1345.01 ===\n")
    print("[ЭТАП 2/3] Копирование файлов системы")
    print("-" * 30)
    print("Создание системных директорий...")
    time.sleep(0.8)

    os.makedirs(os.path.join(BASE_DIR, "system"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "drivers"), exist_ok=True)

    print(f" -> Создана корневая папка: C:\\{BASE_DIR}\\")
    time.sleep(0.4)
    print(f" -> Создана папка: C:\\{BASE_DIR}\\system\\")
    time.sleep(0.4)
    print(f" -> Создана папка: C:\\{BASE_DIR}\\drivers\\")
    print("-" * 30)
    time.sleep(1)

    files_to_create = {
        "system": ["kernel32.dll", "user32.dll", "gdi32.dll", "sas_shell.dll"],
        "drivers": ["vga_display.sys", "kbd_mouse.sys", "sound_sb.sys"],
        "": ["sas_main.exe"] 
    }

    print("Распаковка библиотек и исполняемых модулей:")
    for folder, files in files_to_create.items():
        for filename in files:
            file_path = os.path.join(BASE_DIR, folder, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("SAS-DOS SECURE SYSTEM FILE. EXECUTABLE BINARY DATA.")
            
            print(f" Извлечение: {file_path} ... Готово")
            time.sleep(0.2) 

    with open(os.path.join(BASE_DIR, "credits.txt"), 'w', encoding='utf-8') as f:
        f.write("=== SAS Corporation ===\nLead Coder: Maxim\nTeam: Saveliy, Matvey, Alice\nProject: SAS-DOS v1.1345.01")
    print(f" Извлечение: {os.path.join(BASE_DIR, 'credits.txt')} ... Готово")

    print("\nВсе системные компоненты успешно скопированы.")
    time.sleep(1.5)

    # --- ЭТАП 3: НАСТРОЙКА УЧЕТНОЙ ЗАПИСИ ---
    clear_screen()
    print("=== УСТАНОВЩИК SAS-DOS 1.1345.01 ===\n")
    print("[ЭТАП 3/3] Создание учетной записи")
    print("-" * 30)
    
    while True:
        username = input("Введите имя пользователя (Администратор): ").strip()
        if username:
            break
        print("\033[31mОшибка: Имя пользователя не может быть пустым!\033[0m")
    
    print("\nВведите пароль для защиты системы.")
    print("\033[33m(Оставьте поле пустым и нажмите Enter, чтобы пропустить)\033[0m")
    password = input("Пароль: ").strip()

    print("-" * 30)
    if not password:
        print(f"Пользователь {username} зарегистрирован (без пароля).")
    else:
        print(f"Пользователь {username} зарегистрирован. Пароль зашифрован.")
    
    # Сохраняем имя в конфиг для автозагрузки
    with open(os.path.join(BASE_DIR, "config.sys"), 'w', encoding='utf-8') as f:
        f.write(username)
        
    time.sleep(2)

    # --- ЗАВЕРШЕНИЕ ---
    clear_screen()
    print("=" * 60)
    print(" УСТАНОВКА SAS-DOS 1.1345.01 ЗАВЕРШЕНА! ".center(60, "#"))
    print("=" * 60)
    print(f"\nСистема успешно развернута для пользователя: {username}")
    print("Для завершения конфигурации требуется перезагрузка.")
    print("\n" + "=" * 60)
    
    input("\nНажмите [Enter] для перезагрузки и запуска SAS-DOS...")
    boot_system()


# ==========================================
# 4. ЗАГРУЗЧИК
# ==========================================

def boot_system():
    clear_screen()
    print("Перезагрузка BIOS...")
    time.sleep(1)
    print("Чтение boot-сектора...")
    time.sleep(0.5)
    
    os.chdir(BASE_DIR)
    
    username = "Admin"
    if os.path.exists("config.sys"):
        with open("config.sys", "r", encoding='utf-8') as f:
            username = f.read().strip()
            
    sas_shell(username)


def main():
    if os.name == 'nt':
        os.system('color')
        
    # ЛОГИКА ЗАПУСКА
    if os.path.exists(BASE_DIR) and os.path.exists(os.path.join(BASE_DIR, "sas_main.exe")):
        boot_system()
    else:
        run_installer()

if __name__ == "__main__":
    main()