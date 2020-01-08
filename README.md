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
- secrets

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

## Format of the input data
"BC_data" was extracted from the DxLab software, iso-8859-1 file with ";" as separator, with the following columns:
- sampling date (format: DD/MM/YYYY HH:MM:SS)
- family name (not used in the pipeline)
- First name (not used in the pipeline)
- birth name (not used in the pipeline)
- unique number of the patient (IPP)
- unique number of the stay (not used in the pipeline)
- birth date (format DD/MM/YYYY)
- sex (M/F)
- unique number of the sample (format 99YYDDDXXXX, where YY is the 2 last digits of the year, DDD the day number in the year, and XXXX an incremented unique number)
- ward
- site of the sample (for exemple, direct venopuncture)
- for each identification in the BC:
  - a column with the identification
  - an empty column (unit)
- then for each identification:
  - a column with the germ number in the BC (format "Identification N° : X" with X being this number)
  - an empty column (unit)

"SIR_AST_results_ICM", "SIR_AST_results_CHU", and "SIR_AST_results", files extracted by the SIRweb software, iso-8859-1 files with ";" as separator, with the following columns:
- Family name (not used in the pipeline)
- First name (not used in the pipeline)
- IPP
- stay number (not used in the pipeline)
- birth date (not used in the pipeline)
- unique number of the sample (format NNNNYDDDXXXX, where NNNN are useless digits, Y the last digit of the year, DDD and XXXX the same as in the first file) 
- germ number
- identification (the same as in the first file)
- a boolean (OUI or NON): is a same AST was found by the system for the same identification for this patient in the 30 days in BC)
- SIR results (S, I or R)
  - 2 columns for penicillin
  - 2 columns for cefotaxim
  - ampicillin
  - cotrimoxazole
  - ciprofloxacine
  - nalidixic acid
  - amoxicillin ac. clavulanic
  - piperacillin tazobactam
  - imipenem
  - metronidazole
  - 3 columns for clindamycin
  - 2 columns for cefoxitin
  - erythromycin
  - 2 columns for rifampicin
  - 2 colums for amoxicilin
  - piperacillin
  - tetracylin
  - vancomycin
  - moxifloxacin
  - tigecyclin

"MIC_AST_results", a file extracted by the SIRweb software, iso-8859-1 file with ";" as separator and "," as decimal separator, with the following columns:
- Family name (not used in the pipeline)
- First name (not used in the pipeline)
- IPP
- stay number (not used in the pipeline)
- birth date (not used in the pipeline)
- unique number of the sample (format NNNNYDDDXXXX, where NNNN are useless digits, Y the last digit of the year, DDD and XXXX the same as in the first file) 
- germ number
- identification (the same as in the first file)
- a boolean (OUI or NON): is a same AST was found by the system for the same identification for this patient in the 30 days in BC)
- MIC results:
  - amoxicillin ac. clavulanic
  - piperacillin tazobactam
  - imipenem
  - metronidazole
  - 2 columns for clindamycin
  - 2 columns for cefoxitin
  - erythromycin
  - 2 columns for rifampicin
  - moxifloxacin
  - tigecylin
  - a gibberish column named "VALCMIFINA_ATB277"
  
Headers of these files are provided in the folder "headers".
