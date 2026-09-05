def parse_process_line(line):
    """Разбирает одну строку из ps aux на поля"""
    parts = line.split(None, 10)
    
    if len(parts) < 11:
        return None
    
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
    
    return process

def parse_all_processes(ps_output):
    """Разбирает весь вывод ps aux"""
    lines = ps_output.strip().split('\n')
    processes = []
    
    for line in lines[1:]:
        if line.strip():
            proc = parse_process_line(line)
            if proc:
                processes.append(proc)
    
    return processes

if __name__ == "__main__":
    from step1_get_ps_data import get_ps_output
    
    output = get_ps_output()
    if output:
        processes = parse_all_processes(output)
        print(f"Найдено процессов: {len(processes)}")
        print("\nПример первых 3 процессов:")
        for i in range(min(3, len(processes))):
            proc = processes[i]
            print(f"  {proc['user']}: {proc['command'][:30]}... (CPU: {proc['cpu']}%, MEM: {proc['mem']}%)")
