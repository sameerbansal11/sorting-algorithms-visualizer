#!/usr/bin/env python3
"""
sorting-algorithms-visualizer
Visualizes 8 sorting algorithms in the terminal using ASCII bars.
Shows step-by-step comparisons, swaps, time complexity, and benchmarks.

Author: Sameer Bansal
Reg No: RA2311032010061
College: SRM Institute of Science and Technology
Branch: B.Tech CSE (IoT) | Batch: 2023-2027
"""

import os
import random
import time
import copy
import math

# ── Terminal Colors ───────────────────────────────────────
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
DIM = "\033[2m"


# ── Algorithm Metadata ────────────────────────────────────
ALGORITHMS = {
    "1": {
        "name": "Bubble Sort",
        "time_best": "O(n)",
        "time_avg": "O(n²)",
        "time_worst": "O(n²)",
        "space": "O(1)",
        "stable": True,
        "desc": "Repeatedly steps through the list, compares adjacent elements "
        "and swaps them if they are in the wrong order.",
    },
    "2": {
        "name": "Selection Sort",
        "time_best": "O(n²)",
        "time_avg": "O(n²)",
        "time_worst": "O(n²)",
        "space": "O(1)",
        "stable": False,
        "desc": "Divides the list into sorted and unsorted parts. Repeatedly "
        "finds the minimum from the unsorted part and places it at the front.",
    },
    "3": {
        "name": "Insertion Sort",
        "time_best": "O(n)",
        "time_avg": "O(n²)",
        "time_worst": "O(n²)",
        "space": "O(1)",
        "stable": True,
        "desc": "Builds the sorted array one item at a time by inserting each "
        "new element into its correct position.",
    },
    "4": {
        "name": "Merge Sort",
        "time_best": "O(n log n)",
        "time_avg": "O(n log n)",
        "time_worst": "O(n log n)",
        "space": "O(n)",
        "stable": True,
        "desc": "Divide and conquer algorithm. Splits the array in half, "
        "recursively sorts each half, then merges them back.",
    },
    "5": {
        "name": "Quick Sort",
        "time_best": "O(n log n)",
        "time_avg": "O(n log n)",
        "time_worst": "O(n²)",
        "space": "O(log n)",
        "stable": False,
        "desc": "Picks a pivot, partitions array around it so elements < pivot "
        "are left and elements > pivot are right, then recurses.",
    },
    "6": {
        "name": "Heap Sort",
        "time_best": "O(n log n)",
        "time_avg": "O(n log n)",
        "time_worst": "O(n log n)",
        "space": "O(1)",
        "stable": False,
        "desc": "Builds a max-heap from the array, then repeatedly extracts "
        "the maximum element and places it at the end.",
    },
    "7": {
        "name": "Shell Sort",
        "time_best": "O(n log n)",
        "time_avg": "O(n log² n)",
        "time_worst": "O(n²)",
        "space": "O(1)",
        "stable": False,
        "desc": "Generalization of insertion sort. Starts by sorting elements "
        "far apart, then reduces the gap until gap = 1.",
    },
    "8": {
        "name": "Counting Sort",
        "time_best": "O(n+k)",
        "time_avg": "O(n+k)",
        "time_worst": "O(n+k)",
        "space": "O(k)",
        "stable": True,
        "desc": "Non-comparison sort. Counts occurrences of each value, "
        "then reconstructs the sorted array. Works for integer ranges.",
    },
}


