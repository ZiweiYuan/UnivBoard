import os, json
from elasticsearch import Elasticsearch

#connect to our cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def create_programs(input_dir):
    count = 1
    for path, subdirs, files in os.walk(input_dir):
        for filename in files:
            if not filename.endswith(".json"):
                continue
            file = open(os.path.join(path, filename))
            data = file.read()
            depart_list = json.loads(data)

            for depart_oj in depart_list:
                university = depart_oj["university"]
                school = depart_oj["school"]
                department = depart_oj["department"]
                # description = depart_oj["description"]
                programs = depart_oj["programs"]

                for program in programs:
                    program["university"] = university
                    program["school"] = school
                    program["department"] = department
                    if department == "":
                        program["department"] = "Graduate"
                    es.index(index='scu-program', doc_type='program', id=count, body=program)
                    count += 1

def create_courses(input_dir):
    count = 1
    for path, subdirs, files in os.walk(input_dir):
        for filename in files:
            if not filename.endswith(".json"):
                continue
            file = open(os.path.join(path, filename))
            data = file.read()
            depart_list = json.loads(data)

            for depart_oj in depart_list:
                university = depart_oj["university"]
                school = depart_oj["school"]
                department = depart_oj["department"]
                # description = depart_oj["description"]
                courses = depart_oj["courses"]

                for course in courses:
                    course["university"] = university
                    course["school"] = school
                    course["department"] = department
                    if department == "":
                        course["department"] = "Graduate"
                    es.index(index='scu-course', doc_type='course', id=count, body=course)
                    count += 1


create_programs("data/SCU/Programs")
create_courses("data/SCU/Courses")
