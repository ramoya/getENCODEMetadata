#!/usr/bin/env python3

import os
import csv
import requests

url="https://www.encodeproject.org/{}/?format=json"
headers={"accept":"application/json"}

def get_experiment_ids(tsv_file):

    experiment_ids = []

    with open(tsv_file, "r") as f:

        # skip first metadata line
        next(f)

        # read header
        header = next(f).strip().split("\t")

        accession_idx = header.index("Accession")

        for line in f:
            if not line.strip():
                continue

            cols = line.strip().split("\t")

            accession = cols[accession_idx]

            experiment_ids.append(accession)

    return experiment_ids

def flatten_json(obj):
    values = []

    if isinstance(obj, dict):
        for v in obj.values():
            values.extend(flatten_json(v))

    elif isinstance(obj, list):
        for item in obj:
            values.extend(flatten_json(item))

    else:
        # leaf node
        if obj is not None:
            values.append(str(obj))

    return values


def json_to_csv_string(obj):
    return ",".join(flatten_json(obj))

def get(resource):
    return requests.get(
        url.format(resource),
        headers=headers
    ).json()


def extract_experiment_metadata(replicate_obj):
    library = replicate_obj.get("library", {})
    biosample = library.get("biosample", {})
    donor = biosample.get("donor", {})

    return {
        "accession_donor": donor.get("accession"),
        "sex": donor.get("sex"),
        "age": donor.get("age"),
        "ethnicity": json_to_csv_string(donor.get("ethnicity"))
    }

def extract_file_metadata(file_obj):
    
    return {

        "accession": file_obj.get("accession"),
        "read_count": file_obj.get("read_count"),
        "md5sum": file_obj.get("md5sum"),
        "read_length": file_obj.get("read_length"),
        "run_type": file_obj.get("run_type"),
    }


def get_exp(exp_acc, file_type):

    response = get(os.path.join("experiments", exp_acc))

    rows = []

    for replicate_obj in response["replicates"]:
        x = extract_experiment_metadata(replicate_obj)

    for file_obj in response["files"]:
        if file_obj.get("file_type") == file_type:
            f = extract_file_metadata(file_obj)
            combined = {**x, **f}
            rows.append(combined)

    return rows


def append_to_tsv(rows, output_file):

    file_exists = os.path.isfile(output_file)

    with open(output_file, "a", newline="") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=rows[0].keys(),
            delimiter="\t"
        )

        if not file_exists:
            writer.writeheader()

        writer.writerows(rows)
