# from django.shortcuts import render  # I don't like it
import random

from django.shortcuts import render, HttpResponse, redirect

from django.http import HttpResponse, HttpResponseRedirect, Http404, StreamingHttpResponse
from django.template import loader
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail

from django.core.paginator import Paginator, Page

from .models import *

import os
import uuid
from PIL import Image
import pandas as pd


# the function name should be the route name


def index(request):
    return render(request, "polls/index.html")


def login(request, login_type):
    if request.method == "GET":
        is_login = request.session.get("is_login", False)  # maybe defualt is False
        if is_login:
            return redirect('polls:home')
        else:
            return render(request, "polls/login.html", {
                'login_type': login_type,
            })
    elif request.method == "POST":
        # User type (Attendee or Staff)

        if login_type == 'attendee':

            is_verify = request.POST.get('verify', False)
            username = request.POST.get('email', False)
            password = request.POST.get('password', False)

            print(username)

            if not username:
                messages.error(request, 'Please input your email!')
                return render(request, "polls/login.html", {
                    'login_type': 'attendee',
                    'page_stay': 'verify',
                })

            postfix = str(username).split('@')[1]

            print(postfix)

            if postfix != 'mail.uic.edu.cn':
                messages.error(request, 'UIC Email only!')
                return render(request, "polls/login.html", {
                    'login_type': 'attendee',
                    'page_stay': 'verify',
                })

            check_attendee = Attendee.objects.filter(email=username)

            if is_verify:

                if len(check_attendee) < 1:
                    # Not exist this email account
                    # Create one
                    new_attendee = Attendee(email=username)
                    new_attendee.save()
                    messages.success(request, 'Your account is created (' + str(username) + ').')

                email = request.POST['email']
                verify_code = '%06d' % random.randint(0, 999999)
                send_mail(
                    'Email verification',
                    'Your email verification code is\n' + str(verify_code) + '\nIt is valid for 5 minutes.',
                    'ugallery2022@126.com',
                    [email],
                    fail_silently=False,
                )
                email_history = EmailHistory(email=email, code=verify_code)
                email_history.save()
                messages.success(request, 'The verification information has been sent, please check.')

                return render(request, "polls/login.html", {
                    'login_type': 'attendee',
                    'page_stay': 'verify',
                })

            else:

                if len(check_attendee) < 1:
                    # Not exist this email account
                    messages.error(request,
                                   'This email address does not yet have an associated account, please click Verify to create')
                    return render(request, "polls/login.html", {
                        'login_type': 'attendee',
                        'page_stay': 'verify',
                    })

                password = request.POST.get('password', '000000')
                print('Login info:', username, password)

                email_history = EmailHistory.objects.filter(email=username).order_by('-id')[0]
                verify_code = email_history.code
                is_valid = email_history.was_generated_recently()

                if int(password) == int(verify_code) and is_valid:
                    messages.success(request, 'Login Successfully!')
                    request.session['is_login'] = "True"
                    request.session['email'] = username
                    return render(request, "polls/login.html", {
                        'login_type': 'attendee',
                        'page_stay': 'login',
                    })
                elif int(password) == int(verify_code) and not is_valid:
                    messages.error(request, 'The verification code is expired! Please try again')
                else:
                    messages.error(request, 'Error verification code! Please try again')

                return render(request, "polls/login.html", {
                    'login_type': 'attendee',
                    'page_stay': 'verify',
                })

        elif login_type == 'staff':

            password = request.POST['password']

            if password == '000000':
                request.session['is_login'] = "True"
                request.session['position'] = "admin"
                return redirect('polls:myadmin')

            try:
                staff = Staff.objects.get(password=password)
            except Staff.DoesNotExist:
                messages.error(request, 'This staff does not exist!')
                return redirect('polls:home')

            position = staff.position

            print('Login:', position)

            request.session['is_login'] = "True"
            request.session['position'] = position

            if position == 'coordinator':
                return redirect('polls:coordinator')
            elif position == 'admin':
                return redirect('polls:myadmin')
            elif position == 'chairman':
                return redirect('polls:chairman')
            elif position == 'programme_judge':
                # Get more info from database
                prog_judge = ProgrammeJudge.objects.get(staff_ptr_id=staff.id)
                programme = prog_judge.programme
                print('programme', programme)
                request.session['programme'] = programme  # Set programme info
                request.session['staff_id'] = prog_judge.password
                return redirect('polls:programme_judge')
            elif position == 'head_judge':
                # Get more info from database
                head_judge = HeadJudge.objects.get(staff_ptr_id=staff.id)
                division = head_judge.division
                print('division', division)
                request.session['division'] = division  # Set programme info
                request.session['staff_id'] = head_judge.password
                return redirect('polls:head_judge')
            else:
                return redirect('polls:home')

    return render(request, "polls/login.html", {
        'login_type': login_type,
    })


