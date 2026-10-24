"""test_policy.py - Menguji keputusan kebijakan pada CPU 15%, 50%, 90% (level awal MEDIUM)."""
from dvfs_sim import DVFSSimulator
from q_learning import load_or_train, make_state

SCENARIOS = [15, 50, 90]


def main():
    agent = load_or_train()
    print(f"{'CPU':>5} | {'State':<14} | {'Action':<6} | {'Level':<6} | Daya")
    print("-" * 52)
    for cpu in SCENARIOS:
        sim = DVFSSimulator("MEDIUM")
        state = make_state(cpu, sim.level)
        action = agent.choose_action(state)
        r = sim.step(action, cpu)
        print(f"{cpu:4d}% | {state:<14} | {r['safe_action']:<6} | "
              f"{r['new_level']:<6} | {r['power_w']:.0f}W")


if __name__ == "__main__":
    main()
