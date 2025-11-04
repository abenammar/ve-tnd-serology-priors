# Serology-informed VE in Test-Negative Designs (TND)

This repository provides a small, reproducible pipeline to estimate vaccine effectiveness (VE) in a test-negative design with bias correction for prior infection using imperfect serology.

- Naive VE: from the case–control odds ratio in the TND (VE = 1 - OR).
- Serology-informed VE: multiple-imputation of latent prior infection, using test sensitivity (Se) and specificity (Sp); optional uncertainty propagation by sampling Se/Sp and averaging VE.

Everything runs on pure Python (numpy, pandas, scipy, scikit-learn, matplotlib). No MCMC dependency.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1) Generate a synthetic dataset (weeks x sites)
python scripts/generate_synth.py --n 5000 --weeks 12 --sites 5 --seed 42

# 2) Estimate VE (naive and serology-informed)
python scripts/estimate_ve.py   --data ./outputs/synth.csv   --serology-se 0.92 --serology-sp 0.98   --n-imputations 50   --sample-se-sp   --se-alpha 92 --se-beta 8   --sp-alpha 98 --sp-beta 2   --by week   --out ./outputs/ve_by_week.csv

# 3) Plot VE over time
python scripts/plot_ve.py --ve ./outputs/ve_by_week.csv --out ./outputs/ve_by_week.png
```

Outputs:
- outputs/synth.csv: synthetic dataset
- outputs/ve_by_week.csv: table with naive and serology-informed VE by stratum
- outputs/ve_by_week.png: simple plot

## License
MIT