def logout(request):
    try:
        request.session.flush()
    except KeyError:
        pass
    return redirect('polls:home')


def home(request):
    is_login = request.session.get("is_login", False)

    if ('search' in request.POST) and (request.POST['search'] != ''):

        search = request.POST['search']

        poster_list = Poster.objects.filter(title__icontains=search)

    elif ('dst' in request.POST) and (request.POST['dst'] != ''):

        division = 'dst'
        poster_list = Poster.objects.filter(division=division)

    elif ('dbm' in request.POST) and (request.POST['dbm'] != ''):

        division = 'dbm'
        poster_list = Poster.objects.filter(division=division)

    elif ('dcc' in request.POST) and (request.POST['dcc'] != ''):

        division = 'dcc'
        poster_list = Poster.objects.filter(division=division)

    elif ('dhss' in request.POST) and (request.POST['dhss'] != ''):

        division = 'dhss'
        poster_list = Poster.objects.filter(division=division)

    else:

        poster_list = Poster.objects.all()

    paginator = Paginator(poster_list, 6)

    # Send to web
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if is_login:
        # cookie_content = request.COOKIES
        email = request.session.get("email", False)
        return render(request, 'polls/home.html', {
            # Basic info
            'is_login': is_login,
            'email': email,

            # Poster info
            'num_poster': len(poster_list),
            'page_obj': page_obj,
        })
    else:
        return render(request, 'polls/home.html', {
            'is_login': is_login,

            # Poster info
            'num_poster': len(poster_list),
            'page_obj': page_obj,
        })


def vote(request, poster_name):
    max_vote_num = 1

    print('Voting for:', poster_name)

    is_login = request.session.get("is_login", False)

    if is_login:

        if 'email' in request.session:

            email = request.session['email']

            # Test Case!
            # if email == "testuser@mail.uic.edu.cn":
            #     try:
            #         vote_poster = Poster.objects.get(title=poster_name)
            #     except Poster.DoesNotExist:
            #         messages.error(request, 'This poster does not exist!')
            #         return redirect('polls:home')
            #     vote_poster.increase_vote_amount()
            #     messages.success(request, 'Successful vote! Thank you for your participation!')
            #     return redirect('polls:home')

            try:
                vote_attendee = Attendee.objects.get(email=email)
            except Attendee.DoesNotExist:
                messages.error(request, 'Login status error!')
                return redirect('polls:logout')

            if vote_attendee.vote_status < max_vote_num:

                try:
                    vote_poster = Poster.objects.get(title=poster_name)
                except Poster.DoesNotExist:
                    messages.error(request, 'This poster does not exist!')
                    return redirect('polls:home')

                # Voting
                vote_attendee.set_status()
                print(vote_attendee.vote_status)

                # Add vote
                vote_poster.increase_vote_amount()
                messages.success(request, 'Successful vote! Thank you for your participation!')

                return redirect('polls:home')

            else:

                messages.error(request, 'You have reached the maximum number (' + str(max_vote_num) + ') of votes!')
                return redirect('polls:home')

        else:

            messages.error(request, 'Staff are not allowed to vote. Please just enjoy the interesting posters.')

            return redirect('polls:home')

    else:

        messages.error(request, 'Visitors are not allowed to vote. Please login first!')

        return redirect('polls:home')


def coordinator(request):
    is_login = request.session.get("is_login", False)

    if is_login:
        position = 'coordinator'
        return render(request, 'polls/staff_coordinator.html', {
            'is_login': is_login,
            'position': position,
        })
    else:
        return redirect('polls:logout')


def down_chunk_file_manager(file_path, chuck_size=1024):
    """
    文件分片下发
    :param file_path:
    :param chuck_size:
    :return:
    """
    with open(file_path, "rb") as file:
        while True:
            chuck_stream = file.read(chuck_size)
            if chuck_stream:
                yield chuck_stream
            else:
                break


