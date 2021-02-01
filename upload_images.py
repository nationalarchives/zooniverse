import csv
import re
import credentials
import os
import time

from collections import defaultdict
from panoptes_client import Panoptes, Project, SubjectSet, Subject

subject_data_file = 'WO399_11Jun2020-trunc.tsv'
subject_file_list = 'wo_399_file_list.txt'
subject_file_root = credentials.subject_file_root
subject_file_old_root_re = ''
if credentials.subject_file_old_root != '':
    subject_file_old_root_re = re.compile(credentials.subject_file_old_root)
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
    print("Attempting to create a subject set via the Zooniverse API")
    subject_set = SubjectSet()
    subject_set.links.project = project
    subject_set.display_name = docref + " - " + name
    subject_set.save()
    return subject_set

with open(subject_file_list,'r') as f:
    print("Reading the list of files on the filer")
    for row in f:
        piece_match = file_path_extraction_re.search(row)
        piece = piece_match.group(1)
        filepath = row
        if subject_file_old_root_re != '':
            filepath = subject_file_old_root_re.sub(subject_file_root,filepath)
            filepath = re.sub('\\\\','/',filepath)
        file_inventory[piece].append(filepath.rstrip())
print(str(len(file_inventory)) + " pieces loaded from subject_file_list")

with open(subject_data_file,'r') as f:
    print("Reading the data file for this upload")
    csvreader = csv.reader(f, delimiter='\t')
    for row in csvreader:
        docref, name = row[1], row[5]
        print("Processing "+docref)
        # the next line defines a "regular expression" that will only match piece-level (and lower) docrefs
        match = piece_ref_re.match(docref)
        if match:
            subject_set = create_subject_set(docref,name)
            # Now scan the file_inventory dict for the files that make up this subject set
            new_subjects = list()
            for filename in file_inventory[match.group(1)]:
                start_time = time.time()
                file_size = os.stat(filename).st_size
                print("Processing "+filename+" ("+str(file_size)+")")
                subject = Subject()
                subject.links.project = project
                subject.add_location(filename)
                print("Uploading "+filename)
                subject.save()
                new_subjects.append(subject)
                elapsed_time = time.time() - start_time
                throughput = file_size / elapsed_time
                print("Elapsed time: "+str(elapsed_time)+"s ("+str(int(throughput))+"/s)")
            subject_set.add(new_subjects)
        # else:
        #     raise("Unable to extract a piece reference from "+docref)
