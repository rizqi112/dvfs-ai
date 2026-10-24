"""main.py - Menggabungkan monitoring, keputusan Q-Learning, safety layer, dan simulator.
Contoh: python main.py --steps 30 --interval 1
Hasil dicatat di dvfs_results.csv
"""
import argparse
import csv
import time
from datetime import datetime

from dvfs_sim import DVFSSimulator
from monitor import get_usage
from q_learning import load_or_train, make_state

CSV_FILE = "dvfs_results.csv"
FIELDS = ["waktu", "cpu_percent", "ram_percent", "state", "action",
          "safe_action", "level_lama", "level_baru", "daya_w", "reward"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=30, help="jumlah langkah")
    ap.add_argument("--interval", type=float, default=1.0, help="detik per langkah")
    ap.add_argument("--learn", action="store_true", help="update Q-table saat berjalan")
    args = ap.parse_args()

    agent = load_or_train()
    sim = DVFSSimulator("MEDIUM")

    with open(CSV_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        print(f"{'CPU%':>6} {'RAM%':>6} {'STATE':<14} {'ACTION':<6} {'LEVEL':<14} {'DAYA':>5} {'REWARD':>8}")
        try:
            for _ in range(args.steps):
                u = get_usage(args.interval)
                state = make_state(u["cpu_percent"], sim.level)
                action = agent.choose_action(state, explore=args.learn)
                r = sim.step(action, u["cpu_percent"])
                if args.learn:
                    agent.update(state, action, r["reward"],
                                 make_state(u["cpu_percent"], r["new_level"]))
                w.writerow({
                    "waktu": datetime.now().strftime("%H:%M:%S"),
                    "cpu_percent": u["cpu_percent"], "ram_percent": u["ram_percent"],
                    "state": state, "action": r["chosen_action"],
                    "safe_action": r["safe_action"], "level_lama": r["old_level"],
                    "level_baru": r["new_level"], "daya_w": r["power_w"],
                    "reward": round(r["reward"], 2),
                })
                f.flush()
                print(f"{u['cpu_percent']:6.1f} {u['ram_percent']:6.1f} {state:<14} "
                      f"{r['safe_action']:<6} {r['old_level']+'->'+r['new_level']:<14} "
                      f"{r['power_w']:5.0f} {r['reward']:8.2f}")
        except KeyboardInterrupt:
            print("\nDihentikan oleh pengguna.")

    if args.learn:
        agent.save()
    print(f"\nLog disimpan ke {CSV_FILE}")


if __name__ == "__main__":
    main()
