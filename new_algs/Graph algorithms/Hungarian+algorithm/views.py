import datetime
from django.urls import reverse
from munkres import Munkres, make_cost_matrix, DISALLOWED
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from matching.models import CsvFile


def handle_uploaded_file(fin):
  data = str(fin.read(), encoding="UTF-8")
  csv_file = CsvFile(text=data)
  csv_file.save()
  return csv_file.id


def index(request):
  if request.method == 'POST':
    csv_id = handle_uploaded_file(request.FILES['datafile'])
    return HttpResponseRedirect(reverse("show_csv_file", args=[csv_id]))
  return render(request, 'upload.html')


def list_files(request):
  csv_files = CsvFile.objects.all()
  time_delta = datetime.timedelta(hours=-4)
  for f in csv_files:
    f.url = reverse("show_csv_file", args=[f.id])
    f.created = f.created + time_delta
  context = {
    "csv_files": csv_files
  }
  return render(request, "list_files.html", context=context)


def show_csv_file(request, csv_id):
  data = CsvFile.objects.filter(id=csv_id).first().text.strip()
  mentors = set()
  mentees = set()
  lines = data.splitlines()
  for line in lines[1:]:
    if len(line) <= 1:
      continue
    print(line)
    mentor, mentee, utility = [x.strip() for x in line.split(',')]
    mentors.add(mentor)
    mentees.add(mentee)

  matrix = [[DISALLOWED] * len(mentees) for x in mentors]
  mentors = {x[1]: x[0] for x in enumerate(sorted(mentors))}
  mentees = {x[1]: x[0] for x in enumerate(sorted(mentees))}
  for line in lines[1:]:
    if len(line) <= 1:
      continue
    mentor, mentee, utility = [x.strip() for x in line.split(',')]
    utility = float(utility)
    matrix[mentors[mentor]][mentees[mentee]] = utility

  cost_matrix = make_cost_matrix(matrix, lambda cost: (200 - cost) if (cost != DISALLOWED) else DISALLOWED)
  m = Munkres()
  indexes = m.compute(cost_matrix)

  mentors = {v: k for k, v in mentors.items()}
  mentees = {v: k for k, v in mentees.items()}
  used_mentors = set()
  used_mentees = set()
  table = []
  for row, column in indexes:
    value = matrix[row][column]
    mentor = mentors[row]
    mentee = mentees[column]
    table.append([mentor, mentee, value])
    used_mentors.add(mentor)
    used_mentees.add(mentee)

  mentors = set([x for x in mentors.values()])
  mentees = set([x for x in mentees.values()])
  unused_mentees = mentees - used_mentees
  unused_mentors = mentors - used_mentors
  table = sorted(table, key=lambda x: x[0])
  context = {
    'table': table,
    'unused_mentors': unused_mentors,
    'unused_mentees': unused_mentees
  }
  return render(request, 'show_table.html', context=context)
