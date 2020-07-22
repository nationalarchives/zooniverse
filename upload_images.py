import requests
import csv
import re
import credentials
from collections import defaultdict
from panoptes_client import Panoptes, Project, SubjectSet, Subject

subject_data_file = 'WO399_11Jun2020-trunc.tsv'
subject_file_list = 'wo_399_file_list.txt'
subject_file_root = credentials.subject_file_root
file_inventory = defaultdict(list)

project_id = 11982
# we are only interested in the Piece-level records in the catalogue export.
# the following regex matches Piece references (and lower) only.
piece_ref_re = re.compile(r'WO 399/(\d+)')
file_path_extraction_re = re.compile(r'wo\\399\\(\d+)')

Panoptes.connect(username=credentials.username, password=credentials.password)
project = Project(project_id)

# Read the subject_data_file to get the names and docrefs of the documents
# Identify the images that belong to a subject set and upload them

def create_subject_set(docref,name):
    subject_set = SubjectSet()
    subject_set.links.project = project
    subject_set.display_name = docref + " - " + name
    subject_set.save()
    return subject_set

with open(subject_file_list,'r') as f:
    for row in f:
        piece_match = file_path_extraction_re.search(row)
        piece = piece_match.group(1)
        file_inventory[piece].append(row.rstrip())

with open(subject_data_file,'r') as f:
    csvreader = csv.reader(f, delimiter='\t')
    for row in csvreader:
        docref, name = row[1], row[5]
        # the next line defines a "regular expression" that will only match piece-level (and lower) docrefs
        match = piece_ref_re.match(docref)
        if match:
            subject_set = create_subject_set(docref,name)
            # Now scan the file_inventory dict for the files that make up this subject set
            new_subjects = list()
            for filename in file_inventory[match.group(1)]:
                subject = Subject()
                subject.links.project = project
                subject.add_location(filename)
                subject.save()
                new_subjects.append(subject)
            subject_set.add(new_subjects)
