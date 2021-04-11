# Todo not sure if i want to keep this at all

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'benssite.settings')

import django
django.setup()

# Population script
import random, datetime
from django.contrib.auth.models import User
from todo.models import TaskList, Task
from faker import Faker

fakegen = Faker()
tasklists = ['TaskList1', 'TaskList2', 'TaskList3']
tasks = ['Task1', 'Task2', 'Task3']
descriptions = ['desc1', 'descr2', 'descr3']
commentss = ['comm1', 'comm2', 'comm3']
users = ['Bill', 'Wayne', 'Wendy']
passwords = ['pasdfgsdfgss1', 'passeasfawef2', 'pass3asdgaegaweg']


def add_tasklist():
    # retrieves TaskList from model if it exists... or it creates it
    t = TaskList.objects.get_or_create(name=random.choice(tasklists))[0]
    t.save()
    return t



# def add_task():
#     # retrieves Task from model if it exists... or it creates it
#     t = Task.objects.get_or_create(name=random.choice(tasks))[0]
#     t.save()
#     return t


def populate(n=5):

    for entry in range(n):
        # get the task for the entry
        tsk_lst = add_tasklist()

        # create fake data for the tasklist entry
        fake_description = fakegen.random.choice(descriptions)

        fake_name= random.choice(tasks)
        fake_creation_date = datetime.timedelta(days=random.randint(-100, -1))
        fake_due_date = datetime.timedelta(days=random.randint(1, 100))
        fake_completed = random.choice([True, False])
        fake_comments = fakegen.random.choice(commentss)
        fake_username = random.choice(users)
        fake_password = random.choice(passwords)
        fake_user = User.objects.create_user(username=fake_username, password=fake_password,)

        # creates a fake task
        tsk = Task.objects.get_or_create(
            name=random.choice(tasks),
            completed=fake_completed,
            created_by = fake_user,
            due_date = fake_due_date)[0]


if __name__ == '__main__':
    print('populating script')
    populate(20)
    print('population complete')
