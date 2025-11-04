#!/usr/bin/env python3
import argparse
from src.synth import generate_synth
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000)
    ap.add_argument("--weeks", type=int, default=12)
    ap.add_argument("--sites", type=int, default=5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, default="./outputs/synth.csv")
    args = ap.parse_args()
    df = generate_synth(n=args.n, weeks=args.weeks, sites=args.sites, seed=args.seed)
    df.to_csv(args.out, index=False); print(f"Wrote {args.out}   rows={len(df)}")
if __name__ == "__main__": main()
