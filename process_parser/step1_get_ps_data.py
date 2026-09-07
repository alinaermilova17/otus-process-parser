import subprocess

def get_ps_output():
    """Получаем вывод команды ps aux"""
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e}")
        return None
    except FileNotFoundError:
        print("Команда ps не найдена. Вы работаете в Linux?")
        return None

if __name__ == "__main__":
    output = get_ps_output()
    if output:
        print("Первые 10 строк вывода ps aux:")
        lines = output.split('\n')
        for i in range(min(10, len(lines))):
            print(lines[i])
