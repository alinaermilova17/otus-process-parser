from collections import defaultdict

def generate_report(processes):
    """Генерирует полный отчет"""
    if not processes:
        return "Нет данных о процессах"
    
    users = sorted(set(proc['user'] for proc in processes))
    users_str = ', '.join(f"'{user}'" for user in users)
    
    total_processes = len(processes)
    
    user_counts = defaultdict(int)
    for proc in processes:
        user_counts[proc['user']] += 1
    user_stats = '\n'.join(f"{user}: {count}" 
                          for user, count in sorted(user_counts.items()))
    
    total_cpu = sum(proc['cpu'] for proc in processes)
    total_mem = sum(proc['mem'] for proc in processes)
    
    max_cpu_proc = max(processes, key=lambda x: x['cpu'])
    max_mem_proc = max(processes, key=lambda x: x['mem'])
    
    cpu_cmd = max_cpu_proc['command']
    if len(cpu_cmd) > 20:
        cpu_cmd = cpu_cmd[:20] + '...'
    
    mem_cmd = max_mem_proc['command']
    if len(mem_cmd) > 20:
        mem_cmd = mem_cmd[:20] + '...'
    
    report = f"""Отчёт о состоянии системы:
Пользователи системы: {users_str}
Процессов запущено: {total_processes}

Пользовательских процессов:
{user_stats}

Всего памяти используется: {total_mem:.1f}%
Всего CPU используется: {total_cpu:.1f}%
Больше всего памяти использует: {mem_cmd} ({max_mem_proc['mem']:.1f}%)
Больше всего CPU использует: {cpu_cmd} ({max_cpu_proc['cpu']:.1f}%)
"""
    return report

if __name__ == "__main__":
    from step1_get_ps_data import get_ps_output
    from step2_parse_process import parse_all_processes
    
    output = get_ps_output()
    if output:
        processes = parse_all_processes(output)
        report = generate_report(processes)
        print(report)