def admin(request):
    is_login = request.session.get("is_login", False)
    show_passwords = False

    if is_login:
        position = 'admin'

        navigate_type = request.POST.get('navigate', False)  # default

        if navigate_type is False:

            navigate_type = request.session.get("navigate_type", "ConferenceRule")  # default

        if navigate_type == 'ConferenceRule' or navigate_type is False:

            request.session['navigate_type'] = 'ConferenceRule'

            if request.POST.get('download', False):
                # Get staff
                download_df = pd.DataFrame(list(Staff.objects.all().values()))
                # Get Programme judge
                programme_judge_df = pd.DataFrame(list(ProgrammeJudge.objects.all().values()))[['staff_ptr_id', 'programme']]
                # Get Head judge
                head_judge_df = pd.DataFrame(list(HeadJudge.objects.all().values()))[['staff_ptr_id', 'division']]
                # Merge
                download_df = pd.merge(download_df, programme_judge_df, how='outer', left_on='id', right_on='staff_ptr_id')
                download_df = pd.merge(download_df, head_judge_df, how='outer', left_on='id', right_on='staff_ptr_id')
                download_df = download_df.drop(labels=['id', 'staff_ptr_id_x', 'staff_ptr_id_y'], axis=1)

                # File path
                save_path = os.path.join(settings.MEDIA_ROOT, 'files', 'passwords.xlsx')
                download_df.to_excel(save_path)

                # Download
                response = StreamingHttpResponse(down_chunk_file_manager(save_path))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format('passwords.xlsx')

                messages.success(request, 'Download success!')

                return response

            elif request.POST.get("new_conference", False):

                # Catch info
                conference_name = request.POST.get('name', False)
                abstract = request.POST.get('abstract', False)
                regular_judge = request.POST.get('regular_judge', False)
                head_judge = request.POST.get('head_judge', False)
                first_prize = request.POST.get('first_prize', False)
                second_prize = request.POST.get('second_prize', False)
                third_prize = request.POST.get('third_prize', False)

                # Store to DB
                new_conference = Conference(conf_date=timezone.now(), name=conference_name, abstract=abstract,
                                            programme_judge_num=regular_judge, head_judge_num=head_judge,
                                            first_prize_num=first_prize, second_prize_num=second_prize,
                                            third_prize_num=third_prize)
                new_conference.save()

                # Get uic information
                maybe_divisions = ['dst', 'dbm', 'dcc', 'dhss']
                divisions = []
                programmes = []
                for division in maybe_divisions:
                    division_programme = UICInfo.object.filter(division=division)
                    for programme in division_programme:
                        programmes.append(programme.programme)
                    if len(division_programme) > 0:
                        divisions.append(division)
                print(divisions)
                print(programmes)

                # Create the staffs' password of the newest conference
                # Programme judge(n), Head judge(n), Chairman(1), Coordinator(1), Admin(1)
                staff_number = int(new_conference.programme_judge_num) * len(programmes) + \
                               int(new_conference.head_judge_num) * len(divisions) + 1 + 1 + 1
                password_list = random.sample(range(1, 999999), staff_number)
                password_list = ['%06d' % i for i in password_list]
                password_list_index = 0

                # Clear the database of staff firstly
                Staff.objects.all().delete()

                # For programme judge
                for programme in programmes:
                    for j in range(int(new_conference.programme_judge_num)):
                        new_programme_judge = ProgrammeJudge(password=password_list[password_list_index],
                                                             position='programme_judge', programme=programme)
                        new_programme_judge.save()
                        password_list_index += 1
                # For head judge
                for division in divisions:
                    for j in range(int(new_conference.head_judge_num)):
                        new_head_judge = HeadJudge(password=password_list[password_list_index],
                                                   position='head_judge', division=division)
                        new_head_judge.save()
                        password_list_index += 1
                # For Chairman
                new_chairman = Chairman(password=password_list[password_list_index], position='chairman')
                new_chairman.save()
                password_list_index += 1
                # For Coordinator
                new_coordinator = Chairman(password=password_list[password_list_index], position='coordinator')
                new_coordinator.save()
                password_list_index += 1
                # For Admin
                new_admin = Chairman(password=password_list[password_list_index], position='admin')
                new_admin.save()
                password_list_index += 1

        elif navigate_type == 'PosterUpload':
            request.session['navigate_type'] = 'PosterUpload'

            poster_history = list(Poster.objects.all().order_by('-pub_date'))
            if len(poster_history) > 10:
                poster_history = poster_history[:10]

            return render(request, 'polls/staff_admin.html', {
                'is_login': is_login,
                'position': position,
                'show_passwords': show_passwords,
                'navigate_type': navigate_type,
                'poster_history': poster_history,
            })

        elif navigate_type == 'PosterEdit':
            request.session['navigate_type'] = 'PosterEdit'

            if request.method == 'POST':

                edit_info = request.POST.get("updateBtn", False)
                delete_info = request.POST.get("deleteBtn", False)

                if edit_info is not False:
                    # Edit mode
                    title = edit_info
                    new_author = request.POST.get("new_author")
                    new_division = request.POST.get("new_division")
                    new_programme = request.POST.get("new_programme")
                    new_abstract = request.POST.get("new_abstract")

                    edited_poster = Poster.objects.get(title=title)
                    edited_poster.author = new_author
                    edited_poster.division = new_division
                    edited_poster.programme = new_programme
                    edited_poster.abstract = new_abstract
                    edited_poster.save()

                elif delete_info is not False:
                    title = delete_info

                    deleted_poster = Poster.objects.get(title=title)
                    deleted_poster.delete()

            all_posters = Poster.objects.all()

            return render(request, 'polls/staff_admin.html', {
                'is_login': is_login,
                'position': position,
                'show_passwords': show_passwords,
                'navigate_type': navigate_type,
                'all_posters': all_posters,
            })

        return render(request, 'polls/staff_admin.html', {
            'is_login': is_login,
            'position': position,
            'show_passwords': show_passwords,
            'navigate_type': navigate_type,
        })
    else:
        return redirect('polls:logout')


