#
import numpy as np

# from .io import read_profile
# from .io import format_profile
from mutagene.signatures.identify import decompose_mutational_profile_counts
from mutagene.io.profile import read_signatures, plot_profile
from pprint import pprint

def convert_to_list(name_to_idx, d):
    v = [0] * N
    for value in d:
        idx = name_to_idx.get(value['name'])
        if idx is None:
            # print(value['name'], 'not found in name_to_idx')
            continue
        v[idx] = value['score']
    return v


def get_scores(d):
    ll = 0
    frob = 0
    frob0 = 0
    js = 0
    kl = 0
    for value in d:
        if value['name'] == 'LogLik':
            ll = value['score']
        if value['name'] == 'Frobenius':
            frob = value['score']
        if value['name'] == 'FrobeniusZero':
            frob0 = value['score']
        if value['name'] == 'DivergenceJS':
            js = value['score']
        if value['name'] == 'DivergenceKL':
            kl = value['score']
    return ll, frob, frob0, js, kl


def benchmark_simulated(results_fname, signature_names, W):
    name_to_idx = {}
    for i, s in enumerate(signature_names):
        name_to_idx[s] = i

    W = np.array(W).T
    print(W.shape)
    N = W.shape[1]

    signature_names = list(name_to_idx.keys())
    signature_ids = [str(name.split()[1]) for name in signature_names]

    np.set_printoptions(precision=4)

    with open(results_fname, 'w') as report:
        report.write("TEST\tMUTATIONS\tMETH\tROUND\tSIGNATURE\tVALUE\tSE_E\tMSE_M\tMSE_E\tLL\tFROB\tFROB0\tJS\tKL\n")
        # for j in range(N):
        #     report.write("S{}\t".format(j + 1))
        # report.write("MSE\n")

        for i in range(N):

            for N_mutations in [10, 50, 100, 500, 1000, 10000]:

                for iteration in range(10):
                    h0 = np.zeros(N)
                    h0[i] = int(0.8 * N_mutations)
                    for j in range(N):
                        if i == j:
                            continue

                    # 20% uniform noise
                    # for k in range(int(0.2 * N_mutations)):
                    #     h0[random.randrange(N)] += 1
                    h0 += np.random.multinomial(int(0.2 * N_mutations), [1.0 / N] * N)  # uniform distribution
                    h0_counts = h0.copy()

                    h0 /= h0.sum()
                    v0 = W.dot(h0)
                    v0_counts = np.random.multinomial(N_mutations, v0 / v0.sum())  # np.ceil(v0 * N_mutations)

                    # oname = prefix + "profile"
                    # # print("ONAME:", oname)
                    # with open(oname, 'w') as o:
                    #     query_formatted = format_profile(h0.tolist())
                    #     o.write(query_formatted)

                    # oname = prefix + "counts"
                    # with open(oname, 'w') as o:
                    #     query_formatted = format_profile(h0.tolist(), counts=True)
                    #     o.write(query_formatted)

                    THRESHOLD = 0.0
                    # print(h0_counts)
                    # print(v0_counts)
                    _, _, exposure = decompose_mutational_profile_counts(v0_counts, W, 'MLE', debug=False, others_threshold=THRESHOLD)

                    h1 = np.array(convert_to_list(name_to_idx, exposure))
                    # h1 += min(1.0 - h1.sum(), 0)
                    h1_counts = np.random.multinomial(N_mutations, h1 / h1.sum())
                    ll, frob, frob0, js, kl = get_scores(exposure)

                    # print(np.round(h0, 3))
                    # print(np.round(h1, 3))
                    v1 = W.dot(h1)

                    # convert exposure to mutational burden
                    # v1_counts = np.ceil(v1 * N_mutations)

                    # convert exposure to mutational burden
                    v1_counts = np.random.multinomial(N_mutations, v1 / v1.sum())

                    MSE_M = np.mean((v0_counts - v1_counts)**2)
                    MSE_E = np.mean((h0 - h1)**2)

                    for j in range(N):
                        report.write("{}_{}_{}\t{}\t{}\t{}\t".format(signature_ids[i], 80, 20, N_mutations, "MLE", iteration + 1))
                        report.write("{}\t{}\t".format(signature_names[j], int(h1_counts[j])))
                        SE_E = (h0[j] - h1[j])**2
                        report.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(SE_E, MSE_M, MSE_E, ll, frob, frob0, js, kl))

                    print(signature_ids[i], N_mutations, iteration, round(MSE_M, 4), round(MSE_E, 4), round(ll, 4), round(frob, 4), round(frob0, 4), round(js, 4), round(kl, 4))


