===============================================================
Motif: Search for the presence of mutational motifs in samples
===============================================================

==============
1. Description
==============

------------------
1.1. Functionaility
------------------

Use "mutagene motif" to search for the presence of mutational motifs in mutational data.

--------------------
1.2. Motif Definition
--------------------

A motif is defined as a characteristic pattern of DNA mutation and its local DNA context. It is often associated with a specific carcinogen or a biological process.

------------------------
1.3. Motif Representation
------------------------

MutaGene represents motifs as a string of characters, where characters in brackets represent the single-base substitutions and characters outside brackets represent the unmutated DNA context. The motif must be in quotes to be recognized by MutaGene.

-------------------
1.4. Motif Examples
-------------------

"A[C>A]G" represents the DNA sequence "ACG" mutated into the DNA sequence "AAG"

"C[G>T]" represents the DNA sequence "CG" mutated into the DNA sequence "CT"

"[C>A]C" represents the DNA sequence "CC" mutated into the DNA sequence "AC"

------------------------------
1.5. Further Reading on Motifs
------------------------------

The publication `Mutational signatures and mutable motifs in cancer genomes <https://doi.org/10.1093/bib/bbx049>` describes motifs and their uses.

*Note: if you installed MutaGene in a virtual environment, make sure you activate the virtual environment first.*

-------------------
2. Motif command
-------------------

To use the motif command, type 

``$mutagene motif <action (search or list)>``

If search is specified, infile and genome are also required:

``$ mutagene motif search [arguments]``

You can always find help on the required arguments using the following command:

``$ mutagene motif search -h``
or
``$mutagene motif list -h``

------------
3. Arguments
------------

**3.1.Command:** ``$mutagene motif <action (search or list)>``

followed by the required arguments from the command line. 

**3.2.Required Arguments (must be specified):**

Motif function requires:
``$mutagene motif <action (search or list)>``
If search is specified, infile and genome are also required

=========================   ============================================================  ====================
Argument                    Description                                                   Example
=========================   ============================================================  ====================
--infile INFILE             Input file in MAF or VCF format with 1 or multiple samples     --infile sample1.maf
                            (where INFILE is the sample filename with extension)
-i INFILE                   Short form of --infile INFILE argument                         -i sample1.maf 
--genome GENOME             Location of genome assembly file in 2bit format                --genome hg38.2bit   
                            (where GENOME is the filename)                    
-g GENOME                   Short form of --genome GENOME argument                         -g hg38.2bit                      
=========================   ============================================================  ====================                                                                                                                                          


**3.3.Optional Arguments (can be specified):**

==========================  =============================================================  ============================
Argument                    Description                                                    Example
==========================  =============================================================  ============================
--outfile [OUTFILE]         Name of output file, will be generated in TSV format            --outfile ../../out/out.tsv
                            (if this argument is not included output is to screen)
-o [OUTFILE]                Short form of --outfile [OUTFILE] argument                      -o ../../out/out.tsv
--motif MOTIF               Motif to search for, use the 'R[C>T]GY syntax for the
                            motif. Use quotes
-m MOTIF                    Short form of --motif MOTIF
window-size WINDOW_SIZE     Context window size for motif search
                            (default setting is 50)\ :sup:`a`
-w WINDOW_SIZE              Short form of window-size WINDOW_SIZE
--strand {+,-,=,+-=}        Transcribed strand (+), non-transcribed (-), any (=),
                            or all (+-= default)\ :sup:`b`
-s {+,-,=,+-=}              Short form of --strand {+,-,=,+-=}
==========================  =============================================================  ============================

a. Window Size Parameter Explanation: MutaGene counts window size as the number of DNA bases searched for from the first base of the DNA sequence gathered up to but not including the mutated base. Therefore, the effective length of the DNA sequence searched is 2 * window-size + 1. It may be advantageous to use a window size longer than the default 50 bases if the motif is longer than three nucleotides,
as this motif is likely to appear less frequently in the DNA context. Similarly, if the motif is shorter than three nucleotides,
it may be advantageous to use a window size shorter than the default 50 bases, as the motif is likely to appear in DNA more frequently.
b. Strand Parameter Explanation: MutaGene can search for the presence of a motif on the transcribed or non-transcribed DNA strands or both strands. This information is gathered from the input file provided by the user. Analyzing for the presence on a transcribed or non-transcribed strand is advantageous when a mutational process is known to have mutations with a transcriptional strand bias. For instance, the APOBEC1/3A/B family is known to be associated with mutational processes that have a transcriptional strand bias of mutations in exons. The transcription strand refers to the coding DNA strand, and the non-transcription strand refers to the template DNA strand.

---------------------------------
4. Interpretation of Motif Output
---------------------------------
If no motifs are significantly present in the data, the output will say: "WARNING No significant motif matches found".

If the presence of a motif is significant in the data, the output will show a table with the following headers:

=============  =======================================================================================================================
Header         Description
=============  =======================================================================================================================
Sample         Name of Sample. If input file contains multiple samples, output will be stratified per sample.
Name           Name of motif. If -m/--motif argument is given, name will be "Custom motif".
Motif          Motif searched for in data
Strand         DNA Strand that motif was searched for on. '+': transcribed strand, '-': non-transcribed strand, "=": any strand, "+-=":                all strands.
Enrichment     Quantitative measure of motif's prevalence, significant if greater than one.\ :sup:`a`
mut_low_est    Conservative estimate for number of mutations (of total number in input file) that match motif
mut_high_est   Maximum number of mutations (of total number in input file) that match the motif
pvalue         Fisher's p-value for motif significance
qvalue         Fisher's p-value with Benjamini-Hochberg correction for motif significance
=============  =======================================================================================================================

a. How to Interpret Enrichment Output: Enrichment is modeled off of a risk ratio, meaning that a motif’s enrichment is essentially a ratio between the probability of a motif appearing in a cancer sample’s DNA mutations and the probability of a motif appearing in a
cancer sample’s DNA context. Because enrichment is modeled off a risk ratio, it can be interpreted the same way. The result of enrichment minus one is the percent overrepresentation of a motif. For example, if enrichment is 1.5, it means that there is a 50%
overrepresentation of the mutated motif (as compared to what is likely by chance). For this reason, enrichment is considered significant if it is greater than one. Motifs with enrichments <= 1 are not reported by MutaGene.

-----------
5. Examples
-----------
*5.1. Search for the presence of mutational motifs in sample1.maf using genome hg19 in any strand*
-------
5.1.1.Command
-------

``$ mutagene motif search -i sample1.maf -g hg19 -s "="``

------------------
5.1.2.Motif Output
------------------

============================  ===========  ======  ======  =================  ======================  ===========  ============
sample                        name         motif   strand  enrichment         pvalue                  mut_low_est  mut_high_est   
============================  ===========  ======  ======  =================  ======================  ===========  ============
TCGA-50-6593-01A-11D-1753-08  C>T in CpG   [C>T]G  '='     4.586718025481874  1.0181609110804669e-06  15           18.0
============================  ===========  ======  ======  =================  ======================  ===========  ============ 