def chairman(request):
    is_login = request.session.get("is_login", False)

    print('Chairman!')

    if is_login:
        position = 'chairman'

        print('Chairman!!')

        if request.method == "POST":

            print('Chairman!!!')

            # print(request.POST.get('lucky_draw', False))
            #
            # if request.POST.get('lucky_draw', False):

            print('Luck draw start!')

            # Get conference rule
            conference = Conference.objects.all().order_by('-conf_date')[0]
            first_prize_num = conference.first_prize_num
            second_prize_num = conference.second_prize_num
            third_prize_num = conference.third_prize_num

            # Copy writing
            def copy_writing(place):
                return 'Congratulations on winning the\n' + str(place) + '' \
                    ' prize,\nplease go to the staff with this email to claim the prize.'

            # Pick all voted attendee
            voted_attendee_list = list(Attendee.objects.filter(vote_status=1))

            lucky_draw_type = 0
            first_prize_attendee = None
            second_prize_attendee = None
            third_prize_attendee = None
            if len(voted_attendee_list) >= first_prize_num + second_prize_num + third_prize_num:
                lucky_draw_type = 1
                # First
                first_prize_attendee = random.sample(voted_attendee_list, first_prize_num)
                voted_attendee_list = list(set(voted_attendee_list) - set(first_prize_attendee))
                # Second
                second_prize_attendee = random.sample(voted_attendee_list, second_prize_num)
                voted_attendee_list = list(set(voted_attendee_list) - set(second_prize_attendee))
                # Third
                third_prize_attendee = random.sample(voted_attendee_list, third_prize_num)
                voted_attendee_list = list(set(voted_attendee_list) - set(third_prize_attendee))
            elif len(voted_attendee_list) >= first_prize_num + second_prize_num:
                lucky_draw_type = 2
                # First
                first_prize_attendee = random.sample(voted_attendee_list, first_prize_num)
                voted_attendee_list = list(set(voted_attendee_list) - set(first_prize_attendee))
                # Second
                second_prize_attendee = random.sample(voted_attendee_list, second_prize_num)
                voted_attendee_list = list(set(voted_attendee_list) - set(second_prize_attendee))
            elif len(voted_attendee_list) >= first_prize_num:
                lucky_draw_type = 3
                # First
                print(voted_attendee_list)
                first_prize_attendee = random.sample(voted_attendee_list, first_prize_num)
                voted_attendee_list = list(set(voted_attendee_list) - set(first_prize_attendee))
            else:
                lucky_draw_type = 4
                first_prize_attendee = voted_attendee_list

            print('lucky_draw_type', lucky_draw_type)
            # Sending out
            first_prize_emails = [attendee.email for attendee in first_prize_attendee]
            print('first_prize_emails', first_prize_emails)
            send_mail(
                'Lucky draw result',
                copy_writing('first'),
                'ugallery2022@126.com',
                first_prize_emails,
                fail_silently=False,
            )
            if lucky_draw_type == 3:
                return redirect('polls:chairman')

            second_prize_emails = [attendee.email for attendee in second_prize_attendee]
            print('second_prize_emails', second_prize_emails)
            send_mail(
                'Lucky draw result',
                copy_writing('second'),
                'ugallery2022@126.com',
                second_prize_emails,
                fail_silently=False,
            )
            if lucky_draw_type == 2:
                return redirect('polls:chairman')

            third_prize_emails = [attendee.email for attendee in third_prize_attendee]
            print('third_prize_emails', third_prize_emails)
            send_mail(
                'Lucky draw result',
                copy_writing('third'),
                'ugallery2022@126.com',
                third_prize_emails,
                fail_silently=False,
            )
            if lucky_draw_type == 1:
                return redirect('polls:chairman')

            no_prize_emails = [attendee.email for attendee in voted_attendee_list]
            print('no_prize_emails', no_prize_emails)
            send_mail(
                'Lucky draw result',
                "I'm sorry you didn't win. Thank you for your participation.",
                'ugallery2022@126.com',
                third_prize_emails,
                fail_silently=False,
            )

            return redirect('polls:chairman')

        return render(request, 'polls/staff_chairman.html', {
            'is_login': is_login,
            'position': position,
        })
    else:
        return redirect('polls:logout')