def benchmark_2combinations(results_fname, signature_names, W):
    name_to_idx = {}
    for i, s in enumerate(signature_names):
        name_to_idx[s] = i

    W = np.array(W).T
    N = W.shape[1]

    signature_names = list(name_to_idx.keys())
    signature_ids = [str(name.split()[1]) for name in signature_names]

    np.set_printoptions(precision=4)

    noise_level = 0.05
    ratio = 0.7
    n_sample = 20

    with open(results_fname, 'w') as report:
        report.write("ratio\tn_sample\tnoise_level\tsignatures\tSIGNATURE\tVALUE\tSE_E\tMSE_M\tMSE_E\tLL\tFROB\tFROB0\tJS\tKL\n")
        # for j in range(N):
        #     report.write("S{}\t".format(j + 1))
        # report.write("MSE\n")

        for i in range(N):

            for N_mutations in [10, 50, 100, 500, 1000, 10000]:

                for iteration in range(10):
                    h0 = np.zeros(N)
                    h0[i] = int(0.8 * N_mutations)
                    for j in range(N):
                        if i == j:
                            continue

                    # 20% uniform noise
                    # for k in range(int(0.2 * N_mutations)):
                    #     h0[random.randrange(N)] += 1
                    h0 += np.random.multinomial(int(0.2 * N_mutations), [1.0 / N] * N)  # uniform distribution
                    h0_counts = h0.copy()

                    h0 /= h0.sum()
                    v0 = W.dot(h0)
                    v0_counts = np.random.multinomial(N_mutations, v0 / v0.sum())  # np.ceil(v0 * N_mutations)

                    THRESHOLD = 0.0
                    # print(h0_counts)
                    # print(v0_counts)
                    _, _, exposure = decompose_mutational_profile_counts(v0_counts, W, 'MLE', debug=False, others_threshold=THRESHOLD)

                    h1 = np.array(convert_to_list(name_to_idx, exposure))
                    # h1 += min(1.0 - h1.sum(), 0)
                    h1_counts = np.random.multinomial(N_mutations, h1 / h1.sum())
                    ll, frob, frob0, js, kl = get_scores(exposure)

                    # print(np.round(h0, 3))
                    # print(np.round(h1, 3))
                    v1 = W.dot(h1)

                    # convert exposure to mutational burden
                    # v1_counts = np.ceil(v1 * N_mutations)

                    # convert exposure to mutational burden
                    v1_counts = np.random.multinomial(N_mutations, v1 / v1.sum())

                    MSE_M = np.mean((v0_counts - v1_counts)**2)
                    MSE_E = np.mean((h0 - h1)**2)

                    for j in range(N):
                        report.write("{}_{}_{}\t{}\t{}\t{}\t".format(signature_ids[i], 80, 20, N_mutations, "MLE", iteration + 1))
                        report.write("{}\t{}\t".format(signature_names[j], int(h1_counts[j])))
                        SE_E = (h0[j] - h1[j])**2
                        report.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(SE_E, MSE_M, MSE_E, ll, frob, frob0, js, kl))

                    print(signature_ids[i], N_mutations, iteration, round(MSE_M, 4), round(MSE_E, 4), round(ll, 4), round(frob, 4), round(frob0, 4), round(js, 4), round(kl, 4))

