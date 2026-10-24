"""evaluate.py - Membandingkan baseline (selalu MEDIUM) dengan kebijakan Q-Learning."""
import csv

from dvfs_sim import POWER_WATT, DVFSSimulator, calc_reward
from q_learning import load_or_train, make_state

SCENARIOS = [15, 50, 90]
OUT_FILE = "evaluation_results.csv"


def main():
    agent = load_or_train()
    rows = []
    for cpu in SCENARIOS:
        # baseline: level tetap MEDIUM
        base_level = "MEDIUM"
        base_power = POWER_WATT[base_level]
        base_reward = calc_reward(base_level, cpu)

        # AI Q-Learning
        sim = DVFSSimulator("MEDIUM")
        state = make_state(cpu, sim.level)
        r = sim.step(agent.choose_action(state), cpu)

        rows.append({
            "cpu_simulasi": cpu,
            "level_baseline": base_level,
            "daya_baseline": base_power,
            "reward_baseline": round(base_reward, 2),
            "action_ai": r["safe_action"],
            "level_ai": r["new_level"],
            "daya_ai": r["power_w"],
            "reward_ai": round(r["reward"], 2),
        })

    with open(OUT_FILE, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"{'CPU':>5} | {'Daya Base':>9} | {'Daya AI':>7} | {'Reward Base':>11} | {'Reward AI':>9}")
    print("-" * 56)
    for x in rows:
        print(f"{x['cpu_simulasi']:4d}% | {x['daya_baseline']:8.0f}W | {x['daya_ai']:6.0f}W | "
              f"{x['reward_baseline']:11.2f} | {x['reward_ai']:9.2f}")
    avg_b = sum(x["daya_baseline"] for x in rows) / len(rows)
    avg_a = sum(x["daya_ai"] for x in rows) / len(rows)
    print(f"\nRata-rata daya  baseline: {avg_b:.1f}W | AI: {avg_a:.1f}W")
    print("Catatan: nilai daya adalah parameter simulasi, bukan pengukuran fisik.")
    print(f"Data disimpan ke {OUT_FILE}")


if __name__ == "__main__":
    main()
