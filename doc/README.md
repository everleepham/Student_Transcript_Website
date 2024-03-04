## Project: Student Transcript Website

##### Student: PHAM Phuong Khanh
##### Bsc F2023

***
***

#### 1. Page description:

This project aims to create a student transcript static website using Python, HTML, CSS, and SQL. 

To provide an overview of my website, I will include some images:

![image 1](./img%201.png)
In this image, all elements in the **Overall Active Population** list are clickable, enabling users to access the **Population** page for each group.


![image 2](./img%202.png)
The **Population** page consists of two sections: **Students** and **Courses**. The **Students** section contains two tables, one for Fall intake students and one for Spring intake students. Each student's email is clickable, allowing users to access the **Grade** page.


![image 3](img%203.png)
The **Grade** page allows users to view the transcript of each student, detailing every subject in their program.

![image 4](img%204.png)
Each items in the **Course** table are also clikable, allowing users to view the grades of every student in each course.

![image 5](img%205.png)

On every page, the **Welcome** link at the top is clickable and enables users to return to the **Welcome page**.


*** 
#### 2. Code explanation:

My project contains only 4 components: Python, HTML and CSS and SQL.  I have made a deliberate choice not to utilize frameworks such as Flask, Django, Tornado, etc for this project. Instead, I have solely relied on Python to automatically query the database.

How does it operate?

<u>a. HTML and CSS:</u>
Following your guidance, I created HTML template files featuring placeholders such as population.html, welcome_page.html, grades.html, and course_grade.html. 

Additionally, I generated fragment files: course_row_fragment.html, gcourse_row_frag.html, grade_row_fragment.html, and student_row_fragment.html.

<u>b. Python</u>
My Python scripts are tasked with connecting to the database and executing queries. Subsequently, they retrieve the template files and fragments, incorporate appropriate content into a new HTML file, and then save it.

<u>c. Chart</u>
About the charts, I used Matplotlib to create the chart, save it into the sites folder and link it to the website by html.

***

#### 3. How to run it?:

1. First, after changed the connection of the database in the welcome_page.py file into yours, you need to run the welcome_page.py script first and the population.py and then the rest in src folder.

2. After ran all of the python scripts, you can go to the index.html file in the sites folder and press 'Go Live'

*** 
### Conclusion

Perhaps this isn't the optimal approach for creating the website, and utilizing libraries or frameworks could have been much easier. However, the process of creating the website has taught me a great deal about Python, and for that, I am truly grateful.