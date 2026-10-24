"""monitor.py - Memantau penggunaan CPU dan RAM memakai psutil.
Jalankan: python monitor.py   (hentikan dengan Ctrl+C)
"""
import time
import psutil


def get_usage(interval: float = 1.0) -> dict:
    cpu = psutil.cpu_percent(interval=interval)   # rata-rata selama 'interval' detik
    mem = psutil.virtual_memory()
    return {
        "cpu_percent": cpu,
        "ram_percent": mem.percent,
        "ram_used_gb": mem.used / (1024 ** 3),
    }


def main():
    print("Monitoring CPU & RAM (Ctrl+C untuk berhenti)\n")
    try:
        while True:
            u = get_usage(1.0)
            print(f"CPU: {u['cpu_percent']:5.1f}% | "
                  f"RAM: {u['ram_percent']:5.1f}% | "
                  f"RAM terpakai: {u['ram_used_gb']:.2f} GB")
    except KeyboardInterrupt:
        print("\nMonitoring dihentikan.")


if __name__ == "__main__":
    main()
