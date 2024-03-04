from welcome_page import connect, format_date
from population import replace_in_html
from datetime import datetime

names = ['Albina Glick', 'Ammie Corrio', 'Bette Nicka', 'Bernardo Figeroa', 'Blondell Pugh', 'Cammy Albares', 'Carmelina Lindall', 'Cecily Hollack', 'Danica Bruschke', 'Delmy Ahle', 'Dominque Dickerson', 'Donette Foller', 'Elza Lipke', 'Emerson Bowley', 'Erick Ferencz', 'Ernie Stenseth', 'Francine Vocelka', 'Gladys Rim', 'Jamal Vanausdal', 'Jina Briddick', 'Kallie Blackwood', 'Kanisha Waycott', 'Kati Rulapaugh', 'Kiley Caldarera', 'Kris Marrier', 'Lai Gato', 
         'Laurel Reitler', 'Leota Dilliard', 'Lettie Isenhower', 'Lavera Perin', 'Malinda Hochard', 'Minna Amigon', 'Marjory Mastella', 'Myra Munns', 'Moon Parlato', 'Maryann Royster', 'Natalie Fern', 'Rozella Ostrosky', 'Sage Wieser', 'Simona Morasca', 'Solange Shinko', 'Tamar Hoogland', 'Tawna Buvens', 'Timothy Mulqueen', 'Tyra Shields', 'Tonette Wenner', 'Veronika Inouye', 'Viva Toelkes', 'Wilda Giguere', 'Yuki Whobrey']


# Code that creates names list:
"""

names_column = '''  # this column is copied from database
Albina Glick
Ammie Corrio
Bette Nicka
Bernardo Figeroa
Blondell Pugh
...
Whobrey Yuki

'''

names = names_column.strip().split('\n')

print(names)

"""

intake_mapping = {"FALL": "F2020", "SPRING": "S2021"}

original = "sites/grades.html"


def main():
    for name in names:
        new_name = name.replace(" ", "_")
        new_file = f"./sites/grade_html/{new_name}.html"

        with connect() as connection, connection.cursor() as cursor:
            cursor.execute(
                "select s.student_epita_email, c.contact_first_name, c.contact_last_name, concat(c.contact_first_name, ' ', c.contact_last_name) as fullname, s.student_population_period_ref, "
                "s.student_population_code_ref,g.grade_course_code_ref, sum(g.grade_score * e.exam_weight) / sum(e.exam_weight) as grade "
                "from contacts c "
                "join students s on c.contact_email = s.student_contact_ref "
                "join grades g on s.student_epita_email = g.grade_student_epita_email_ref "
                "join exams e on g.grade_course_code_ref = e.exam_course_code "
                f"where concat(c.contact_first_name, ' ', c.contact_last_name) like '{name}' "
                "group by e.exam_course_code, s.student_epita_email, c.contact_last_name, c.contact_last_name "
            )

            data = cursor.fetchall()

        new_file = f"./sites/grade_html/{new_name}.html"

        with open(original, "r") as f:
            html = f.read()

        html = html.replace("%full_name%", name)

        with open("./sites/grade_row_fragment.html", "r") as file:
            grades_row_fragment = file.read()

        grades_rows = ""

        for tup in data:
            grade_str = str(tup[7])
            grade = grade_str.rstrip("0").rstrip(".") if "." in grade_str else grade_str
            temp = grades_row_fragment.replace(r"%student_email%", tup[0])
            temp = temp.replace(r"%student_fname%", tup[1])
            temp = temp.replace(r"%student_lname%", tup[2])
            temp = temp.replace(r"%course_id%", tup[6])
            temp = temp.replace(r"%grade%", str(grade))
            grades_rows += temp
            

        html = replace_in_html(
            html,
            {
                "%major%": tup[5],
                "%intake%": intake_mapping.get(tup[4]),
                "%grade_rows%": grades_rows,
                "%datetime%": format_date(datetime.now()),
            },
        )

        with open(new_file, "w") as f:
            f.write(html)

        print(f"Created {new_file}")


if __name__ == "__main__":
    main()
