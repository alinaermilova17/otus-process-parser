from collections import defaultdict

def get_users_list(processes):
    """Получаем список уникальных пользователей"""
    users = sorted(set(proc['user'] for proc in processes))
    return users

def count_processes_by_user(processes):
    """Считаем количество процессов по пользователям"""
    user_count = defaultdict(int)
    for proc in processes:
        user_count[proc['user']] += 1
    return dict(user_count)

def calculate_total_usage(processes):
    """Считаем общее использование CPU и памяти"""
    total_cpu = sum(proc['cpu'] for proc in processes)
    total_mem = sum(proc['mem'] for proc in processes)
    return total_cpu, total_mem

def find_max_process(processes, key):
    """Находит процесс с максимальным значением по ключу"""
    if not processes:
        return None, 0
    
    max_proc = max(processes, key=lambda x: x[key])
    command = max_proc['command']
    
    if len(command) > 20:
        command = command[:20] + '...'
    
    return command, max_proc[key]

if __name__ == "__main__":
    from step1_get_ps_data import get_ps_output
    from step2_parse_process import parse_all_processes
    
    output = get_ps_output()
    if output:
        processes = parse_all_processes(output)
        
        users = get_users_list(processes)
        user_counts = count_processes_by_user(processes)
        total_cpu, total_mem = calculate_total_usage(processes)
        max_cpu_proc, max_cpu_val = find_max_process(processes, 'cpu')
        max_mem_proc, max_mem_val = find_max_process(processes, 'mem')
        
        print("Пользователи:", ', '.join(f"'{u}'" for u in users))
        print(f"Всего процессов: {len(processes)}")
        print("\nПроцессов по пользователям:")
        for user, count in sorted(user_counts.items()):
            print(f"  {user}: {count}")
        print(f"\nВсего CPU: {total_cpu:.1f}%")
        print(f"Всего памяти: {total_mem:.1f}%")
        print(f"Больше всего CPU: {max_cpu_proc} ({max_cpu_val:.1f}%)")
        print(f"Больше всего памяти: {max_mem_proc} ({max_mem_val:.1f}%)")
