
from mutagene.profiles.profile import generate_resampled_profiles
from mutagene.signatures.identify import decompose_mutational_profile_counts, IDENTIFY_MIN_FUNCTIONS
from mutagene.signatures.functions import get_bootstrap_decomposition
from mutagene.io.decomposition import write_decomposition, write_bootstrap_decomposition
from mutagene.io.profile import read_signatures
from mutagene.profiles import SyntheticSample
import sys

class Identify:
    extra = []

    def __init__(self, profile, sig_set, method='MLEZ', others_threshold=0, bootstrap=True, dummy_sigs=True, global_optimization=None):
        """
        Arguments:
        `profile`: Profile to decompose. Must have length 96.
        `sig_set`: signature set to use for the decomposition.
        `method`: solver method.
        `others_threshold`: minimum threshold for acceptable results.
        `bootstrap`: Use the bootstrap to calculate confidence intervals. 
        `dummy_sigs`: Account for unexplained variance (non-context dependent mutational processes and unknown signatures)
        `debug`: run the decomposition in debug mode.
        """
        assert len(profile)==96, "Invalid sample. Must be vector of length 96"
        assert sig_set in [5,10,30,49], "Invalid sig_set choice. Must be 5,10,30 or 49"
        assert method.lower() in IDENTIFY_MIN_FUNCTIONS, "Unknown method provided"

        self.profile = profile
        self.sig_set = sig_set
        self.method = method
        self.bootstrap = bootstrap
        self.enable_dummy = dummy_sigs
        self.global_optimization = global_optimization
        self.others_threshold = others_threshold
        self.W_and_labels = read_signatures(self.sig_set)
        self._main()

    @classmethod
    def synthetic(cls, synthetic_sample, sig_set=None, method='MLEZ', others_threshold=0, bootstrap=True, dummy_sigs=True, global_optimization=None, debug=False):
        assert type(synthetic_sample) == SyntheticSample, "Invalid sample. Must be of type SyntheticSample"
        if not sig_set:
            sig_set = synthetic_sample.ref_sig

        identify = cls(synthetic_sample.profile, sig_set, method, others_threshold, bootstrap, dummy_sigs, global_optimization, debug)
        setattr(identify, 'comparison', [])
        setattr(identify, 'total_error', 0)

        for index, sig in enumerate(synthetic_sample.info['sig']['used']):
            sig_res = list(filter(lambda item: item['name']==sig, identify.decomposition))
            found = 'Yes' if sig_res else 'No'
            real_score = synthetic_sample.info['h'][index]
            calc_score = sig_res[0]['score'] if sig_res else 0
            diff = abs(real_score - calc_score)
            identify.total_error += diff
            identify.comparison.append({
                'sig': sig,
                'found': found,
                'real_score': real_score,
                'calc_score': calc_score,
                'error': diff
            })

        return identify

    def _decompose(self, sample):
        h, summary, results = decompose_mutational_profile_counts(
            sample,
            self.W_and_labels,
            self.method,
            self.others_threshold,
            self.global_optimization,
            self.enable_dummy)
        self.extra.append({
            'h': h,
            'summary': summary,
            'results': results
        })
        res = list(filter(lambda r: r['mutations'] != '', results))
        res = sorted(res, key=lambda r: r['score'], reverse=True)
        return res

    def _main(self):
        if self.bootstrap:
            self.bootstrap_results = []
            for resampled_profile in generate_resampled_profiles(self.profile, 100):
                self.bootstrap_results.append(self._decompose(resampled_profile))
            self.decomposition = get_bootstrap_decomposition(self.bootstrap_results, self.W_and_labels[1])
        else:
            self.decomposition = self._decompose(self.profile)

    def write_results(self, to=sys.stdout):
        if self.bootstrap:
            write_bootstrap_decomposition(to, self.bootstrap_results, self.W_and_labels[1], 'VCF')
        else:
            write_decomposition(to, self.decomposition, self.W_and_labels[1], 'VCF')