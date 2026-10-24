"""plot_results.py - Membuat 3 grafik dari evaluation_results.csv."""
import csv

import matplotlib
matplotlib.use("Agg")          # aman untuk server tanpa tampilan (SSH)
import matplotlib.pyplot as plt

from dvfs_sim import LEVELS

IN_FILE = "evaluation_results.csv"


def load():
    with open(IN_FILE) as f:
        return list(csv.DictReader(f))


def bar_compare(labels, a, b, la, lb, title, ylabel, out):
    x = range(len(labels))
    w = 0.35
    plt.figure(figsize=(7, 4.5))
    plt.bar([i - w / 2 for i in x], a, w, label=la)
    plt.bar([i + w / 2 for i in x], b, w, label=lb)
    plt.xticks(list(x), labels)
    plt.xlabel("Skenario penggunaan CPU")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    print("Disimpan:", out)


def main():
    rows = load()
    labels = [f"{r['cpu_simulasi']}%" for r in rows]

    bar_compare(labels,
                [float(r["daya_baseline"]) for r in rows],
                [float(r["daya_ai"]) for r in rows],
                "Baseline", "AI Q-Learning",
                "Perbandingan Estimasi Daya", "Estimasi daya (W)",
                "grafik_perbandingan_daya.png")

    # grafik level DVFS
    plt.figure(figsize=(7, 4.5))
    ys = [LEVELS.index(r["level_ai"]) for r in rows]
    plt.plot(labels, ys, marker="o")
    plt.yticks(range(len(LEVELS)), LEVELS)
    plt.xlabel("Skenario penggunaan CPU")
    plt.ylabel("Level DVFS terpilih")
    plt.title("Pemilihan Level DVFS oleh AI")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig("grafik_level_dvfs.png", dpi=150)
    plt.close()
    print("Disimpan: grafik_level_dvfs.png")

    bar_compare(labels,
                [float(r["reward_baseline"]) for r in rows],
                [float(r["reward_ai"]) for r in rows],
                "Baseline", "AI Q-Learning",
                "Perbandingan Reward", "Reward (lebih dekat ke 0 = lebih baik)",
                "grafik_reward.png")


if __name__ == "__main__":
    main()
