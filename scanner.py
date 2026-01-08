import os
import re
import fnmatch
from pathlib import Path
from typing import Set, Optional, List
import sys

class ProjectScanner:
    def __init__(self, root_dir: str = ".", output_file: str = "project_content.txt"):
        self.root_dir = Path(root_dir).resolve()
        self.output_file = Path(output_file).resolve()
        self.gitignore_patterns = []
        self._load_gitignore()
        
    def _load_gitignore(self) -> None:
        """Загружает и парсит .gitignore файлы"""
        gitignore_path = self.root_dir / ".gitignore"
        if gitignore_path.exists():
            with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.gitignore_patterns.append(line)
        
        # Всегда исключаем саму папку .git и стандартные временные файлы
        default_ignores = ['.git/', '__pycache__/', '*.pyc', '*.pyo', '*.pyd', '.env', 'venv/', '.venv/', 'env/']
        self.gitignore_patterns.extend(default_ignores)
        
        # Исключаем выходной файл, если он находится в корневой директории
        try:
            output_rel = self.output_file.relative_to(self.root_dir)
            self.gitignore_patterns.append(str(output_rel))
        except ValueError:
            # Выходной файл находится вне корневой директории, не добавляем в исключения
            pass
    
    def _is_ignored(self, path: Path) -> bool:
        """Проверяет, должен ли файл/папка быть проигнорирован"""
        try:
            rel_path = path.relative_to(self.root_dir)
        except ValueError:
            # Файл вне корневой директории
            return True
            
        rel_str = str(rel_path).replace('\\', '/')
        
        # Проверяем каждый шаблон
        for pattern in self.gitignore_patterns:
            # Убираем начальный / для шаблонов
            if pattern.startswith('/'):
                pattern = pattern[1:]
            
            # Проверяем точное совпадение или совпадение по шаблону
            if pattern.endswith('/'):
                # Папка: проверяем, начинается ли путь с этой папки
                if rel_str.startswith(pattern) or f"{rel_str}/".startswith(pattern):
                    return True
            else:
                # Файл: проверяем точное совпадение или шаблон fnmatch
                if rel_str == pattern or fnmatch.fnmatch(rel_str, pattern):
                    return True
                
                # Проверяем совпадение для любой части пути
                if '/' in pattern and fnmatch.fnmatch(rel_str, f"*/{pattern}"):
                    return True
        
        return False
    
    def _is_binary_file(self, file_path: Path) -> bool:
        """Определяет, является ли файл бинарным"""
        # Список бинарных расширений
        binary_extensions = {'.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.bin', 
                            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', 
                            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', 
                            '.tar', '.gz', '.rar', '.7z', '.mp3', '.mp4', '.avi'}
        
        if file_path.suffix.lower() in binary_extensions:
            return True
            
        # Проверяем первые несколько байт на наличие нулевых байтов
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\x00' in chunk
        except:
            return True
    
    def _get_file_content(self, file_path: Path) -> Optional[str]:
        """Получает содержимое файла в безопасном виде"""
        try:
            # Проверяем размер файла (не больше 1MB)
            if file_path.stat().st_size > 1024 * 1024:
                return f"[ФАЙЛ СЛИШКОМ ВЕЛИК: {file_path.stat().st_size} байт]"
            
            # Проверяем, не бинарный ли файл
            if self._is_binary_file(file_path):
                return f"[БИНАРНЫЙ ФАЙЛ: {file_path.stat().st_size} байт]"
            
            # Пробуем разные кодировки
            encodings = ['utf-8', 'cp1251', 'latin-1', 'iso-8859-1']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
                except Exception:
                    continue
            
            return f"[НЕ УДАЛОСЬ ПРОЧИТАТЬ ФАЙЛ: {file_path.stat().st_size} байт]"
                    
        except Exception as e:
            return f"[ОШИБКА ЧТЕНИЯ: {str(e)}]"
    
    def scan_project(self) -> None:
        """Основной метод сканирования проекта"""
        total_files = 0
        skipped_files = 0
        ignored_files = 0
        
        print(f"Начинаем сканирование проекта: {self.root_dir}")
        print(f"Выходной файл: {self.output_file}")
        print(f"Правил из .gitignore: {len(self.gitignore_patterns)}")
        
        with open(self.output_file, 'w', encoding='utf-8') as output:
            output.write("=" * 80 + "\n")
            output.write(f"СОДЕРЖАНИЕ ПРОЕКТА: {self.root_dir}\n")
            output.write("=" * 80 + "\n\n")
            
            # Рекурсивно обходим все файлы
            for root, dirs, files in os.walk(self.root_dir):
                root_path = Path(root)
                
                # Удаляем игнорируемые директории из списка для обхода
                dirs_to_remove = []
                for d in dirs:
                    dir_path = root_path / d
                    if self._is_ignored(dir_path):
                        dirs_to_remove.append(d)
                        ignored_files += 1
                
                for d in dirs_to_remove:
                    dirs.remove(d)
                
                for file in files:
                    file_path = root_path / file
                    
                    # Пропускаем игнорируемые файлы
                    if self._is_ignored(file_path):
                        ignored_files += 1
                        continue
                    
                    # Получаем содержимое файла
                    content = self._get_file_content(file_path)
                    if content is None:
                        skipped_files += 1
                        continue
                    
                    # Получаем относительный путь
                    try:
                        rel_path = file_path.relative_to(self.root_dir)
                    except ValueError:
                        rel_path = file_path
                    
                    # Записываем информацию о файле
                    output.write("\n" + "=" * 80 + "\n")
                    output.write(f"ФАЙЛ: {rel_path}\n")
                    output.write(f"ПОЛНЫЙ ПУТЬ: {file_path}\n")
                    output.write(f"РАЗМЕР: {file_path.stat().st_size} байт\n")
                    output.write("=" * 80 + "\n\n")
                    
                    # Записываем содержимое файла
                    output.write(content)
                    
                    # Добавляем разделитель
                    output.write("\n\n")
                    
                    total_files += 1
                    
                    # Выводим прогресс
                    if total_files % 10 == 0:
                        print(f"Обработано файлов: {total_files}, пропущено: {skipped_files}, игнорировано: {ignored_files}")
        
        # Статистика
        print(f"\n{'='*60}")
        print(f"СКАНИРОВАНИЕ ЗАВЕРШЕНО")
        print(f"{'='*60}")
        print(f"Обработано файлов: {total_files}")
        print(f"Пропущено файлов (ошибки чтения): {skipped_files}")
        print(f"Игнорировано файлов (по .gitignore): {ignored_files}")
        print(f"Всего проверено: {total_files + skipped_files + ignored_files}")
        print(f"Выходной файл: {self.output_file}")
        
        if self.output_file.exists():
            print(f"Размер выходного файла: {self.output_file.stat().st_size:,} байт")


def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Сканирует проект и создает текстовый файл со всем содержимым',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s                    # Сканирует текущую директорию
  %(prog)s --dir /путь/к/проекту
  %(prog)s --output проект.txt
  %(prog)s --dir . --output ../проект_копия.txt
        """
    )
    
    parser.add_argument('--dir', '-d', default='.', 
                       help='Корневая директория проекта (по умолчанию: текущая)')
    parser.add_argument('--output', '-o', default='project_content.txt',
                       help='Имя выходного файла (по умолчанию: project_content.txt)')
    
    args = parser.parse_args()
    
    try:
        scanner = ProjectScanner(root_dir=args.dir, output_file=args.output)
        scanner.scan_project()
    except KeyboardInterrupt:
        print("\n\nСканирование прервано пользователем.")
        sys.exit(1)
    except Exception as e:
        print(f"\nОшибка: {e}")
        print("Убедитесь, что:")
        print("1. Указанная директория существует")
        print("2. У вас есть права на чтение файлов")
        print("3. У вас есть права на запись в выходной файл")
        sys.exit(1)


if __name__ == "__main__":
    main()