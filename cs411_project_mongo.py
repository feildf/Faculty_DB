from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/")
mydb = client["academicworld"]

def faculty_info_by_name(name):
    return mydb.faculty.find_one({"name": name})

def update_faculty_info(data, name, university_info):
    filter = {"name": name}
    newvalues = {"$set": {'position': data['Position'], 'email': data['Email'], 'phone': data['Phone'], 'affiliation': university_info}}
    mydb.faculty.update_one(filter, newvalues)

def faculty_keyword_by_name(name):
    return mydb.faculty.find_one({"name": name}, {"_id":0, "keywords.name":1, "keywords.score":1})
