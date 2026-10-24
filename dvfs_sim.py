"""dvfs_sim.py - Simulator level DVFS (LOW / MEDIUM / HIGH) dan estimasi daya.

CATATAN: nilai performa dan daya adalah PARAMETER SIMULASI (Bab 3.5.4),
bukan hasil pengukuran CPU fisik.
"""

LEVELS = ["LOW", "MEDIUM", "HIGH"]
ACTIONS = ["DOWN", "KEEP", "UP"]

PERFORMANCE = {"LOW": 0.50, "MEDIUM": 0.75, "HIGH": 1.00}
POWER_WATT = {"LOW": 5.0, "MEDIUM": 10.0, "HIGH": 18.0}

# Bobot fungsi reward: R = -(W_LEVEL * |L - L_target|) - (W_POWER * P)
# Nilai ini dicocokkan dengan hasil pada modul (reward -1,50 / -3,00 / -5,40 / -13,00)
W_LEVEL = 40.0
W_POWER = 0.3

CPU_LOW_LIMIT = 30.0    # < 30%        -> LOW
CPU_HIGH_LIMIT = 70.0   # >= 70%       -> HIGH


def cpu_category(cpu_percent: float) -> str:
    """Kategori penggunaan CPU (Bab 3.5.1)."""
    if cpu_percent < CPU_LOW_LIMIT:
        return "LOW"
    if cpu_percent < CPU_HIGH_LIMIT:
        return "MEDIUM"
    return "HIGH"


def target_level(cpu_percent: float) -> str:
    """Level target = level yang namanya sama dengan kategori CPU."""
    return cpu_category(cpu_percent)


def safety_layer(level: str, action: str) -> str:
    """Safety layer (Bab 3.10): level tidak boleh keluar dari LOW..HIGH."""
    if level == "LOW" and action == "DOWN":
        return "KEEP"
    if level == "HIGH" and action == "UP":
        return "KEEP"
    return action


def next_level(level: str, action: str) -> str:
    idx = LEVELS.index(level)
    if action == "DOWN":
        idx -= 1
    elif action == "UP":
        idx += 1
    return LEVELS[max(0, min(len(LEVELS) - 1, idx))]


def calc_reward(level: str, cpu_percent: float) -> float:
    """Reward: makin dekat ke 0 makin baik."""
    l_target = PERFORMANCE[target_level(cpu_percent)]
    l_now = PERFORMANCE[level]
    return -(W_LEVEL * abs(l_now - l_target)) - (W_POWER * POWER_WATT[level])


class DVFSSimulator:
    def __init__(self, level: str = "MEDIUM"):
        self.level = level

    def step(self, action: str, cpu_percent: float) -> dict:
        """Jalankan satu langkah simulasi dan kembalikan hasilnya."""
        safe_action = safety_layer(self.level, action)
        old_level = self.level
        self.level = next_level(self.level, safe_action)
        return {
            "old_level": old_level,
            "chosen_action": action,
            "safe_action": safe_action,
            "new_level": self.level,
            "performance": PERFORMANCE[self.level],
            "power_w": POWER_WATT[self.level],
            "reward": calc_reward(self.level, cpu_percent),
        }
