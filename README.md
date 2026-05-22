# get_ENCODE_metadata
From Experiment Search on encodeproject.org, get FASTQ file and biosample metadata.

Parse JSON of each experiment accession for the following metadata:
- Donor accession
- Donor sex
- Donor age
- Donor ethnicity/ethnicities
- File accession
- FASTQ read count
- FASTQ md5sum
- FASTQ read length
- Run type

To run this script, download experiment report. From https://www.encodeproject.org/report/?type=Experiment, choose your filters and click "Download TSV".

The output TSV has one column per metadata above.

Example:

```
tsv_file = "experiment_report_2026_5_15_18h_20m.tsv"

from getENCODEMetadata import *

accessions = get_experiment_ids(tsv_file)
print(f"Found {len(accessions)} experiments")
output_file = "encode_metadata.tsv"

for exp_acc in accessions:
    rows = get_exp(exp_acc, "fastq") # file type is FASTQ
    append_to_tsv(rows, output_file)
    print(f"Processed {exp_acc}")
```
