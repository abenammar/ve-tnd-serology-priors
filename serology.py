import numpy as np
def rogan_gladen(observed_prev, se, sp):
    denom = se + sp - 1.0
    if denom == 0:
        return float(min(max(observed_prev, 0.0), 1.0))
    p = (observed_prev + sp - 1.0) / denom
    return float(min(max(p, 0.0), 1.0))
def p_z1_given_serology(serology_pos, p_z1, se, sp):
    p = p_z1; s = serology_pos
    if s == 1:
        num = se * p; den = se*p + (1-sp)*(1-p)
        return float(num/den) if den>0 else p
    else:
        num = (1-se) * p; den = (1-se)*p + sp*(1-p)
        return float(num/den) if den>0 else p
