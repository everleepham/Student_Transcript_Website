import matplotlib.pyplot as plt
from welcome_page import connect


connection = connect()
cursor = connection.cursor()

cursor.execute(
    "select s.student_population_code_ref, "
    "(count(s.student_epita_email) / (select count(*) from students s)) * 100 as percentage "
    "FROM students s "
    "group by s.student_population_code_ref "
)

pop_percentage = cursor.fetchall()

cursor.execute(
    "select s.student_population_code_ref, "
    "round(sum(a.attendance_presence) / count(*) * 100) as percentage "
    "from attendance a "
    "join students s "
    "on a.attendance_student_ref = s.student_epita_email "
    "group by s.student_population_code_ref "
)

att_percentage = cursor.fetchall()


cursor.close()
connection.close()

colors = [
    "plum",
    "cornflowerblue",
    "lightpink",
    "mediumaquamarine",
    "navajowhite",
]


def draw_pie_chart(data, output_filename):
    labels = [tup[0] for tup in data]
    size = [tup[1] for tup in data]

    plt.pie(
        size,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        textprops={"fontsize": 11},
    )

    plt.rcParams["font.size"] = 13
    plt.axis("equal")
    plt.title("Populations", pad=20)
    plt.savefig(output_filename)
    plt.show()
    plt.close()


def draw_bar_chart(data, output_filename):
    categories = [tup[0] for tup in data]
    values = [tup[1] for tup in data]

    width = 0.5

    plt.bar(categories, values, color=colors, width=width)

    for i in range(len(categories)):
        plt.text(
            i,
            float(values[i]) + 0.1,
            f"{str(values[i])}%",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.xlabel("Majors")
    plt.ylabel("Attendance percentage")
    plt.title("Overall attendance", pad=20)

    plt.savefig(output_filename)
    plt.show()
    plt.close()


draw_pie_chart(pop_percentage, "sites/population.png")
draw_bar_chart(att_percentage, "sites/attendance.png")
