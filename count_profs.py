from requests import get
from bs4 import BeautifulSoup

base_url = "https://www.matse.itc.rwth-aachen.de/dienste/public/index.php?m=courses/seminar&p=seminar_overview" \
           "&selectSeminar="


def extract_profs_from_url(url):
    response = get(url)

    soup = BeautifulSoup(response.text, features="html.parser")
    table_data = soup.select("td:nth-child(6)")

    profs = map(lambda td: td.contents[0].split(":")[1][1:], table_data)
    return profs


def count_seminars(profs, prof_seminar_count_dict):
    # Count how often each professor supervised a Seminararbeit
    for prof in profs:
        if prof not in prof_seminar_count_dict:
            prof_seminar_count_dict[prof] = 0

        prof_seminar_count_dict[prof] += 1


def sort_by_seminars(prof_seminar_count_dict):
    return dict(sorted(prof_seminar_count_dict.items(), key=lambda item: item[1]))


def print_overview(prof_seminar_count_dict):
    for prof, count in sort_by_seminars(prof_seminar_count_dict).items():
        print(count, ": ", prof)


def main():
    prof_seminar_count_dict = {}
    for i in range(7, 16):
        url = base_url + str(i)
        profs = extract_profs_from_url(url)
        count_seminars(profs, prof_seminar_count_dict)

    print_overview(prof_seminar_count_dict)


if __name__ == "__main__":
    main()
