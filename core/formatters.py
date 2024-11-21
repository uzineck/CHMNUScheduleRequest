from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class BaseFormatter(ABC):
    @abstractmethod
    def format_dict(self, value: dict) -> dict[Any, Any]:
        ...

    @abstractmethod
    def format_list(self, list_value: list) -> list[Any]:
        ...


class TeacherFormatter(BaseFormatter):
    def format_dict(self, value: dict) -> dict[Any, Any]:
        raise NotImplemented

    def format_list(self, list_value: list[str]) -> list[Any]:
        formatted_teacher_list = []
        for teacher in list_value:
            formatted_teacher_dict = {}
            teacher = teacher.replace(" ", "")
            teacher_left_side = teacher.split('.')[0]
            teacher_first_name = teacher_left_side[-1]
            teacher_last_name = teacher_left_side[:-1]
            teacher_middle_name = teacher.split('.')[1]
            formatted_teacher_dict["first_name"] = teacher_first_name + '.'
            formatted_teacher_dict["last_name"] = teacher_last_name
            formatted_teacher_dict["middle_name"] = teacher_middle_name + '.'
            formatted_teacher_list.append(formatted_teacher_dict)
        return formatted_teacher_list


class FacultyFormatter(BaseFormatter):
    def format_dict(self, value: dict) -> dict[Any, Any]:
        ...

    def format_list(self, list_value: list[str]) -> list[Any]:
        formatted_faculty_list = []
        for faculty in list_value:
            formatted_faculty_dict = {}
            words = faculty.split(' ')
            first_word_parts = words[0].split('-')
            if len(first_word_parts) == 2:
                first_letter = first_word_parts[0][0].upper() + first_word_parts[1][0].upper()
            else:
                first_letter = words[0][0].upper()
            code_name = first_letter + ''.join(name[0].upper() for name in words[1:])
            # first_word = faculty.split('-')
            # first_letter = first_word[0][0].upper()
            # code_name = first_letter + ''.join(name[0].upper() for name in first_word[1].split(' '))
            formatted_faculty_dict["name"] = faculty
            formatted_faculty_dict["code_name"] = code_name
            formatted_faculty_list.append(formatted_faculty_dict)
        return formatted_faculty_list
