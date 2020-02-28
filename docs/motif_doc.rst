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
                            (default setting is 50
-w WINDOW_SIZE              Short form of window-size WINDOW_SIZE
--strand {+,-,=,+-=}        Transcribed strand (+), non-transcribed (-), any (=),
                            or all (+-= default)
-s {+,-,=,+-=}              Short form of --strand {+,-,=,+-=}
==========================  =============================================================  ============================


-----------
4. Examples
-----------
*4.1. Search for the presence of MutaGene-10 signatures in PD3851a.vcf using hg38 and default method mlez (method mle gives same output for this input)*
-------
4.1.1.Command
-------

``$ mutagene signature identify -i PD3851a.vcf -g hg38.2bit -f VCF -s10``

---------------
4.1.2.Identify Output
---------------

=======  ============  ============  =========== 
sample     signature     exposure    mutations   
=======  ============  ============  =========== 
VCF        2             0.0935      80
VCF        3             0.0392      33
VCF        4             0.0074      6
VCF        5             0.0728      62
VCF        6             0.1362      116
VCF        7             0.0118      10
VCF        8             0.0552      47
VCF        9             0.0271      23
VCF        10            0.0121      10
=======  ============  ============  =========== 



