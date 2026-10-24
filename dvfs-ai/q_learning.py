"""q_learning.py - Agen Q-Learning untuk keputusan DVFS (UP / KEEP / DOWN).

State  : <kategori CPU>_<level saat ini>, contoh LOW_MEDIUM, HIGH_MEDIUM
Action : DOWN, KEEP, UP
"""
import json
import os
import random

from dvfs_sim import (ACTIONS, LEVELS, DVFSSimulator, calc_reward,
                      cpu_category, safety_layer, next_level)

Q_TABLE_FILE = "q_table.json"


def make_state(cpu_percent: float, level: str) -> str:
    return f"{cpu_category(cpu_percent)}_{level}"


def all_states():
    return [f"{c}_{l}" for c in LEVELS for l in LEVELS]


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.3, epsilon=0.2):
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount factor
        self.epsilon = epsilon  # peluang eksplorasi
        self.q = {s: {a: 0.0 for a in ACTIONS} for s in all_states()}

    # ---- keputusan ----
    def choose_action(self, state: str, explore: bool = False) -> str:
        if explore and random.random() < self.epsilon:
            return random.choice(ACTIONS)
        values = self.q[state]
        best = max(values.values())
        best_actions = [a for a, v in values.items() if v == best]
        # urutan prioritas jika seri: KEEP dulu agar stabil
        for pref in ("KEEP", "DOWN", "UP"):
            if pref in best_actions:
                return pref
        return best_actions[0]

    # ---- pembelajaran ----
    def update(self, state, action, reward, next_state):
        best_next = max(self.q[next_state].values())
        old = self.q[state][action]
        self.q[state][action] = old + self.alpha * (reward + self.gamma * best_next - old)

    # ---- simpan / muat ----
    def save(self, path: str = Q_TABLE_FILE):
        with open(path, "w") as f:
            json.dump(self.q, f, indent=2)

    def load(self, path: str = Q_TABLE_FILE) -> bool:
        if not os.path.exists(path):
            return False
        with open(path) as f:
            self.q = json.load(f)
        return True


def train(episodes: int = 20000, seed: int = 42, verbose: bool = True) -> QLearningAgent:
    """Latih agen pada simulator dengan beban CPU acak 0-100%."""
    random.seed(seed)
    agent = QLearningAgent()
    for ep in range(episodes):
        level = random.choice(LEVELS)
        cpu = random.uniform(0, 100)
        state = make_state(cpu, level)
        action = agent.choose_action(state, explore=True)
        safe = safety_layer(level, action)
        new_level = next_level(level, safe)
        reward = calc_reward(new_level, cpu)
        next_cpu = random.uniform(0, 100)           # beban berikutnya
        agent.update(state, action, reward, make_state(next_cpu, new_level))
    if verbose:
        print(f"Training selesai ({episodes} langkah).")
    return agent


def load_or_train(path: str = Q_TABLE_FILE) -> QLearningAgent:
    agent = QLearningAgent()
    if not agent.load(path):
        print("q_table.json belum ada -> melatih agen...")
        agent = train()
        agent.save(path)
    return agent


if __name__ == "__main__":
    a = train()
    a.save()
    print(f"Q-table disimpan ke {Q_TABLE_FILE}")
    for s, vals in a.q.items():
        print(s, {k: round(v, 2) for k, v in vals.items()})
