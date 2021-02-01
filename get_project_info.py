import credentials
from panoptes_client import Panoptes, Project, SubjectSet, Subject

project_id = 11982
Panoptes.connect(username=credentials.username, password=credentials.password)

project = Project.find(project_id)
print(project)
