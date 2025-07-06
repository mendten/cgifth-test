from csv import reader
from points.models import *
from datetime import date

PROGRAM = Program.objects.get(name='CGI Florida Main Camp 5784')

def main():
    with open('bunk_list.csv') as f:
        csv_reader = reader(f)
        current_bunk = False
        bunk_number = 1
        counselors = 0
        for row in csv_reader:
            print(row)
            if row[0] == '':
                continue
            if 'Bunk' in row[0]:
                current_bunk = create_group(row, bunk_number)
                bunk_number += 1
                counselors = 0
            elif counselors < 2:
                get_counselor(row, current_bunk)
                counselors += 1
            else:
                create_camper(row, current_bunk)


def create_group(row, bunk_number):
    bunk = Group(
        program=PROGRAM,
        name=row[0],
        group_type='bunk',
        number=bunk_number,
    )
    bunk.save()
    return bunk


def get_counselor(row, group):
    # split on the last space to get the last name
    last_name = row[0].strip().split(' ')[-1]
    # first name is everything before the last name
    first_name = row[0].strip()[:-len(last_name)].strip()
    try:
        counselor = User.objects.get(first_name=first_name, last_name=last_name)
    except User.DoesNotExist:
        counselors = User.objects.filter(position='counselor', group=None)
        print(f'No object found for {first_name} {last_name}. Here are the counselors: ')
        for c in counselors:
            is_the_right_counselor = input(f'Is {c.first_name} {c.last_name} the right counselor? (y/n)')
            if is_the_right_counselor.lower() == 'y':
                counselor = c
                counselor.first_name = first_name
                counselor.last_name = last_name
                username = first_name[0].lower() + last_name.lower()
                counselor.username = username
                counselor.set_password(username)
                counselor.save()
                break
    group.staff.add(counselor)
    group.save()
    return True


def create_camper(row, group):
    first_name = row[1]
    last_name = row[0]
    camper = Camper(
        program=PROGRAM,
        first_name=first_name,
        last_name=last_name,
        new_bunk=group,
    )
    camper.save()
    return True


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        print('Something went wrong. Exiting...')
        exit(1)


def resequence():
    marked_lines = MarkedSheetLine.objects.filter(sequence=0)
    total = str(len(marked_lines))
    for i, line in enumerate(marked_lines):
        print('fixing line ' + str(i) + '/' + total)
        blank_line = BlankSheetLine.objects.get(group=line.group, task=line.task)
        line.sequence = blank_line.sequence
        line.save()


def dictify_blank_line():
    blank_lines = BlankSheetLine.objects.all()
    for i, line in enumerate(blank_lines):
        print('fixing line ' + str(i) + '/' + str(len(blank_lines)))
        line.set_checklist_dict()
        line.save()
    print('done')


def clean_up():
    campers = Camper.objects.all()
    # start_date = PROGRAM.info.first().start_date
    # today = date.today()
    for camper in campers:
        print('cleaning up ' + camper.first_name + ' ' + camper.last_name)
        sheets = camper.sheet.filter()
        for sheet in sheets:
            deleted = False
            try:
                is_there_another_sheet = MarkedSheet.objects.filter(camper=camper, date=sheet.date)
            except MarkedSheet.DoesNotExist:
                pass
            # if multiple sheets exist for the same date, delete whichever one has 0 points. If both have zero, delete either one
            sheets_to_delete = []
            good_sheet = False
            if len(is_there_another_sheet) > 1:
                print('multiple sheets found for ' + str(sheet.date) + ' for ' + camper.first_name + ' ' + camper.last_name)
                for other_sheet in is_there_another_sheet:
                    print(other_sheet, 'TOTAl: ', sheet.total)
                    if sheet.total == 0:
                        sheets_to_delete.append(other_sheet)
                    elif good_sheet and sheet.total > good_sheet.total:
                        sheets_to_delete.append(good_sheet)
                        good_sheet = other_sheet
                    else:
                        good_sheet = other_sheet
                if len(sheets_to_delete) >= 1:
                    if good_sheet:
                        for sheet_to_del in sheets_to_delete:
                            if sheet_to_del == sheet:
                                deleted = True
                            sheet_to_del.delete()

                    else:
                        good_sheet = sheets_to_delete[0]
                        for sheet_to_del in sheets_to_delete[1:]:
                            if sheet_to_del == sheet:
                                deleted = True
                            sheet_to_del.delete()
                elif len(sheets_to_delete) == 1 and good_sheet:
                    for sheet_to_del in sheets_to_delete:
                        if sheet_to_del == sheet:
                            deleted = True
                        sheet_to_del.delete()

            else:
                print('only one sheet found for ' + str(sheet.date) + ' for ' + camper.first_name + ' ' + camper.last_name)
            if not deleted:
                sheet.week = PROGRAM.get_week('number', sheet.date)
                sheet.save()
            # sheet.save()
            

def generate_weekly_chart():
    campers = Camper.objects.all().order_by('new_bunk__number', 'last_name')
    for camper in campers:
        print('generating chart for ' + camper.first_name + ' ' + camper.last_name)
        camper.set_total_points()
        for week in [1, 2, 3, 4]:
            print('     week ' + str(week))
            for group in [camper.new_bunk, camper.new_class]:
                print('         group ' + group.name)
                try:
                    chart = WeeklyChart.objects.get(program=PROGRAM, camper=camper, group=group, week=week)
                except:
                    chart = WeeklyChart(
                        program=PROGRAM,
                        camper=camper,
                        group=group,
                        week=week,
                    )
                    chart.generate_chart(week=week)
                    chart.save()
    print('done')


def fix_name():
    user = User.objects.get(username='sbrashavitzki')
    user.last_name = 'Brashevitzky'
    user.username = 'sbrashevitzky'
    user.set_password('sbrashevitzky')
    user.save()


def enable_admin_task():
    blank_lines = BlankSheetLine.objects.filter(task__name='Admin total')
    for line in blank_lines:
        line.active = True
        line.points_type = 'custom'
        line.save()
    groups = Group.objects.all()
    for group in groups:
        if not BlankSheetLine.objects.filter(group=group, task__name='Admin total'):
            task = Task.objects.get(name='Admin total', task_type=group.group_type)
            line = BlankSheetLine(
                group=group,
                task=task,
                max_points=50,
                sequence=100,
                active=True,
            )
            line.save()
        line.set_checklist_dict()
        group.save()


def add_admin_task_to_marked_sheets():
    sheets = MarkedSheet.objects.all().order_by('group__number', 'camper__last_name', 'date')
    total = str(len(sheets))
    for i, sheet in enumerate(sheets):
        print('fixing sheet ' + str(i) + '/' + total)
        if not sheet.line.filter(task__name='Admin total'):
            print('sheet does not have admin task')
            task = Task.objects.get(name='Admin total', task_type=sheet.group.group_type)
            line = MarkedSheetLine(
                sheet=sheet,
                group=sheet.group,
                camper=sheet.camper,
                points_type='custom',
                date=sheet.date,
                week=sheet.week,
                task=task,
                points=0,
                sequence=100,
            )
            line.save()
        else:
            print('sheet already has admin task')