# ── Visualizer Core ───────────────────────────────────────
class Visualizer:
    """Tracks comparisons/swaps and renders ASCII bar charts."""

    def __init__(
        self, arr: list[int], delay: float = 0.08, bar_char: str = "█"
    ) -> None:
        self.arr = arr[:]
        self.original = arr[:]
        self.n = len(arr)
        self.delay = delay
        self.bar_char = bar_char
        self.comparisons = 0
        self.swaps = 0
        self.max_val = max(arr) if arr else 1
        self._comparing: set[int] = set()
        self._swapping: set[int] = set()
        self._sorted: set[int] = set()
        self._pivot: int | None = None

    def compare(self, i: int, j: int) -> bool:
        self.comparisons += 1
        self._comparing = {i, j}
        self._render()
        return self.arr[i] > self.arr[j]

    def swap(self, i: int, j: int) -> None:
        self.swaps += 1
        self._swapping = {i, j}
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
        self._render()
        self._swapping = set()

    def mark_sorted(self, *indices: int) -> None:
        for i in indices:
            self._sorted.add(i)

    def mark_pivot(self, idx: int | None) -> None:
        self._pivot = idx

    def final_render(self) -> None:
        self._sorted = set(range(self.n))
        self._comparing = set()
        self._swapping = set()
        self._pivot = None
        self._render()

    def _bar_color(self, idx: int) -> str:
        if idx in self._swapping:
            return RED
        if idx in self._comparing:
            return YELLOW
        if idx == self._pivot:
            return MAGENTA
        if idx in self._sorted:
            return GREEN
        return CYAN

    def _render(self) -> None:
        if self.delay == 0:
            return
        os.system("cls" if os.name == "nt" else "clear")

        MAX_HEIGHT = 16
        scale = MAX_HEIGHT / self.max_val

        rows = []
        for row in range(MAX_HEIGHT, 0, -1):
            line = "  "
            for i, val in enumerate(self.arr):
                filled = int(val * scale) >= row
                color = self._bar_color(i)
                line += f"{color}{self.bar_char}{RESET}" if filled else " "
                line += " "
            rows.append(line)

        label_line = "  "
        for val in self.arr:
            label_line += f"{DIM}{val:>2}{RESET}"

        print(f"\n{'─' * (self.n * 2 + 4)}")
        for r in rows:
            print(r)
        print(label_line)
        print(f"{'─' * (self.n * 2 + 4)}")
        print(
            f"  {YELLOW}Comparisons: {self.comparisons:<6}{RESET}  "
            f"{RED}Swaps: {self.swaps:<6}{RESET}  "
            f"{CYAN}[Yellow=Compare  Red=Swap  Green=Sorted  Magenta=Pivot]{RESET}"
        )

        time.sleep(self.delay)


# ── Sorting Algorithms ────────────────────────────────────


def bubble_sort(v: Visualizer) -> None:
    n = v.n
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if v.compare(j, j + 1):
                v.swap(j, j + 1)
                swapped = True
        v.mark_sorted(n - i - 1)
        if not swapped:
            break
    for i in range(v.n):
        v.mark_sorted(i)


def selection_sort(v: Visualizer) -> None:
    n = v.n
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            v.comparisons += 1
            v._comparing = {j, min_idx}
            v._render()
            if v.arr[j] < v.arr[min_idx]:
                min_idx = j
        if min_idx != i:
            v.swap(i, min_idx)
        v.mark_sorted(i)


def insertion_sort(v: Visualizer) -> None:
    for i in range(1, v.n):
        key = v.arr[i]
        j = i - 1
        v.mark_pivot(i)
        while j >= 0 and v.arr[j] > key:
            v.comparisons += 1
            v._comparing = {j, j + 1}
            v.arr[j + 1] = v.arr[j]
            v.swaps += 1
            v._render()
            j -= 1
        v.arr[j + 1] = key
        v.mark_sorted(j + 1)
    v.mark_pivot(None)
    for i in range(v.n):
        v.mark_sorted(i)


def merge_sort(v: Visualizer, left: int = 0, right: int = -1) -> None:
    if right == -1:
        right = v.n - 1
    if left >= right:
        return
    mid = (left + right) // 2
    merge_sort(v, left, mid)
    merge_sort(v, mid + 1, right)
    _merge(v, left, mid, right)


def _merge(v: Visualizer, left: int, mid: int, right: int) -> None:
    left_arr = v.arr[left : mid + 1]
    right_arr = v.arr[mid + 1 : right + 1]
    i = j = 0
    k = left
    while i < len(left_arr) and j < len(right_arr):
        v.comparisons += 1
        v._comparing = {left + i, mid + 1 + j}
        v._render()
        if left_arr[i] <= right_arr[j]:
            v.arr[k] = left_arr[i]
            i += 1
        else:
            v.arr[k] = right_arr[j]
            j += 1
        v.swaps += 1
        v.mark_sorted(k)
        k += 1
    while i < len(left_arr):
        v.arr[k] = left_arr[i]
        v.mark_sorted(k)
        i += 1
        k += 1
    while j < len(right_arr):
        v.arr[k] = right_arr[j]
        v.mark_sorted(k)
        j += 1
        k += 1


def quick_sort(v: Visualizer, low: int = 0, high: int = -1) -> None:
    if high == -1:
        high = v.n - 1
    if low < high:
        pi = _partition(v, low, high)
        quick_sort(v, low, pi - 1)
        quick_sort(v, pi + 1, high)


