#!/usr/bin/env python3
import subprocess
from collections import defaultdict
from datetime import datetime

def parse_ps_aux():
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, check=True)
        processes = []
        lines = result.stdout.strip().split('\n')
        for line in lines[1:]:
            if not line.strip():
                continue
            parts = line.split(None, 10)
            if len(parts) < 11:
                continue
            try:
                process = {
                    'user': parts[0],
                    'pid': int(parts[1]),
                    'cpu': float(parts[2]),
                    'mem': float(parts[3]),
                    'vsz': int(parts[4]),
                    'rss': int(parts[5]),
                    'tty': parts[6],
                    'stat': parts[7],
                    'start': parts[8],
                    'time': parts[9],
                    'command': parts[10]
                }
                processes.append(process)
            except (ValueError, IndexError):
                continue
        return processes
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Ошибка: {e}")
        return []

def generate_report(processes):
    if not processes:
        return "Нет данных о процессах\n"
    
    users = sorted(set(proc['user'] for proc in processes))
    users_str = ', '.join(f"'{user}'" for user in users)
    total_processes = len(processes)
    
    user_counts = defaultdict(int)
    for proc in processes:
        user_counts[proc['user']] += 1
    user_stats = '\n'.join(f"{user}: {count}" for user, count in sorted(user_counts.items()))
    
    total_cpu = sum(proc['cpu'] for proc in processes)
    total_mem = sum(proc['mem'] for proc in processes)
    
    max_cpu_proc = max(processes, key=lambda x: x['cpu'])
    max_mem_proc = max(processes, key=lambda x: x['mem'])
    
    def truncate(cmd):
        return cmd[:20] + '...' if len(cmd) > 20 else cmd
    
    report = f"""Отчёт о состоянии системы:
Пользователи системы: {users_str}
Процессов запущено: {total_processes}

Пользовательских процессов:
{user_stats}

Всего памяти используется: {total_mem:.1f}%
Всего CPU используется: {total_cpu:.1f}%
Больше всего памяти использует: {truncate(max_mem_proc['command'])} ({max_mem_proc['mem']:.1f}%)
Больше всего CPU использует: {truncate(max_cpu_proc['command'])} ({max_cpu_proc['cpu']:.1f}%)
"""
    return report

def save_report(report):
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M")
    filename = f"{timestamp}-scan.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    return filename

def main():
    print("Сбор информации о процессах...")
    processes = parse_ps_aux()
    if not processes:
        print("Не удалось получить данные о процессах.")
        return
    report = generate_report(processes)
    print("\n" + report)
    filename = save_report(report)
    print(f"\nОтчет сохранен в файл: {filename}")

if __name__ == "__main__":
    main()
