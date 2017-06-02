from sqlalchemy import desc
from .models import Teacher,Class,Student,Lesson,Class_m2m_Lesson,Study_record
import random

class  Student_Center(object):
    "学生视图"
    def __init__(self,session):
        self.session = session
        self.authentication()
        self.handler()

    def handler(self):
        while True:
            print('''\n\33[35;1m———欢迎来【%s】进入学员管理系统————\33[0m \n
            \33[34;0mup_homework 上传作业
            show_homework 查看作业成绩
            show_rank 查看班级排名
            exit 退出管理系统
            \33[0m''' % self.student_obj.stu_name)
            user_func = input("\033[34;0m请输入进行操作的命令:\033[0m").strip()
            if hasattr(self, user_func):
                getattr(self, user_func)()

    def authentication(self):
        '''认证'''
        while True:
            student_name = input("\033[34;0m请输入学生名:\033[0m").strip()
            self.student_obj = self.session.query(Student).filter_by(stu_name=student_name).first()
            if not self.student_obj:
                print("\33[31;1m输入错误：请输入有效的学生名\33[0m")
                continue
            else:
                # print(self.teacher_obj)
                break

    def up_homework(self):
        "上传作业"
        class_name = input("\033[34;0m请输入班级名:\033[0m")

        for class_obj in self.student_obj.classes:
            print(class_obj.class_name)
            if class_name == class_obj.class_name:
                lesson_name = input("\033[34;0m请输入的课节名（lesson）:\033[0m")
                lesson_obj = self.session.query(Lesson).filter_by(lesson_name=lesson_name).first()

                if lesson_obj:  # 输入的lesson名字存在
                    class_m2m_lesson_obj = self.session.query(Class_m2m_Lesson).filter(
                        Class_m2m_Lesson.class_id == class_obj.class_id). \
                        filter(Class_m2m_Lesson.lesson_id == lesson_obj.lesson_id).first()
                    if class_m2m_lesson_obj:  # 班级对应的课lesson表数据存在
                        study_record_obj = self.session.query(Study_record).filter(
                            Study_record.class_m2m_lesson_id == class_m2m_lesson_obj.id).filter(
                            Study_record.stu_id == self.student_obj.stu_id).first()

                        if study_record_obj:  # 上课记录存在
                            score = random.randint(10,100)
                            study_record_obj.score = score
                            self.session.commit()
                            print("上传成功")
                        else:
                            print("\33[31;1m系统错误：当前上课记录已经创建\33[0m")
                else:
                    print("\33[31;1m系统错误：lesson未创建\33[0m")

    def show_homework(self):
        '''查看作业成绩'''
        class_name = input("\033[34;0m请输入学习记录的班级名:\033[0m")
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()

        if class_obj:
            lesson_name = input("\033[34;0m请输入学习记录的课节名（lesson）:\033[0m")
            lesson_obj = self.session.query(Lesson).filter_by(lesson_name=lesson_name).first()

            if lesson_obj:  # 输入的lesson名字存在
                class_m2m_lesson_obj = self.session.query(Class_m2m_Lesson).filter(
                    Class_m2m_Lesson.class_id == class_obj.class_id). \
                    filter(Class_m2m_Lesson.lesson_id == lesson_obj.lesson_id).first()

                if class_m2m_lesson_obj:  # 班级对应的课lesson表数据存在
                    study_record_objs = self.session.query(Study_record).filter(
                        Study_record.class_m2m_lesson_id == class_m2m_lesson_obj.id).all()
                    for obj in study_record_objs:
                        if obj.stu_id == self.student_obj.stu_id:
                            print(obj)

    def show_rank(self):
        '''查看排名'''

        class_name = input("\033[34;0m请输入学习记录的班级名:\033[0m")
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()

        if class_obj:
            lesson_name = input("\033[34;0m请输入学习记录的课节名（lesson）:\033[0m")
            lesson_obj = self.session.query(Lesson).filter_by(lesson_name=lesson_name).first()

            if lesson_obj:  # 输入的lesson名字存在
                class_m2m_lesson_obj = self.session.query(Class_m2m_Lesson).filter(
                    Class_m2m_Lesson.class_id == class_obj.class_id). \
                    filter(Class_m2m_Lesson.lesson_id == lesson_obj.lesson_id).first()

                if class_m2m_lesson_obj:  # 班级对应的课lesson表数据存在
                    score_rank_obj = self.session.query(Study_record).order_by(desc(Study_record.score))
                    for obj in score_rank_obj:
                        if obj.class_m2m_lesson_id == class_m2m_lesson_obj.id:
                            print(obj)
