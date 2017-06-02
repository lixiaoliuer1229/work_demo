from .models import Teacher,Class,Student,Lesson,Class_m2m_Lesson,Study_record,class_m2m_student

class  Teacher_Center(object):
    "讲师视图"
    def __init__(self,session):
        self.session = session
        self.authentication()
        self.handler()

    def handler(self):
        while True:
            print('''\n\33[35;1m———欢迎来【%s】进入讲师管理系统————\33[0m \n
        \33[34;0mshow_classes 显示可管理的班级
        add_class 创建班级
        add_student 添加学员
        add_lesson 添加课程节次
        add_studyrecord 创建上课记录
        modify_scores 修改学员成绩
        exit 退出管理系统
        \33[0m''' % self.teacher_obj.teacher_name)
            user_func = input("\033[34;0m请输入进行操作的命令:\033[0m").strip()
            if hasattr(self, user_func):
                getattr(self, user_func)()


    def authentication(self):
        '''认证'''
        while True:
            teacher_name = input("\033[34;0m请输入讲师名:\033[0m").strip()
            self.teacher_obj = self.session.query(Teacher).filter_by(teacher_name=teacher_name).first()
            if not self.teacher_obj:
                print("\33[31;1m输入错误：请输入有效的讲师名\33[0m")
                continue
            else:
                #print(self.teacher_obj)
                break


    def add_class(self):
        '''创建班级'''
        class_name = input("\033[34;0m请输入创建班级的名称:\033[0m")
        course = input("\033[34;0m请输入创建班级的类型:\033[0m")
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()
        if not class_obj:
            class_new = Class(class_name=class_name,course=course)
            self.teacher_obj.classes.append(class_new)
            self.session.add(class_new)
            self.session.commit()
            print("\033[34;1m班级创建成功\033[0m")
        else:
            print("\33[31;1m系统错误：班级已经存在\33[0m")


    def show_classes(self):
        '''查看所有的班级'''
        print(self.teacher_obj)
        for class_obj in self.teacher_obj.classes:
            print("讲师：【%s】\t班级：【%s】\t类型：【%s】" % (class_obj.teachers[0].teacher_name,
                                                 class_obj.class_name,class_obj.course))


    def add_student(self):
        '''添加学员'''
        class_name = input("\033[34;0m请输入要添加学员的班级名:\033[0m")
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()

        if class_obj and class_obj.teachers[0] == self.teacher_obj:
            stu_name = input("\033[34;0m请输入学员的姓名:\033[0m")
            QQ = input("\033[34;0m请输入学员的QQ号:\033[0m")
            student_obj = self.session.query(Student).filter_by(QQ = QQ).first()

            if student_obj:
                if student_obj.stu_name not in class_obj.students:
                    class_obj.students.append(student_obj)
                    self.session.add(class_obj)
                    self.session.commit()
                    print("\033[34;1m学员添加成功\033[0m")
                else:
                    print("\33[31;1m系统错误：学员已经存在此班中\33[0m")

            elif not student_obj:
                student_new = Student(stu_name=stu_name, QQ=QQ)
                class_obj.students.append(student_new)
                self.session.add(student_new)
                self.session.commit()
                print("\033[34;1m学员添加成功\033[0m")
            else:
                print("\33[31;1m系统错误：学员已经存在\33[0m")
        else:
            print("\33[31;1m输入错误：班级不存在或没有权限管理此班级\33[0m")


    def add_lesson(self):
        '''添加课程节次'''
        class_name = input("\033[34;0m请输入要添加lesson的班级名:\033[0m")
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()

        if class_obj and class_obj.teachers[0] == self.teacher_obj:     #输入的班级名存在且在属于当前老师管理
            lesson_name = input("\033[34;0m请输入添加的lesson名（类day1）:\033[0m")
            lesson_obj = self.session.query(Lesson).filter_by(lesson_name=lesson_name).first()
            if not lesson_obj:                                          #输入的lesson名字不存在
                print("lesson  不存在")
                lesson_obj = Lesson(lesson_name=lesson_name)                #增加lesson表数据
                self.session.add(lesson_obj)
                self.session.commit()

            rest = self.session.query(Class_m2m_Lesson).filter(Class_m2m_Lesson.class_id==class_obj.class_id).\
                filter(Class_m2m_Lesson.lesson_id==lesson_obj.lesson_id).first()
            if not rest:                                                #如果class_m2m_lesson没有存储班级和课节的对应关系
                print("class:%s----lesson:%s"%(class_obj.class_id,lesson_obj.lesson_id))
                class_m2m_lesson_new = Class_m2m_Lesson(class_id=class_obj.class_id,lesson_id=lesson_obj.lesson_id)
                self.session.add(class_m2m_lesson_new)                  #创建class_m2m_lesson对应关系
                self.session.commit()

        else:
            print("\33[31;1m输入错误：班级不存在或没有权限管理此班级\33[0m")


    def add_studyrecord(self):
        '''添加学习记录'''
        class_name = input("\033[34;0m请输入要添加学习记录的班级名:\033[0m")
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()

        if class_obj and class_obj.teachers[0] == self.teacher_obj:  # 输入的班级名存在且在属于当前老师管理
            lesson_name = input("\033[34;0m请输入添加学习记录的课节名（lesson）:\033[0m")
            lesson_obj = self.session.query(Lesson).filter_by(lesson_name=lesson_name).first()
            if lesson_obj:                                       # 输入的lesson名字存在
                class_m2m_lesson_obj = self.session.query(Class_m2m_Lesson).filter(Class_m2m_Lesson.class_id == class_obj.class_id). \
                    filter(Class_m2m_Lesson.lesson_id == lesson_obj.lesson_id).first()
                if class_m2m_lesson_obj:                                            # 班级对应的课lesson表数据存在

                    study_record_obj = self.session.query(Study_record).filter_by(class_m2m_lesson_id=class_m2m_lesson_obj.id).first()
                    if not study_record_obj:                                                    # 上课记录为创建
                        for student_obj in class_obj.students:
                            status = input("输入学生 %s 的上课状态（yes/no）："%student_obj.stu_name)
                            study_record_new = Study_record(class_m2m_lesson_id=class_m2m_lesson_obj.id,
                                                            stu_id=student_obj.stu_id,
                                                            status=status)
                            self.session.add(study_record_new)
                            self.session.commit()
                    else:
                        print("\33[31;1m系统错误：当前上课记录已经创建\33[0m")
                else:
                     print("\33[31;1m系统错误：当前班级的lesson课节未创建\33[0m")
            else:
                print("\33[31;1m系统错误：lesson未创建\33[0m")
        else:
            print("\33[31;1m输入错误：班级不存在或没有权限管理此班级\33[0m")


    def modify_scores(self):
        '''修改成绩'''
        class_name = input("\033[34;0m请输入学习记录的班级名:\033[0m")
        class_obj = self.session.query(Class).filter_by(class_name=class_name).first()

        if class_obj and class_obj.teachers[0] == self.teacher_obj:  # 输入的班级名存在且在属于当前老师管理
            lesson_name = input("\033[34;0m请输入学习记录的课节名（lesson）:\033[0m")
            lesson_obj = self.session.query(Lesson).filter_by(lesson_name=lesson_name).first()

            if lesson_obj:  # 输入的lesson名字存在
                class_m2m_lesson_obj = self.session.query(Class_m2m_Lesson).filter(
                    Class_m2m_Lesson.class_id == class_obj.class_id). \
                    filter(Class_m2m_Lesson.lesson_id == lesson_obj.lesson_id).first()

                if class_m2m_lesson_obj:  # 班级对应的课lesson表数据存在
                    while True:
                        study_record_objs = self.session.query(Study_record).filter(
                                Study_record.class_m2m_lesson_id==class_m2m_lesson_obj.id).all()
                        for obj in  study_record_objs:
                            print(obj)

                        student_name = input("\033[34;0m输入要修改成绩的学生名：[Q 退出]\33[0m")
                        if student_name == "q" or student_name == "Q":break
                        student_obj = self.session.query(Student).filter_by(stu_name=student_name).first()
                        if student_obj:
                            study_record_obj = self.session.query(Study_record).filter(
                                Study_record.class_m2m_lesson_id==class_m2m_lesson_obj.id).filter(
                                Study_record.stu_id == student_obj.stu_id).first()

                            if study_record_obj:                            # 上课记录存在
                                score = input("\033[34;0m输入修改后的成绩\33[0m")
                                study_record_obj.score= score
                                self.session.commit()

                    else:
                        print("\33[31;1m系统错误：当前上课记录已经创建\33[0m")
                else:
                    print("\33[31;1m系统错误：当前班级的lesson课节未创建\33[0m")
            else:
                print("\33[31;1m系统错误：lesson未创建\33[0m")
        else:
            print("\33[31;1m输入错误：班级不存在或没有权限管理此班级\33[0m")


    def exit(self):
        exit()










