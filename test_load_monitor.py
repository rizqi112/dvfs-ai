"""test_load_monitor.py - Membebani CPU lalu memantau kenaikan penggunaan CPU.
Jalankan: python test_load_monitor.py [durasi_detik]
"""
import multiprocessing as mp
import sys
import time

from monitor import get_usage


def burn(stop_at: float):
    x = 0
    while time.time() < stop_at:
        x = (x * 31 + 7) % 1000003


def main():
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print("== Sebelum beban (3 detik) ==")
    for _ in range(3):
        u = get_usage(1.0)
        print(f"CPU: {u['cpu_percent']:5.1f}% | RAM: {u['ram_percent']:5.1f}%")

    n = mp.cpu_count()
    print(f"\n== Beban CPU dimulai: {n} proses selama {duration} detik ==")
    stop_at = time.time() + duration
    procs = [mp.Process(target=burn, args=(stop_at,)) for _ in range(n)]
    for p in procs:
        p.start()
    while time.time() < stop_at:
        u = get_usage(1.0)
        print(f"CPU: {u['cpu_percent']:5.1f}% | RAM: {u['ram_percent']:5.1f}%")
    for p in procs:
        p.join()

    print("\n== Setelah beban (3 detik) ==")
    for _ in range(3):
        u = get_usage(1.0)
        print(f"CPU: {u['cpu_percent']:5.1f}% | RAM: {u['ram_percent']:5.1f}%")


if __name__ == "__main__":
    main()
