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
                            (default setting is 50)\ :sup:'1'
-w WINDOW_SIZE              Short form of window-size WINDOW_SIZE
--strand {+,-,=,+-=}        Transcribed strand (+), non-transcribed (-), any (=),
                            or all (+-= default)
-s {+,-,=,+-=}              Short form of --strand {+,-,=,+-=}
==========================  =============================================================  ============================


-----------
4. Examples
-----------
*4.1. Search for the presence of mutational motifs in sample1.maf using genome hg19 in any strand*
-------
4.1.1.Command
-------

``$ mutagene motif search -i sample1.maf -g hg19 -s "="``

---------------
4.1.2.Motif Output
---------------

============================  ===========  ======  ======  =================  ======================  ===========  ============
sample                        name         motif   strand  enrichment         pvalue                  mut_low_est  mut_high_est   
============================  ===========  ======  ======  =================  ======================  ===========  ============
TCGA-50-6593-01A-11D-1753-08  C>T in CpG   [C>T]G  '='     4.586718025481874  1.0181609110804669e-06  15           18.0
============================  ===========  ======  ======  =================  ======================  ===========  ============ 



