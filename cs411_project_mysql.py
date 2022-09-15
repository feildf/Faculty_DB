import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="test_root",
    database="academicworld"
)

mycursor = mydb.cursor()

def faculty_publication_by_year(name):
    sql = 'SELECT year, publication_count FROM FacultyPublicationYear WHERE faculty_id = (SELECT id FROM faculty WHERE name = "{}")'.format(name)
    mycursor.execute(sql)
    myresult = list(mycursor.fetchall())
    return myresult

def all_faculty_name():
    sql = 'SELECT name FROM faculty'
    mycursor.execute(sql)
    myresult = list(mycursor.fetchall())
    return myresult

def all_keyword():
    sql = 'SELECT name FROM keyword'
    mycursor.execute(sql)
    myresult = list(mycursor.fetchall())
    return myresult

def top_faculty_by_keyword(keyword):
    sql = 'SELECT faculty.name, score FROM faculty, faculty_keyword, keyword WHERE faculty.id = faculty_id AND keyword_id = keyword.id AND keyword.name = "{}" ORDER BY score DESC LIMIT 10'.format(keyword)
    mycursor.execute(sql)
    myresult = list(mycursor.fetchall())
    return myresult

def get_publication_id(title):
    sql = 'SELECT id FROM publication WHERE title = "{}"'.format(title)
    mycursor.execute(sql)
    myresult = list(mycursor.fetchone())
    return myresult[0]

def get_faculty_id(name):
    sql = 'SELECT id FROM faculty WHERE name = "{}"'.format(name)
    mycursor.execute(sql)
    myresult = list(mycursor.fetchone())
    return myresult[0]

def get_usable_id():
    for id in range(1, 2147483647):
        sql = 'select ({} in (select id from publication))'.format(id)
        mycursor.execute(sql)
        myresult = list(mycursor.fetchone())[0]
        if myresult == 0:
            return id
    return -1

def insert_publication(publication_info):
    id = get_usable_id()
    sql = 'INSERT INTO publication VALUES ({}, "{}", "{}", "{}", {})'.format(id, publication_info['title'], publication_info['venue'], publication_info['year'], publication_info['num_citations'])
    mycursor.execute(sql)
    mydb.commit()
    return id

def insert_publications(n_clicks, data, name):
    f_id = get_faculty_id(name)
    for publication_info in data:
        try:
            p_id = insert_publication(publication_info)
        except:
            pass
        else:
            sql = 'INSERT INTO faculty_publication VALUES ({}, {})'.format(f_id, p_id)
            mycursor.execute(sql)
            mydb.commit()

def keyword_by_faculty(name):
    sql = 'SELECT keyword.name, score FROM faculty, faculty_keyword, keyword WHERE faculty.id = faculty_id AND keyword_id = keyword.id AND faculty.name = "{}" ORDER BY score DESC'.format(name)
    mycursor.execute(sql)
    myresult = list(mycursor.fetchall())
    return myresult

def university_info(name):
    sql = 'SELECT * FROM university WHERE name = "{}"'.format(name)
    mycursor.execute(sql)
    myresult = list(mycursor.fetchone())
    return {'id':myresult[0], 'name':myresult[1], 'photoUrl':myresult[2]}