def programme_judge(request):
    is_login = request.session.get("is_login", False)

    if is_login:

        position = 'programme_judge'
        programme = request.session.get("programme", False)

        # Get Staff info
        staff_id = request.session.get("staff_id", False)
        prog_judge = ProgrammeJudge.objects.get(password=staff_id)
        score_status = prog_judge.score_status

        if programme:

            poster_list = Poster.objects.filter(programme=programme)

            if request.method == "POST":

                for poster in poster_list:
                    poster_rate = request.POST.get(poster.title, False)

                    # print(poster.title, ':', poster_rate)

                    poster.increase_rate_amount(poster_rate)

                prog_judge.finish_rating()
                messages.success(request, 'Rating success!')

                return redirect('polls:programme_judge')

            return render(request, 'polls/staff_programme_judge.html', {
                'is_login': is_login,
                'position': position,
                'programme': programme,
                'poster_list': poster_list,
                'num_poster': len(poster_list),
                'score_status': score_status,
            })

    else:
        return redirect('polls:logout')


def head_judge(request):
    # Check login status
    is_login = request.session.get("is_login", False)
    if is_login:
        position = 'head_judge'
        # Get Staff info
        staff_id = request.session.get("staff_id", False)
        head_judge_info = HeadJudge.objects.get(password=staff_id)
        score_status = head_judge_info.score_status
        # Get division
        division = request.session.get("division", False)
        if division:
            # Need division's information
            # Get programmes
            best_posters = []
            programmes = UICInfo.object.filter(division=division)
            print('Length of programme', len(programmes))
            for programme in programmes:
                # Get posters of the programme
                programme_posters = Poster.objects.filter(programme=programme.programme)
                print(
                    'Number of programme (' + str(programme.programme) + ') poster is: ' + str(len(programme_posters)))
                # Get best rate (Best poster of that programme)
                highest_rate = 0
                highest_poster = None
                for poster in programme_posters:
                    if poster.get_avg_rate():
                        if poster.get_avg_rate() > highest_rate:
                            highest_rate = poster.get_avg_rate()
                            highest_poster = poster
                    print(poster.title + str(poster.get_avg_rate()))
                if highest_poster is not None:
                    best_posters.append(highest_poster)
                    print('Best poster:' + highest_poster.title)

            poster_list = best_posters  # Pick the best

            if request.method == "POST":

                for poster in poster_list:
                    poster_ticket = request.POST.get(poster.title, False)

                    print(poster.title, ':', poster_ticket)

                    poster.increase_ticket_amount(poster_ticket)

                head_judge_info.finish_rating()
                messages.success(request, 'Rating success!')

                return redirect('polls:head_judge')

            # Check the rating status of all programme judge
            judges_finish_status = True
            for programme in programmes:
                programme_judges = ProgrammeJudge.objects.filter(programme=programme.programme)
                for judge in programme_judges:
                    if judge.score_status == 0:
                        judges_finish_status = False

            return render(request, 'polls/staff_head_judge.html', {
                'is_login': is_login,
                'position': position,
                'division': division,
                'poster_list': poster_list,
                'num_poster': len(poster_list),
                'judges_finish_status': judges_finish_status,
                'score_status': score_status,
            })
    else:
        return redirect('polls:logout')


