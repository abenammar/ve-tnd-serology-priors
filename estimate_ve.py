#!/usr/bin/env python3
import argparse, pandas as pd
from src.ve import naive_ve, serology_informed_ve
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--serology-se", type=float, default=0.92)
    ap.add_argument("--serology-sp", type=float, default=0.98); ap.add_argument("--n-imputations", type=int, default=50)
    ap.add_argument("--sample-se-sp", action="store_true"); ap.add_argument("--se-alpha", type=int, default=92)
    ap.add_argument("--se-beta", type=int, default=8); ap.add_argument("--sp-alpha", type=int, default=98)
    ap.add_argument("--sp-beta", type=int, default=2); ap.add_argument("--by", type=str, default=None)
    ap.add_argument("--out", type=str, default="./outputs/ve_by_week.csv"); args = ap.parse_args()
    df = pd.read_csv(args.data)
    naive = naive_ve(df, by=args.by)
    informed = serology_informed_ve(df, se=args.serology_se, sp=args.serology_sp, n_imputations=args.n_imputations,
                                    by=args.by, sample_se_sp=args.sample_se_sp, se_alpha=args.se_alpha, se_beta=args.se_beta,
                                    sp_alpha=args.sp_alpha, sp_beta=args.sp_beta)
    out = naive.merge(informed, on="stratum", how="left"); out.to_csv(args.out, index=False); print(f"Wrote {args.out}")
if __name__ == "__main__": main()
