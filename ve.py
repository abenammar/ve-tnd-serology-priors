import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from scipy.stats import beta
from .serology import rogan_gladen, p_z1_given_serology
def tnd_or(counts):
    a,b,c,d = counts['a'], counts['b'], counts['c'], counts['d']
    if min(a,b,c,d) == 0: a+=0.5; b+=0.5; c+=0.5; d+=0.5
    return (a/b) / (c/d)
def ve_from_or(or_val): return 1.0 - or_val
def naive_ve(df, by=None):
    groups = [("overall", df)] if by is None else df.groupby(by)
    rows = []
    for key, g in groups:
        a = int(((g['case']==1)&(g['vaccinated']==1)).sum())
        b = int(((g['case']==0)&(g['vaccinated']==1)).sum())
        c = int(((g['case']==1)&(g['vaccinated']==0)).sum())
        d = int(((g['case']==0)&(g['vaccinated']==0)).sum())
        OR = tnd_or({'a':a,'b':b,'c':c,'d':d}); VE = ve_from_or(OR)
        rows.append({'stratum': key if by else 'overall', 'naive_or': OR, 'naive_ve': VE, 'a':a,'b':b,'c':c,'d':d})
    return pd.DataFrame(rows)
def serology_informed_ve(df, se=0.92, sp=0.98, n_imputations=50, by=None,
                         sample_se_sp=False, se_alpha=92, se_beta=8, sp_alpha=98, sp_beta=2, random_state=0):
    rng = np.random.default_rng(random_state)
    strata = [("overall", df.copy())] if by is None else list(df.groupby(by))
    out_rows = []
    for key, g in strata:
        g = g.copy(); obs_prev = g['serology_pos'].mean(); log_or_draws = []
        for _ in range(n_imputations):
            if sample_se_sp:
                se_m = beta.rvs(se_alpha, se_beta, random_state=rng); sp_m = beta.rvs(sp_alpha, sp_beta, random_state=rng)
            else:
                se_m, sp_m = se, sp
            p_true = rogan_gladen(obs_prev, se_m, sp_m)
            pz = [p_z1_given_serology(int(s), p_true, se_m, sp_m) for s in g['serology_pos'].tolist()]
            z_imp = (rng.random(len(pz)) < np.array(pz)).astype(int)
            X = np.column_stack([g['vaccinated'].values, g['age'].values, g['sex'].values, z_imp])
            y = g['case'].values.astype(int)
            clf = LogisticRegression(penalty='l2', solver='lbfgs', max_iter=200)
            clf.fit(X, y)
            log_or_draws.append(float(clf.coef_[0][0]))
        mean_log_or = float(np.mean(log_or_draws)); pooled_or = float(np.exp(mean_log_or)); ve = 1.0 - pooled_or
        out_rows.append({'stratum': key if by else 'overall','serology_informed_or': pooled_or,'serology_informed_ve': ve,
                         'se': se,'sp': sp,'n_imputations': n_imputations,'sample_se_sp': sample_se_sp})
    return pd.DataFrame(out_rows)
