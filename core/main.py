import asyncio
import os

from core.formatters import TeacherFormatter, FacultyFormatter
from core.json_handler import JsonHandler
from core.requests import CHMNUScheduleRequestBot


async def upload_teachers(api: CHMNUScheduleRequestBot) -> None:
    teachers = JsonHandler.convert_from_json_to_py_obj_file(path_to_file='../fixtures/teachers_2023_1_sem.json')
    formatted_teachers = TeacherFormatter().format_list(teachers)

    tasks = [
        api.create_teacher(
            first_name=teacher['first_name'],
            last_name=teacher['last_name'],
            middle_name=teacher['middle_name'],
            rank='lecturer'
        )
        for teacher in formatted_teachers
    ]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        print(response)


async def upload_subjects(api: CHMNUScheduleRequestBot) -> None:
    subjects = JsonHandler.convert_from_json_to_py_obj_file(path_to_file='../fixtures/subjects_2023_1_sem.json')
    tasks = [
        api.create_subject(subject=subject)
        for subject in subjects
    ]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        print(response)


async def upload_faculties(api: CHMNUScheduleRequestBot) -> None:
    faculties = JsonHandler.convert_from_json_to_py_obj_file(path_to_file='../fixtures/faculty_2024_1_sem.json')
    formatted_faculties = FacultyFormatter().format_list(faculties)
    tasks = [
        api.create_faculty(
            name=faculty['name'],
            code_name=faculty['code_name'],
        )
        for faculty in formatted_faculties
    ]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        print(response)

if __name__ == "__main__":
    bot = CHMNUScheduleRequestBot(protocol='http', domain='localhost', api_version='v1')
    access_token, refresh_token = asyncio.run(
        bot.login(
            email=os.getenv('ADMIN_EMAIL'),
            password=os.getenv('ADMIN_PASSWORD')
        )
    )
    bot.access_token = access_token
    asyncio.run(upload_faculties(bot))
