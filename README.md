Title: Exploration of Faculty in The Academic World.

Purpose: The application scenario is for anyone to learn more about particular faculty members in the academic world. Target users are students (or anyone) who want to gather information on faculty members. The objective is to provide a user-friendly app to display interesting information of faculty members, search faculty based on keywords, search and update faculty publication records and explore connection between faculty members.

Demo: https://mediaspace.illinois.edu/media/t/1_6es4o21y

Installation: The databases are installed according to the MPs.

Usage:
Potential users should use the web app. Dropdown selectors are available for users to select names of faculty members and keywords, which will cause various widgets to populate. Details of each widget will be discussed below.

Design:
The overall architecture of the web app is composed of six widgets that are organized in a straightforward layout. Widgets 1 and 3 are updating widgets.

Widget 1: Faculty Basic Info.
Users can select a faculty member from the dropdown menu, and position, email, phone and university of the selected faculty member will be displayed in a table. This table is editable, and users can choose any field and type in new information. Clicking the “Update Faculty Basic Info” bottom will commit the change and update the MongoDB database in the backend. In addition, an image of the faculty member will be displayed as well.

Widget 2: Faculty Number of Publications by Year.
This widget takes the same input as widget 1. It displays the numbers of publications of that particular faculty member by year in a bar chart. The horizontal axis is the year and the vertical axis is the number of publications.

Widget 3: New Publications in 2022.
Since the databases only has publication information up to 2021, the widget allows users to specify a faculty member, and then searches Google Scholar for his or her latest publications in 2022, which will be displayed as a list. The users can then click the “Insert New Publications” bottom and commit to add these new publications to the MySQL database. If a publication already exists, it will not be added.

Widget 4: Faculty by Keyword.
Users can select a keyword from the dropdown menu, and the top 10 faculty members relevant to that keyword will be displayed in a list, ranked by their keyword score in the faculty_keyword table.

Widget 5: Display Fields of Interests by Faculty.
Users can select a faculty member from the dropdown menu, and a pie chart will be displayed to show all the associated keywords in the faculty_keyword table. The size of the wedge in the pie chart is proportional to the keyword score.

Widget 6: Co-authored Publications by Two Faculty Members.
Users can select two faculty members from the dropdown menus, and a list of their co-authored publications will be displayed. If they haven’t co-authored any publication, “No co-authored publication” will be displayed instead.

Implementation:
The front-end of this web app is implemented using Dash Plotly, which uses callback functions to connect to the MySQL, MongoDB and Neo4j databases in the back-end. Details of each widget is discussed below.

Widget 1: Faculty Basic Info.
The implementation of this widget is pretty straightforward. The MongoDB database is queried with the name selected from the dropdown menu using the find() method, and position, email, phone, university and picture are parsed from the returned dictionary. If the users input new values for the above fields, they can be used to update the MongoDB database with the update_one() method.

Widget 2: Faculty Number of Publications by Year.
This widget uses the MySQL database. A view named “FacultyPublicationYear” was constructed that contains three fields: faculty_id, year and publication_count. An index was created for the “name” field in the “faculty” relation, that allows us to quickly obtain faculty_id using name, which is then used to query the view to get year and publication_count, displayed as a plotly bar chart.

Widget 3: New Publications in 2022.
Here I use the Python Scholarly library to query Google Scholar with faculty name to obtain a list of publications, which is then filtered to display only publications in 2022. If the users want to insert these new publications into the MySQL database, first unused ids will be generated for these publications. Next we attempt to insert the publications into the “publication” relation. A trigger was set up so that if the publication already exists, the insertion would result in an error which we will catch. Finally, if the insertion is successful, we then insert faculty_id and publication_id into the “faculty_publication” relation.

Widget 4: Faculty by Keyword.
This widget uses the MySQL database. We join the “faculty”, “faculty_keyword” and “keyword” relations and query with the name of the keyword. A list of faculty is returned, ranked by their scores associated with the keyword.

Widget 5: Display Fields of Interests by Faculty.
This widget uses the MongoDB database. We query by faculty name and return a list of keywords and the associated scores, which are then displayed with a Plotly pie chart.

Widget 6: Co-authored Publications by Two Faculty Members.
This widget uses the Neo4j database. Given two faculty members, we match them to the same publication. These publications are returned and displayed if they exist.

Database Techniques:
1. Indexing.
This technique is used in widget 2, 3 and 4. We need to query the “faculty” relation in the MySQL database to obtain the id. The key of this relation is the id, however, the users will input faculty names. To allow efficient querying with names, index was created for the “name” variable.

2. View.
This technique is used in widget 2. A view named “FacultyPublicationYear” was constructed that contains three fields: faculty_id, year and publication_count, so we can easily query by faculty and plot numbers of publications by year. The following output is obtained with the “SHOW CREATE VIEW” command that shows the definition of the view.
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `facultypublicationyear` AS select `faculty_publication`.`faculty_id` AS `faculty_id`,`publication`.`year` AS `year`,count(0) AS `publication_count` from (`faculty_publication` join `publication`) where (`faculty_publication`.`publication_id` = `publication`.`id`) group by `faculty_publication`.`faculty_id`,`publication`.`year` order by `faculty_publication`.`faculty_id`,`publication`.`year`

3. Trigger.
This technique is used in widget 3. When we insert new publications into the “publication” relation, if a publication with the same title already exists, the insertion will not go through and an error will be returned, which will be caught in Python. The following output is obtained with the “SHOW TRIGGERS” command that shows the definition of the trigger.
InsertPreventTrigger | INSERT | publication | BEGIN IF(new.title IN (select title from publication)) THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Publication already existed'; END IF; END | BEFORE

Extra-Credit Capabilities:
1. External data sourcing.
This is used in widget 3, where we query Google Scholar to obtain the latest list of publications by a faculty member to insert into the database. Code used to query Google Scholar is in cs411_project_scholarly.py.

2. Multi-database querying.
This is used in widget 1. When we update the university of a faculty member, we first query the “university” relation in the MySQL database to obtain the university_id and photoUrl, which are then changed in the MongoDB database, together with the university name.

Contributions:
I completed this project alone, which took me about 20 hours, including learning Dash Plotly and writing queries in Python.
