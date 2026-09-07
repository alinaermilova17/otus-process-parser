import sys
import os
import json
import re
from collections import defaultdict, Counter


def parse_log_line(line):
    pattern = r'^(\S+) - - \[([^\]]+)\] "(\S+) (\S+) ([^"]+)" (\d+) (\S+) "([^"]*)" "([^"]*)" (\d+)$'
    match = re.match(pattern, line.strip())

    if not match:
        return None

    ip, timestamp, method, url, protocol, status, bytes_sent, referer, user_agent, duration = match.groups()

    return {
        'ip': ip,
        'timestamp': timestamp,
        'method': method,
        'url': url,
        'protocol': protocol,
        'status': int(status),
        'bytes': bytes_sent if bytes_sent != '-' else 0,
        'referer': referer,
        'user_agent': user_agent,
        'duration': int(duration)
    }


def analyze_log_file(file_path):
    stats = {
        'total_requests': 0,
        'methods': defaultdict(int),
        'ip_counter': Counter(),
        'top_slow_requests': []
    }

    slowest_requests = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                parsed = parse_log_line(line)
                if not parsed:
                    continue

                stats['total_requests'] += 1

                stats['methods'][parsed['method']] += 1

                stats['ip_counter'][parsed['ip']] += 1

                slowest_requests.append((
                    parsed['duration'],
                    parsed['method'],
                    parsed['url'],
                    parsed['ip'],
                    parsed['timestamp']
                ))

                slowest_requests.sort(key=lambda x: x[0], reverse=True)
                if len(slowest_requests) > 3:
                    slowest_requests = slowest_requests[:3]

    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")
        return None

    stats['methods'] = dict(stats['methods'])
    stats['top_ips'] = [
        {'ip': ip, 'count': count}
        for ip, count in stats['ip_counter'].most_common(3)
    ]
    stats['slowest_requests'] = [
        {
            'method': req[1],
            'url': req[2],
            'ip': req[3],
            'duration': req[0],
            'timestamp': req[4]
        }
        for req in slowest_requests
    ]
    del stats['ip_counter']

    return stats


def print_stats(stats, file_name):
    print(f"\n{'=' * 60}")
    print(f"Статистика для файла: {file_name}")
    print(f"{'=' * 60}")

    print(f"\nОбщее количество запросов: {stats['total_requests']}")

    print("\nЗапросы по HTTP-методам:")
    for method, count in sorted(stats['methods'].items()):
        print(f"  {method}: {count}")

    print("\nТоп-3 IP адресов:")
    for i, ip_info in enumerate(stats['top_ips'], 1):
        print(f"  {i}. {ip_info['ip']} - {ip_info['count']} запросов")

    print("\nТоп-3 самых долгих запросов:")
    for i, req in enumerate(stats['slowest_requests'], 1):
        print(f"  {i}. {req['method']} {req['url']}")
        print(f"     IP: {req['ip']}")
        print(f"     Длительность: {req['duration']} мс")
        print(f"     Время: {req['timestamp']}")

    print(f"\n{'=' * 60}\n")


def save_stats_to_json(stats, file_path, output_dir='.'):
    base_name = os.path.basename(file_path)
    json_name = f"{os.path.splitext(base_name)[0]}_stats.json"
    json_path = os.path.join(output_dir, json_name)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"Статистика сохранена в: {json_path}")
    return json_path


def main():
    """
    Главная функция скрипта
    """
    if len(sys.argv) != 2:
        print("Использование: python analyzer.py <путь_к_файлу_или_директории>")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print(f"Ошибка: путь {path} не существует")
        sys.exit(1)
    files_to_analyze = []

    if os.path.isfile(path):
        files_to_analyze.append(path)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            full_path = os.path.join(path, filename)
            if os.path.isfile(full_path):
                files_to_analyze.append(full_path)
    else:
        print(f"Ошибка: {path} не является файлом или директорией")
        sys.exit(1)

    if not files_to_analyze:
        print("Не найдено файлов для анализа")
        sys.exit(1)

    print(f"Найдено файлов для анализа: {len(files_to_analyze)}")

    for file_path in files_to_analyze:
        print(f"\nОбработка файла: {file_path}")

        stats = analyze_log_file(file_path)
        if not stats:
            continue

        print_stats(stats, os.path.basename(file_path))

        save_stats_to_json(stats, file_path, os.path.dirname(file_path))


if __name__ == "__main__":
    main()