class SyntheticSample():
    def __init__(self, ref_sig, N_mut=1000, complexity=5, noise=10, _gen=True):
        """
        Returns a synthetic sample object.

        Arguments:
        `ref_sig`: signatures used to generate the sample. Can be 5,10,30 or 49.
        `N_mut`: total number of mutations desired. The final result will differ. Must be `int`.
        `complexity`: how many of the `ref_sig` to use for the sample. Must be `int < len(ref_sig)`.
        `noise`: max number of mutations to add or subtract randomly to sample.
        """
        assert type(N_mut)==int and N_mut>0, "N_mut must be an integer above 0"
        assert ref_sig in [5,10,30,49], "Invalid ref_sig choice. Must be 5,10,30 or 49"
        assert type(complexity)==int and complexity>1 and complexity<ref_sig, "Invalid complexity value. Must be int above 0 and less than ref_sig"
        assert type(noise)==int and noise>=0, "noise must be a positive integer"

        self.noise = noise
        self.complexity = complexity
        self.N_mut = N_mut
        self.ref_sig = ref_sig
        if _gen:
            self._gen()

    @classmethod
    def gen_from(cls, ref_sig, sig_names=[], h=[], N_mut=1000, noise=10):
        """
        Returns a synthetic sample object.

        Arguments:
        `ref_sig`: signatures used to generate the sample. Can be 5,10,30 or 49.
        `sig_names`: which signatures from `ref_sig` to use for the sample.
        `h`: contributions of each signature. Must add up to 1.
        `N_mut`: total number of mutations desired. The final result will differ. Must be `int`.
        `noise`: max number of mutations to add or subtract randomly to sample.
        """
        new_cls = cls(ref_sig, N_mut, len(sig_names), noise, _gen=False)
        new_cls._predef(sig_names, h)
        return new_cls
    
    def _predef(self, sig_names=[], h=[]):
        assert sig_names, "No signatures provided"
        assert h, "No h provided"
        assert sum(h) == 1, "h must add up to 1"
        assert len(sig_names) == len(h), "Dimensions of sig_names and h don't match"

        self.predef_sig_names = sig_names
        self.predef_h = h
        self._gen()

    def _gen(self):
        W_og, signature_names = read_signatures(self.ref_sig)
        self.ref_w_labels = (W_og, signature_names)
        sig_dict = list( map(lambda w,name: {'w':w, 'name':name}, W_og.T, signature_names) )
        if 'predef_sig_names' in dir(self):
            sig_names = self.predef_sig_names
            sample_sigs = list(filter(lambda item: item['name'] in sig_names, sig_dict))
            assert len(sample_sigs)==len(sig_names), "sig_names provided were not found"
            h = self.predef_h
        else:
            sample_sigs = np.random.choice(sig_dict, self.complexity, replace=False) # synthetic sample sigs
            sig_names = [sig["name"] for sig in sample_sigs]
            h = np.random.rand(self.complexity) # init exposure
            h = h/h.sum() # normalize exposures
        W = np.array([sig["w"] for sig in sample_sigs]).T # sample specific W
        v = W.dot(h) # calculate mutational profile
        v = np.rint( v*(self.N_mut/v.sum()) ) # make v the desired number of mutations
        v_noise = np.random.random_integers(-self.noise, self.noise, 96) # generate noise
        v += v_noise # add noise to v
        v[v < 0] = 0 # make any negative counts 0
        info = {
            'sig': {
                'group': self.ref_sig,
                'used': sig_names
            },
            'W': W,
            'h': h,
            'noise': v_noise,
            'total_mut': v.sum()
        }
        self.v, self.info = v, info

    def decompose(self, method='MLEZ', debug=False, others_threshold=0):
        h, summary, results = decompose_mutational_profile_counts(self.v, self.ref_w_labels, method, debug, others_threshold)
        res = filter(lambda item: item['mutations'] != '', results)
        res = filter(lambda item: item['mutations']>0, res)
        self.decomposition = sorted(res, key=lambda item: item['score'], reverse=True)
        self._decomp = {
            'h': h,
            'summary': summary,
            'results': results}
        self.comparison = []
        self.total_error = 0
        for index, sig in enumerate(self.info['sig']['used']):
            sig_res = list(filter(lambda item: item['name']==sig, self.decomposition))
            found = 'Yes' if sig_res else 'No'
            real_score = self.info['h'][index]
            calc_score = sig_res[0]['score'] if sig_res else 0
            diff = abs(real_score - calc_score)
            self.total_error += diff
            self.comparison.append({
                'sig': sig,
                'found': found,
                'real_score': real_score,
                'calc_score': calc_score,
                'error': diff
            })
    
    def plot_v(self):
        plot_profile(self.v)

    def print_results(self, decomposition=True, comparison=True, sep='\t'):
        if decomposition:
            print("DECOMPOSITION")
            print('signature','score','mutations',sep=sep)
            for res in self.decomposition:
                print(res['name'],res['score'],res['mutations'],sep=sep)
        if comparison:
            print("REAL COMPOSITION")
            print('signature','found in decomposition','real score','calc score','error',sep=sep)
            for comp in self.comparison:
                print(comp['sig'],comp['found'],comp['real_score'],comp['calc_score'],comp['error'],sep=sep)
        print('TOTAL ERROR',self.total_error,sep='\n')

    def export_results(self, fname='results.out', fextra=None):
        pprint({
            'decomposition': self.decomposition,
            'comparison': self.comparison
        }, stream=open(fname,'w'))
        if fextra:
            pprint({
                'synthetic_sample': {
                    'v': self.v,
                    'info': self.info
                },
                'decomposition': self._decomp,
                'comparison': self.comparison
            }, stream=open(fextra,'w'))