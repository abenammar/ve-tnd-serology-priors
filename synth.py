import numpy as np, pandas as pd
def generate_synth(n=5000, weeks=12, sites=5, seed=42):
    rng = np.random.default_rng(seed)
    week = rng.integers(1, weeks+1, size=n)
    site = rng.integers(1, sites+1, size=n)
    age = rng.normal(55, 12, size=n).clip(18, 95)
    sex = rng.integers(0, 2, size=n)
    base_prev = 0.25 + 0.1 * np.sin(week / 2.0) + 0.05 * (site % 3 == 0)
    base_prev = np.clip(base_prev, 0.05, 0.6)
    prior_inf_true = (rng.random(n) < base_prev).astype(int)
    logit_vax = -0.3 + 0.012*(age-50) + 0.2*(sex==1) - 0.6*prior_inf_true + 0.15*(site==1)
    p_vax = 1/(1+np.exp(-logit_vax))
    vaccinated = (rng.random(n) < p_vax).astype(int)
    b0 = -1.2 + 0.08*np.cos(week/3.0) + 0.1*(site==2)
    bV = -0.8; bZ = -0.9
    lp = b0 + bV*vaccinated + bZ*prior_inf_true + 0.01*(age-55)
    p_case = 1/(1+np.exp(-lp))
    case = (rng.random(n) < p_case).astype(int)
    Se_nom, Sp_nom = 0.92, 0.98
    serology_pos = np.where(
        prior_inf_true==1, (rng.random(n) < Se_nom).astype(int),
        (rng.random(n) > Sp_nom).astype(int)
    )
    return pd.DataFrame({
        "week": week, "site": site, "age": age.round(1), "sex": sex,
        "vaccinated": vaccinated, "prior_inf_true": prior_inf_true,
        "serology_pos": serology_pos, "case": case
    })