def upload_action(request):

    request.session['navigate_type'] = 'PosterUpload'

    if request.method == 'POST':

        # Catch info
        file = request.FILES['poster']
        file_type = file.name.split('.')[-1]
        file_name = request.POST['title'] + '.' + file_type

        title = request.POST['title']
        author = request.POST['author']
        programme = request.POST['programme'].lower()
        division = request.POST['division'].lower()
        abstract = request.POST['abstract']

        exist_poster = Poster.objects.filter(title=title)

        if exist_poster:

            messages.error(request, "This name is already in use, please change it")

            redirect('polls:myadmin')

        if file_type == 'jpg':

            # Create save path
            save_path = os.path.join(settings.MEDIA_ROOT, 'images', file_name)

            # Saving the file
            with open(save_path, 'wb') as f:
                for content in file.chunks():
                    f.write(content)

            # Catch image info
            im = Image.open(file)
            width = im.size[0]
            height = im.size[1]

            # Save into Database
            new_poster = Poster(title=title,
                                author=author,
                                programme=programme,
                                division=division,
                                abstract=abstract,
                                file_name=file_name,
                                file_width=width,
                                file_height=height,
                                file_path=os.path.join('media', 'images', file_name),
                                pub_date=timezone.now(),
                                )
            new_poster.save()

            return redirect('polls:myadmin')

        else:

            messages.error(request, "Error upload file type!")

            return redirect('polls:myadmin')

    else:

        messages.error(request, "The form you submitted is missing information!")

        return redirect('polls:myadmin')


def detail(request, poster_name):
    is_login = request.session.get("is_login", False)
    email = request.session.get("email", False)

    poster = Poster.objects.get(title=poster_name)

    return render(request, 'polls/detail.html', {
        'is_login': is_login,
        'poster': poster,
        'email': email,
    })


def best(request):
    is_login = request.session.get("is_login", False)
    email = request.session.get("email", False)

    all_head_judge = HeadJudge.objects.all()
    all_finished = 1
    for judge in all_head_judge:
        if judge.score_status == 0:
            all_finished = 0
            break
    best_posters = []
    if all_finished:
        maybe_divisions = ['dst', 'dbm', 'dcc', 'dhss']
        for division in maybe_divisions:
            division_posters = list(Poster.objects.filter(division=division).order_by('-total_ticket'))
            if len(division_posters) > 0:
                best_posters.append(division_posters[0])
    if len(best_posters) < 1:
        all_finished = 0

    return render(request, 'polls/poster_best.html', {
        'is_login': is_login,
        'all_finished': all_finished,
        'best_posters': best_posters,
        'email': email,
    })


def popular(request):
    is_login = request.session.get("is_login", False)
    email = request.session.get("email", False)

    popular_poster = Poster.objects.all().order_by('-votes')

    if len(popular_poster) > 10:
        popular_poster = popular_poster[:10]

    poster_index = 1
    for poster in popular_poster:
        poster.ranking = poster_index
        poster_index += 1

    return render(request, 'polls/poster_popular.html', {
        'is_login': is_login,
        'popular_poster': popular_poster,
        'email': email,
    })


def download(request, poster_name):
    is_login = request.session.get("is_login", False)

    if is_login:

        poster = Poster.objects.get(title=poster_name)

        poster_full_name = str(poster_name) + '.jpg'

        if poster:
            # File path
            save_path = os.path.join(settings.MEDIA_ROOT, 'images', poster_full_name)

            # Download
            response = StreamingHttpResponse(down_chunk_file_manager(save_path))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(poster_full_name)

            return response

        else:

            return redirect('polls:home')

    else:

        messages.error(request, 'Please login first!')

        return redirect('polls:home')
