from django.core.validators import MaxValueValidator
from django.db import models


# Create your models here.


class Mentors(models.Model):
    name = models.CharField(max_length=25)
    designation = models.CharField(max_length=25)
    description = models.TextField()
    email = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(max_length=12)


course_select = [(None, 'Select Course'), ('M.Voc', 'M.Voc'), ('B.Voc', 'B.Voc'), ('M.Sc', 'M.Sc'),
                 ('Integrated M.Sc', 'Integrated M.Sc'),
                 ('M.Phil', 'M.Phil'), ('Ph.D', 'Ph.D'), ('M.A', 'M.A'), ('M.Tech', 'M.Tech'), ('MCA', 'MCA'),
                 ('MSc', 'MSc'), ('B.Tech', 'B.Tech'), ('LLM', 'LLM'), ('Civil Engg.(B.Tech)', 'Civil Engg.(B.Tech)'),
                 ('Computer Science & Engg.(B.Tech)', 'Computer Science & Engg.(B.Tech)'),
                 ('Electrical and Electronics Engg.(B.Tech)', 'Electrical and Electronics Engg.(B.Tech)'),
                 ('Electronics & Communication Engg.(B.Tech)', 'Electronics & Communication Engg.(B.Tech)'),
                 ('Information Technology(B.Tech)', 'Information Technology(B.Tech)'),
                 ('Mechanical Engg.(B.Tech)', 'Mechanical Engg.(B.Tech)'),
                 ('Safety & Fire Engg(B.Tech)', 'Safety & Fire Engg(B.Tech)'),
                 ('Civil Engg.(M.Tech)', 'Civil Engg.(M.Tech)'),
                 ('Computer Science & Engg.(M.Tech)', 'Computer Science & Engg.(M.Tech)'),
                 ('Electrical and Electronics Engg.(M.Tech)', 'Electrical and Electronics Engg.(M.Tech)'),
                 ('Electronics & Communication Engg.(M.Tech)', 'Electronics & Communication Engg.(M.Tech)'),
                 ('Information Technology(M.Tech)', 'Information Technology(M.Tech)'),
                 ('Mechanical Engg.(M.Tech)', 'Mechanical Engg.(M.Tech)'),
                 ('Safety & Fire Engg(M.Tech)', 'Safety & Fire Engg(M.Tech)'), ('LLB', 'LLB'), ('MBA', 'MBA'), ]

year_select = (
    (None, 'year for which allotment is required',),
    (5, "5th Year"),
    (4, "4th Year",),
    (3, "3rd Year",),
    (2, "2nd Year",),
    (1, "1st Year",),

)


class Volunteers(models.Model):
    name = models.CharField(max_length=25)
    year_of_study = models.IntegerField(choices=year_select, default=2)
    course = models.CharField(max_length=45, choices=course_select)
    email = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(max_length=12)
    profile = models.ImageField(upload_to='images/', null=True, blank=True)
    is_organiser = models.BooleanField(default=False)


