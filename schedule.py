import re
from datetime import date

import requests
import pandas as pd


class Schedule:
    def __init__(self):
        self.URL_ONLINE = "https://www.avalon.ru/retraining/groupschedule/21246/"
        self.URL_OFFLINE = "https://www.avalon.ru/retraining/groupschedule/21245/"
        self.df = None

    @staticmethod
    def is_actual(scheduled):
        m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", scheduled)
        scheduled_date = date(*map(int, reversed(m.groups())))
        return scheduled_date >= date.today()

    @staticmethod
    def cut_to_space(full_name):
        return full_name.split()[0]

    @staticmethod
    def cut_to_dot(full_sub):
        return full_sub.split(".")[0]

    @staticmethod
    def type_cut(val):
        if "Лекция" in val:
            return "Л"
        elif "Практика" in val:
            return "П"
        else:
            return "пр."

    def rename_columns(self):
        new_columns = {
            "Дата занятия": "Дата",
            "Время занятия": "Время",
            "Программа/дисциплина": "Курс"
        }
        self.df.rename(columns=new_columns, inplace=True)

    def cut_content(self):
        self.df = self.df[self.df["Дата"].apply(self.is_actual)]
        self.df["Дата"] = self.df["Дата"].apply(self.cut_to_space)
        self.df["Преподаватель"] = self.df["Преподаватель"].apply(self.cut_to_space)
        self.df["Курс"] = self.df["Курс"].apply(self.cut_to_dot)
        self.df["Время"] = self.df["Время"].apply(self.cut_to_space)
        self.df["Занятие"] = self.df["Занятие"].apply(self.type_cut)

    def cut_room(self):
        self.df = self.df.drop(columns=["Аудитория"])
        self.df.reset_index(drop=True, inplace=True)

    def get(self, limit=5):
        responce = requests.get(url=self.URL_ONLINE)
        self.df = pd.read_html(responce.content)[0]
        self.rename_columns()
        self.cut_content()
        self.cut_room()
        return self.df.head(limit).to_string(index=False, header=False)

    def get_room(self):
        responce = requests.get(url=self.URL_ONLINE)
        self.df = pd.read_html(responce.content)[0]
        self.rename_columns()
        self.cut_content()
        next_lecture = self.df.head(1)
        next_date = next_lecture["Дата"].to_string(index=False)
        next_room = next_lecture["Аудитория"].to_string(index=False)
        if next_room != "_Онлайн":
            next_room = "в аудитории " + next_room
        return f"Следующее занятие пройдет {next_date} {next_room}"


if __name__ == "__main__":
    schedule = Schedule()
    print(schedule.get_room())

