from datetime import datetime
from welcome_page import connect, format_date

majors = ["AIs", "CS", "ISM", "DSA", "SE"]

original = ".\sites\populations.html"


def replace_in_html(html_content, replacements):
    for key, value in replacements.items():
        html_content = html_content.replace(key, value)
    return html_content


def main():
    for major in majors:
        new_file = f"./sites/population_html/{major}.html"

        connection = connect()
        cursor = connection.cursor()

        cursor.execute(
            "select sub.student_epita_email, sub.contact_first_name, sub.contact_last_name, concat(sub.contact_first_name, ' ', sub.contact_last_name) as full_name, "
            "sum(sub.passed) as passed, count(sub.passed) as total,  sub.student_population_period_ref "
            "from (select s.student_epita_email, c.contact_first_name, c.contact_last_name, s.student_population_period_ref, g.grade_course_code_ref, "
            "CASE WHEN sum(g.grade_score * e.exam_weight) / sum(e.exam_weight) >= 10 then 1 else 0 end as passed "
            "from students s "
            "join contacts c on s.student_contact_ref = c.contact_email "
            "join grades g on s.student_epita_email = g.grade_student_epita_email_ref "
            "join exams e on g.grade_course_code_ref = e.exam_course_code "
            f"where s.student_population_code_ref like '{major}' "
            "group by s.student_epita_email, c.contact_first_name, c.contact_last_name, s.student_population_period_ref, g.grade_course_code_ref) as sub "
            "group by sub.student_epita_email, sub.contact_first_name, sub.contact_last_name, sub.student_population_period_ref "
            "order by sub.student_epita_email "
        )

        students_data = cursor.fetchall()

        cursor.execute(
            "select c.course_code, c.course_name, count(*) as 'session count' "
            "from courses c "
            "join sessions s on c.course_code = s.session_course_ref "
            "join programs p on c.course_code = p.program_course_code_ref "
            f"where p.program_assignment like '{major}' "
            "group by c.course_code, c.course_name "
        )

        courses_data = cursor.fetchall()

        cursor.close()
        connection.close()

        new_file = f"./sites/population_html/{major}.html"

        with open(original, "r") as f:
            html = f.read()

        html = html.replace("%major%", major)

        with open("./sites/student_row_fragment.html", "r") as file:
            students_rows_fragment = file.read()

        students_rows_fall = ""
        student_rows_spring = ""

        for tup in students_data:
            fullname = tup[3].replace(" ", "_")
            student_grade_href = f"../grade_html/{fullname}.html"
            temp = students_rows_fragment.replace(r"%grades_href%", student_grade_href)
            temp = temp.replace(r"%student_email%", tup[0])
            temp = temp.replace(r"%student_fname%", tup[1])
            temp = temp.replace(r"%student_lname%", tup[2])
            temp = temp.replace(r"%student_fullname%", tup[3])
            temp = temp.replace(r"%pass_count%", f"{tup[4]}/{tup[5]}")
            if tup[6] == "FALL":
                students_rows_fall += temp
            else:
                student_rows_spring += temp

        with open("./sites/course_row_fragment.html", "r") as file:
            courses_rows_fragment = file.read()

        courses_row = ""

        for tup in courses_data:
            gcourse_href = f"../course_grade_html/{tup[0]}.html"
            temp = courses_rows_fragment.replace(r"%course_id%", tup[0])
            temp = temp.replace(r"%course_name%", tup[1])
            temp = temp.replace(r"%sessions_count%", str(tup[2]))
            temp = temp.replace("%gcourse_href%", gcourse_href)
            courses_row += temp

        formatted_datetime = format_date(datetime.now())

        html = replace_in_html(
            html,
            {
                "%students_rows_fall%": students_rows_fall,
                "%students_rows_spring%": student_rows_spring,
                "%courses_rows%": courses_row,
                "%datetime%": formatted_datetime,
            },
        )

        with open(new_file, "w") as f:
            f.write(html)

        print(f"Created {new_file}")


if __name__ == "__main__":
    main()