def _partition(v: Visualizer, low: int, high: int) -> int:
    pivot = v.arr[high]
    v.mark_pivot(high)
    i = low - 1
    for j in range(low, high):
        v.comparisons += 1
        v._comparing = {j, high}
        v._render()
        if v.arr[j] <= pivot:
            i += 1
            v.swap(i, j)
    v.swap(i + 1, high)
    v.mark_sorted(i + 1)
    v.mark_pivot(None)
    return i + 1


def heap_sort(v: Visualizer) -> None:
    n = v.n
    for i in range(n // 2 - 1, -1, -1):
        _heapify(v, n, i)
    for i in range(n - 1, 0, -1):
        v.swap(0, i)
        v.mark_sorted(i)
        _heapify(v, i, 0)
    v.mark_sorted(0)


def _heapify(v: Visualizer, n: int, i: int) -> None:
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n:
        v.comparisons += 1
        v._comparing = {left, largest}
        v._render()
        if v.arr[left] > v.arr[largest]:
            largest = left
    if right < n:
        v.comparisons += 1
        v._comparing = {right, largest}
        v._render()
        if v.arr[right] > v.arr[largest]:
            largest = right
    if largest != i:
        v.swap(i, largest)
        _heapify(v, n, largest)


def shell_sort(v: Visualizer) -> None:
    gap = v.n // 2
    while gap > 0:
        for i in range(gap, v.n):
            temp = v.arr[i]
            j = i
            v.mark_pivot(i)
            while j >= gap:
                v.comparisons += 1
                v._comparing = {j - gap, j}
                v._render()
                if v.arr[j - gap] > temp:
                    v.arr[j] = v.arr[j - gap]
                    v.swaps += 1
                    j -= gap
                else:
                    break
            v.arr[j] = temp
            v.mark_sorted(j)
        gap //= 2
    v.mark_pivot(None)
    for i in range(v.n):
        v.mark_sorted(i)


def counting_sort(v: Visualizer) -> None:
    max_val = max(v.arr)
    min_val = min(v.arr)
    offset = min_val
    count = [0] * (max_val - min_val + 1)
    for x in v.arr:
        v.comparisons += 1
        count[x - offset] += 1
    idx = 0
    for i, c in enumerate(count):
        for _ in range(c):
            v.arr[idx] = i + offset
            v.swaps += 1
            v.mark_sorted(idx)
            v._comparing = {idx}
            v._render()
            idx += 1


# ── Benchmarking ──────────────────────────────────────────
def benchmark_all(sizes: list[int] = [10, 50, 100, 200]) -> None:
    FUNCS = {
        "Bubble": lambda a: _run_sort(bubble_sort, a),
        "Selection": lambda a: _run_sort(selection_sort, a),
        "Insertion": lambda a: _run_sort(insertion_sort, a),
        "Merge": lambda a: _run_sort(merge_sort, a),
        "Quick": lambda a: _run_sort(quick_sort, a),
        "Heap": lambda a: _run_sort(heap_sort, a),
        "Shell": lambda a: _run_sort(shell_sort, a),
        "Counting": lambda a: _run_sort(counting_sort, a),
    }
    print(f"\n  {BOLD}⏱️  BENCHMARK (time in ms){RESET}")
    print(f"  {'Algorithm':<12}", end="")
    for s in sizes:
        print(f"  {f'n={s}':>8}", end="")
    print()
    print(f"  {'─' * (12 + len(sizes) * 10)}")
    for name, fn in FUNCS.items():
        print(f"  {name:<12}", end="", flush=True)
        for size in sizes:
            arr = random.sample(range(1, size * 10), size)
            t0 = time.perf_counter()
            fn(arr[:])
            ms = (time.perf_counter() - t0) * 1000
            color = GREEN if ms < 1 else YELLOW if ms < 10 else RED
            print(f"  {color}{ms:>7.2f}{RESET}", end="", flush=True)
        print()


def _run_sort(fn, arr: list[int]) -> list[int]:
    v = Visualizer(arr, delay=0)
    fn(v)
    return v.arr


# ── Display Helpers ───────────────────────────────────────
def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def display_banner() -> None:
    print("=" * 58)
    print("       📊 SORTING ALGORITHMS VISUALIZER")
    print("       Author : Sameer Bansal | RA2311032010061")
    print("       College: SRMIST Kattankulathur | CSE IoT")
    print("=" * 58)


def display_algorithm_info(algo: dict) -> None:
    stable = f"{GREEN}Yes{RESET}" if algo["stable"] else f"{RED}No{RESET}"
    print(f"""
  {BOLD}{algo['name']}{RESET}
  {'─' * 46}
  {algo['desc']}

  {BOLD}Complexity{RESET}
  Best Case   : {GREEN}{algo['time_best']}{RESET}
  Average     : {YELLOW}{algo['time_avg']}{RESET}
  Worst Case  : {RED}{algo['time_worst']}{RESET}
  Space       : {CYAN}{algo['space']}{RESET}
  Stable      : {stable}
""")


def pick_algorithm() -> tuple[str, dict]:
    print(f"\n  {BOLD}SELECT ALGORITHM{RESET}")
    print(f"  {'─' * 46}")
    for key, algo in ALGORITHMS.items():
        stable = f"{GREEN}✓{RESET}" if algo["stable"] else f"{RED}✗{RESET}"
        print(
            f"  [{key}] {algo['name']:<18} "
            f"Avg: {YELLOW}{algo['time_avg']:<14}{RESET} "
            f"Stable:{stable}"
        )
    print(f"  [9] Run ALL algorithms sequentially")
    print(f"  [b] Benchmark all (no animation)")
    choice = input("\n  → ").strip()
    return choice, ALGORITHMS.get(choice, ALGORITHMS["1"])


def pick_array() -> tuple[list[int], str]:
    print(f"\n  {BOLD}INPUT ARRAY{RESET}")
    print(f"  [1] Random shuffle  (default)")
    print(f"  [2] Nearly sorted")
    print(f"  [3] Reverse sorted  (worst case for many)")
    print(f"  [4] Many duplicates")
    print(f"  [5] Custom input")
    choice = input("  → ").strip()

    size_input = input("  Array size (5-30, default 15): ").strip()
    try:
        size = max(5, min(30, int(size_input)))
    except ValueError:
        size = 15

    if choice == "2":
        arr = list(range(1, size + 1))
        for _ in range(size // 5):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        label = "Nearly Sorted"
    elif choice == "3":
        arr = list(range(size, 0, -1))
        label = "Reverse Sorted"
    elif choice == "4":
        arr = [random.choice([1, 2, 3, 4, 5]) for _ in range(size)]
        label = "Many Duplicates"
    elif choice == "5":
        raw = input("  Enter space-separated integers: ").strip()
        try:
            arr = [int(x) for x in raw.split()]
            if not arr:
                raise ValueError
        except ValueError:
            print(f"  {YELLOW}Invalid. Using random.{RESET}")
            arr = random.sample(range(1, size * 2), size)
        label = "Custom"
    else:
        arr = random.sample(range(1, size * 2), size)
        label = "Random"

    return arr, label


def pick_speed() -> float:
    print(f"\n  {BOLD}ANIMATION SPEED{RESET}")
    print(f"  [1] Slow   (0.15s)  — great for learning")
    print(f"  [2] Medium (0.08s)  — default")
    print(f"  [3] Fast   (0.03s)  — quick overview")
    print(f"  [4] Instant (no animation) — stats only")
    choice = input("  → ").strip()
    return {"1": 0.15, "2": 0.08, "3": 0.03, "4": 0.0}.get(choice, 0.08)


def run_sort(algo_key: str, arr: list[int], delay: float) -> dict:
    sort_fns = {
        "1": bubble_sort,
        "2": selection_sort,
        "3": insertion_sort,
        "4": merge_sort,
        "5": quick_sort,
        "6": heap_sort,
        "7": shell_sort,
        "8": counting_sort,
    }
    fn = sort_fns.get(algo_key, bubble_sort)
    v = Visualizer(arr[:], delay=delay)
    algo = ALGORITHMS[algo_key]
    clear()
    display_banner()
    display_algorithm_info(algo)
    input(f"  Press ENTER to start visualization...")
    t0 = time.perf_counter()
    fn(v)
    elapsed = time.perf_counter() - t0
    v.final_render()
    return {
        "name": algo["name"],
        "comparisons": v.comparisons,
        "swaps": v.swaps,
        "time_ms": round(elapsed * 1000, 3),
        "n": v.n,
        "sorted": v.arr,
    }


def display_result(res: dict) -> None:
    print(f"\n  {BOLD}{GREEN}✅ SORT COMPLETE — {res['name']}{RESET}")
    print(f"  {'─' * 44}")
    print(f"  Array size   : {res['n']}")
    print(f"  Comparisons  : {YELLOW}{res['comparisons']}{RESET}")
    print(f"  Swaps/moves  : {RED}{res['swaps']}{RESET}")
    print(f"  Time taken   : {CYAN}{res['time_ms']} ms{RESET}")
    is_sorted = all(
        res["sorted"][i] <= res["sorted"][i + 1] for i in range(len(res["sorted"]) - 1)
    )
    print(
        f"  Correct sort : {GREEN}✅ YES{RESET}"
        if is_sorted
        else f"  Correct sort : {RED}❌ NO{RESET}"
    )


def run_all(arr: list[int], delay: float) -> None:
    results = []
    for key in ALGORITHMS:
        res = run_sort(key, arr, delay)
        display_result(res)
        results.append(res)
        input("  Press ENTER for next algorithm...")
    clear()
    display_banner()
    print(f"\n  {BOLD}📊 COMPARISON TABLE — All Algorithms (n={len(arr)}){RESET}")
    print(f"  {'─' * 62}")
    print(f"  {'Algorithm':<18} {'Comparisons':>12} {'Swaps':>8} {'Time (ms)':>10}")
    print(f"  {'─' * 62}")
    best_cmp = min(r["comparisons"] for r in results)
    best_time = min(r["time_ms"] for r in results)
    for r in results:
        cc = GREEN if r["comparisons"] == best_cmp else RESET
        tc = GREEN if r["time_ms"] == best_time else RESET
        print(
            f"  {r['name']:<18} {cc}{r['comparisons']:>12}{RESET} "
            f"{r['swaps']:>8} {tc}{r['time_ms']:>10.3f}{RESET}"
        )
    print(
        f"\n  {GREEN}🏆 Fewest comparisons: "
        f"{next(r['name'] for r in results if r['comparisons']==best_cmp)}{RESET}"
    )
    print(
        f"  {CYAN}⚡ Fastest: "
        f"{next(r['name'] for r in results if r['time_ms']==best_time)}{RESET}"
    )


def show_complexity_table() -> None:
    print(f"\n  {BOLD}📋 COMPLEXITY CHEAT SHEET{RESET}")
    print(f"  {'─' * 72}")
    print(
        f"  {'Algorithm':<18} {'Best':>10} {'Average':>14} {'Worst':>14} "
        f"{'Space':>8} {'Stable':>7}"
    )
    print(f"  {'─' * 72}")
    for algo in ALGORITHMS.values():
        stable = f"{GREEN}Yes{RESET}" if algo["stable"] else f"{RED}No {RESET}"
        print(
            f"  {algo['name']:<18} {GREEN}{algo['time_best']:>10}{RESET} "
            f"{YELLOW}{algo['time_avg']:>14}{RESET} {RED}{algo['time_worst']:>14}{RESET} "
            f"{CYAN}{algo['space']:>8}{RESET} {stable:>7}"
        )


def show_menu() -> None:
    print(f"""
  {BOLD}MENU{RESET}
  [1–8] Visualize a specific algorithm
  [9]   Run ALL algorithms on same array
  [b]   Benchmark all (speed comparison, no animation)
  [c]   Complexity cheat sheet
  [q]   Quit
""")


# ── Main ──────────────────────────────────────────────────
def main() -> None:
    clear()
    display_banner()
    print(f"\n  {GREEN}✅ Sorting Algorithms Visualizer Ready!{RESET}")
    print(f"  📚 Algorithms : {len(ALGORITHMS)}")
    print(f"  🎨 Visualization: ASCII bar chart in terminal")
    print(f"  📊 Tracks: comparisons, swaps, time taken")
    show_menu()

    while True:
        try:
            choice, algo_meta = pick_algorithm()

            if choice == "q":
                print(f"\n  👋 Goodbye! Keep sorting!\n")
                break

            elif choice == "c":
                show_complexity_table()
                input("\n  Press ENTER to continue...")
                show_menu()
                continue

            elif choice == "b":
                benchmark_all()
                input("\n  Press ENTER to continue...")
                show_menu()
                continue

            elif choice in ALGORITHMS or choice == "9":
                arr, label = pick_array()
                delay = pick_speed()
                print(f"\n  {CYAN}Array ({label}, n={len(arr)}): {arr}{RESET}")
                if choice == "9":
                    run_all(arr, delay)
                else:
                    res = run_sort(choice, arr, delay)
                    display_result(res)
                again = input("\n  🔄 Sort again? [y/n]: ").strip().lower()
                if again != "y":
                    show_menu()
            else:
                print(f"  {YELLOW}⚠️  Invalid. Enter 1-9, b, c, or q.{RESET}")

        except KeyboardInterrupt:
            print(f"\n\n  👋 Interrupted. Goodbye!")
            break


if __name__ == "__main__":
    main()
