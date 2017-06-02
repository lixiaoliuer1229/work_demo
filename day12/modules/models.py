from sqlalchemy import create_engine,Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey,Table
from sqlalchemy.orm import relationship


############创建数据表结构######################3
# 创建实例，并连接work库
engine = create_engine("mysql+pymysql://root:@localhost/home_work?charset=utf8")
Base = declarative_base()  # 生成orm基类

# 班级与讲师的对应关系表
teacher_m2m_class = Table("teacher_m2m_class",Base.metadata,
                          Column("teacher_id", Integer, ForeignKey("teacher.teacher_id")),
                          Column("class_id", Integer, ForeignKey("class.class_id")),
                          )

# 班级与学生的对应关系表
class_m2m_student = Table("class_m2m_student",Base.metadata,
                          Column("class_id",Integer,ForeignKey("class.class_id")),
                          Column("stu_id", Integer, ForeignKey("student.stu_id")),
                          )

class Class_m2m_Lesson(Base):
    '''班级和课节对应表'''
    __tablename__ = "class_m2m_lesson"
    id =  Column(Integer, primary_key=True)
    class_id = Column(Integer,ForeignKey("class.class_id"))
    lesson_id = Column(Integer, ForeignKey("lesson.lesson_id"))

    classes = relationship("Class",backref="class_m2m_lessons")
    lessons = relationship("Lesson", backref="class_m2m_lessons")

    def __repr__(self):
        return "%s %s" % (self.classes,self.lessons)

class Study_record(Base):
    "上课记录"
    __tablename__ = "study_record"
    id = Column(Integer,primary_key=True)
    class_m2m_lesson_id = Column(Integer,ForeignKey("class_m2m_lesson.id"))
    stu_id = Column(Integer, ForeignKey("student.stu_id"))
    status = Column(String(32),nullable=False)
    score = Column(Integer,nullable=True)

    class_m2m_lessons = relationship("Class_m2m_Lesson",backref="my_study_record")
    students = relationship("Student", backref="my_study_record")

    def __repr__(self):
       return  "\033[35;0m%s,%s,状态：【%s】,成绩：【%s】\33[0m"%(self.class_m2m_lessons,self.students,self.status,self.score)

class Teacher(Base):
    "讲师"
    __tablename__ = "teacher"
    teacher_id = Column(Integer, primary_key=True)
    teacher_name = Column(String(32), nullable=False, unique=True)   #唯一

    classes = relationship("Class", secondary=teacher_m2m_class, backref="teachers")

    def __repr__(self):
        return "讲师：【%s】"%self.teacher_name

class Class(Base):
    "班级"
    __tablename__ ="class"
    class_id = Column(Integer, primary_key=True)
    class_name = Column(String(32), nullable=False,unique=True)
    course =  Column(String(32), nullable=False)

    students = relationship("Student",secondary=class_m2m_student,backref="classes")

    def __repr__(self):
        return "班级名：【%s】"%self.class_name

class Student(Base):
    "学生"
    __tablename__ ="student"
    stu_id = Column(Integer, primary_key=True)
    stu_name = Column(String(32), nullable=False, unique=True)
    QQ =  Column(Integer(), nullable=False)

    def __repr__(self):
        return "学生名：【%s】"%self.stu_name

class Lesson(Base):
    "课节"
    __tablename__ = "lesson"
    lesson_id = Column(Integer, primary_key=True)
    lesson_name = Column(String(32), nullable=False, unique=True)

    def __repr__(self):
        return "节次名：【%s】"%self.lesson_name


Base.metadata.create_all(engine)

