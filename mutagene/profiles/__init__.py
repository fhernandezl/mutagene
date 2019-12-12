import numpy as np
from mutagene.io.profile import plot_profile, read_signatures
from mutagene.io.mutations_profile import read_auto_profile
from mutagene.io.context_window import read_MAF_with_context_window
from mutagene.profiles.profile import get_mutational_profile, get_multisample_mutational_profile

class Profile:
    def __init__(self, profile):
        self.profile = profile

    def plot_profile(self):
        plot_profile(self.profile)

class Sample(Profile):
    def __init__(self, infile, genome):
        """
        Arguments:
        `infile`: path to vcf file
        `genome`: path to reference genome
        """
        assert infile.endswith(('vcf','VCF')), "File must be VCF, for multisample files like MAF use the `multisample` method"
        self.infile = open(infile)
        self.genome = genome
        mutations, self.processing_stats = read_auto_profile(self.infile, fmt='VCF', asm=self.genome)
        profile = get_mutational_profile(mutations, counts=True)
        super().__init__(profile)

    @staticmethod
    def multisample(infile, genome):
        """
        Arguments:
        `infile`: path to maf file
        `genome`: path to reference genome
        """
        mutations, mutations_with_context, processing_stats = read_MAF_with_context_window(open(infile), genome, window_size=1)
        profile = get_multisample_mutational_profile(mutations, counts=True)
        samples = []
        for name, profile in profile.items():
            _cls = Profile(profile)
            setattr(_cls, 'name', name)
            setattr(_cls, 'infile', open(infile))
            setattr(_cls, 'genome', genome)
            setattr(_cls, 'mutations_with_context', mutations_with_context)
            setattr(_cls, 'processing_stats', processing_stats)
            samples.append(_cls)
        return samples

class SyntheticSample(Profile):
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
        self.info = info
        super().__init__(v)