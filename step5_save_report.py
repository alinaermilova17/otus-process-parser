from datetime import datetime

def save_report_to_file(report):
    """Сохраняет отчет в файл с временной меткой"""
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M")
    filename = f"{timestamp}-scan.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return filename

if __name__ == "__main__":
    from step1_get_ps_data import get_ps_output
    from step2_parse_process import parse_all_processes
    from step4_report import generate_report
    
    output = get_ps_output()
    if output:
        processes = parse_all_processes(output)
        report = generate_report(processes)
        print(report)
        filename = save_report_to_file(report)
        print(f"\nОтчет сохранен в файл: {filename}")
