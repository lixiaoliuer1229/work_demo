from sqlalchemy.orm import sessionmaker
from .models import Teacher,Class
from .teacher_center import Teacher_Center
from .student_center import Student_Center
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:@localhost/work?charset=utf8")

class Action(object):
    "管理视图"
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.initialize_database()

    def func(self):
        while True:
            print('''\n\33[35;1m———欢迎来到选课系统————\33[0m \n
        \33[34;0m1.讲师视图
        2.学员视图
        q.退出
        \33[0m''')
            user_choice = input("\033[34;0m请输入你进入的视图:\033[0m")
            if user_choice == '1':
                Teacher_Center(self.session)
            elif user_choice == '2':
                Student_Center(self.session)
            elif user_choice == 'q':
                print("\033[34;1m感谢使用管理系统,退出\033[0m")
                break
            else:
                print("\033[31;1m请输入正确的选项\033[0m")

    def initialize_database(self):
        '''初始化数据库'''
        rest = self.session.query(Teacher).filter(Teacher.teacher_id>0).all()
        if not rest:
            class1 = Class(class_name="S14", course="Python")
            teacher1 = Teacher(teacher_name="Alex")
            teacher1.classes = [class1]

            self.session.add_all([class1,  teacher1])
            self.session.commit()
















