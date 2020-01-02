# Pipeline for the analysis of the frequencies of anaerobic bacteria in two hospital centers

This pipeline was designed to analyse the frequencies of bacteriamia involving anaerobic bacteria in two different hospital centers. It is a simple pipeline not meant to be re-use, but that needs to be published so it could be reviewed.

## Python requirements

Python 3.6 was used for this project
the following modules are needed to run the pipeline:
- csv
- sys
- pickle
- datetime
- statistics
- numpy
- scipy

## How to use this pipeline
Each script of the pipeline must be used in the correct order. Here I explain the use of every script.

- create_dataset.py: creates the basic dataset from different databases (One file containing all the blood culture results, and two files of antimicrobial sensitivity typing results (AST), one for each hospital center), after some cleaning of the database. The output file is dataset.pickle, a datastructure containning the different results needed for the rest of the analysis.
- bacteria.py: extract the different species found in the dataset, in a table with one column, bacteria.csv. This file is then manually curated into bacteria_def.csv, adding a number used further in the pipeline, to eliminate contaminants from the data:
- 0 are not bacteria and will be discard in the analysis
- 1 are aerobic bacteria that are not frequent contaminant, therefore a single blood culture is enough to assert a bacteriemia
- 2 are aerobic bacteria that can be contaminant, so AST is performed on two different BC to assert whether it is a true bacteriemia
- 3 are anaerobic bacteria that are not frequent contaminant, therefore a single blood culture is enough to assert a bacteriemia
- 4 are anaerobic bacteria that can be contaminant, so multiple BC are needed to assert a bacteriemia
- extract_bacteriemia.py: using dataset.pickle and bacteria_def.csv, associate positive blood culture into monobacterial episodes of bacteriemia, then checks if the conditions are met to assert a true episodes of bacteriemia. BC in an episode must not be separated from more than 5 days, or the pipeline creates two different episodes. The output files are true_bacteriemia.pickle, and false_bacteriemia.pickle. The second one won't be used afterward.
- organise_bacte.py: using true_bacteriemia.pickle, associates each monobacterial episode of bacteriemia into episodes of multibacterial bacteriemia, if possible, using overlapping dates of first and last isolement of bacteria. The output file is bacteriemia.pickle.
- analyse_bacte.py: performs various analysis on bacteriemia.pickle.
- extract_ast.py: extract AST results of anaerobic bacteria found in true_bacteriemia.pickle from the files of AST results, and output the results in atb_ana.csv.
- extract_mic.py: idem, but extract minimimal inhibitory concentrations (MIC), and output the results in mic_ana.csv, mic_per_sp.csv and mic_per_gen.csv
- analyse_ast.py: analyse the results of AST by diffusion, from atb_ana.csv. The output files are ast_per_sp.csv and ast_per_gen.csv.
