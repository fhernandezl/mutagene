from collections import defaultdict
import numpy as np
from scipy import stats

def get_bootstrap_decomposition(bootstrap_results, sig_names):
    exposures_lists = defaultdict(list)
    mutations_lists = defaultdict(list)
    for result in bootstrap_results:
        for x in result:
            exposures_lists[x['name']].append(x['score'])
            mutations_lists[x['name']].append(x['mutations'])

    h = np.array([np.nanmean(exposures_lists[name]) for name in sig_names])
    m = np.array([np.nanmean(mutations_lists[name]) for name in sig_names])  # , np.int)

    h_sem = np.array([stats.sem(exposures_lists[name]) for name in sig_names])
    m_sem = np.array([stats.sem(mutations_lists[name]) for name in sig_names])

    _decomp = []
    for i in range(h.shape[0]):
        h_ci_low = h[i] - 1.96 * h_sem[i]
        h_ci_hi = h[i] + 1.96 * h_sem[i]
        m_ci_low = m[i] - 1.96 * m_sem[i]
        m_ci_hi = m[i] + 1.96 * m_sem[i]

        if m_ci_low < 1.0:
            continue

        _decomp.append({
            'name': sig_names[i],
            'score': h[i],
            'score_CI_low': h_ci_low,
            'score_CI_high': h_ci_hi,
            'mutations': m[i],
            'mutations_CI_low': m_ci_low,
            'mutations_CI_high': m_ci_hi
        })

    return _decomp