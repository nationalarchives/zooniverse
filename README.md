# WO 399 Zooniverse Upload

This repo contains scripts related to data upload for the WO 399 project with Zooniverse.

The script references external data files which aren't in the repo:

- a subject_data_file, a metadata TSV file which needs to be in this directory and contains the information needed to select the documents to upload and create their descriptions within the Zooniverse platform. Amend the value of the variable to match the name of the file you're using.
- a subject_file_list, a list of file locations containing the images for the project. Amend the value of the variable to match the name of the file you're using.
- a credentials.py file which contains your Zooniverse credentials and the path to the image files:

```
username='<username>'
password='<password>'
subject_file_root='\\\\<servername>\\<sharename>\\'`
```
The script is hardcoded to look for the Document Reference in column 2 and the document name in column 6 of the metadata TSV file.
The file listing is expected to be of the format output by the command:

`dir /b/s/a-d/on >file_list.txt`

The script will then work out from the file paths which record each image belongs to (our standard filing convention is a directory tree like ../WO/399/1/0/0001.jpg)

## Testing
It is advisable to run some tests first, and the best way to do this is to deliberately use a truncated metadata file containing just one or two records.
