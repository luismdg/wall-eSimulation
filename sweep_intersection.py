import argparse
import time
from LIB_TC2008B import IntersectionSim

parser = argparse.ArgumentParser(description='Sweep TS values to find best throughput')
parser.add_argument('--lifters', type=int, default=3)
parser.add_argument('--P', type=float, default=0.2)
parser.add_argument('--duration', type=float, default=60.0)
parser.add_argument('--minTS', type=float, default=2.0)
parser.add_argument('--maxTS', type=float, default=30.0)
parser.add_argument('--step', type=float, default=2.0)
args = parser.parse_args()

# Speed up by disabling sleeping used in the simulator
try:
    import time as _time_mod
    _time_mod.sleep = lambda s: None
except Exception:
    pass

results = []
TS = args.minTS
while TS <= args.maxTS:
    sim = IntersectionSim(args.lifters, TS, args.P, args.duration)
    sim.run()
    results.append((TS, sim.total))
    print(f"TS={TS:.1f} -> passed={sim.total}")
    TS += args.step

best = max(results, key=lambda x: x[1])
print('\n=== Sweep summary ===')
for t,p in results:
    print(f"TS={t:.2f} -> total_passed={p}")
print(f"\nBest TS={best[0]:.2f} with total passed={best[1]}")
