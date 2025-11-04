#!/usr/bin/env python3
import argparse, pandas as pd, matplotlib.pyplot as plt
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ve", required=True); ap.add_argument("--out", default="./outputs/ve_by_week.png")
    args = ap.parse_args(); df = pd.read_csv(args.ve)
    if "stratum" not in df.columns: print("Expected a 'stratum' column for x axis."); return
    x = df["stratum"].astype(str); fig, ax = plt.subplots(figsize=(9,4))
    if "naive_ve" in df.columns: ax.plot(x, df["naive_ve"], marker="o", label="Naive VE")
    if "serology_informed_ve" in df.columns: ax.plot(x, df["serology_informed_ve"], marker="o", label="Serology-informed VE")
    ax.set_xlabel("Stratum"); ax.set_ylabel("VE (1 - OR)"); ax.set_ylim(-0.2, 1.0); ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout(); plt.savefig(args.out, dpi=150); print(f"Wrote {args.out}")
if __name__ == "__main__": main()
