import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

# 模拟数据库操作类
class Database:
    def __init__(self):
        self.data_file = "students.json"
        try:
            with open(self.data_file, "r") as file:
                self.students = json.load(file)
        except FileNotFoundError:
            self.students = []

    def insert(self, student):
        self.students.append(student)

    def all(self):
        return self.students

    def save_data(self):
        with open(self.data_file, "w") as file:
            json.dump(self.students, file)

    def delete_by_name(self, name):
        for student in self.students:
            if student["name"] == name:
                self.students.remove(student)
                return True
        return False

    def search_by_name(self, name):
        for student in self.students:
            if student["name"] == name:
                return student
        return None

    def update(self, stu):
        for i, student in enumerate(self.students):
            if student["name"] == stu["name"]:
                self.students[i] = stu
                return True
        return False

# 登录页面类
class LoginPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.create_page()

    def create_page(self):
        root.title("欢迎进入学生成绩管理系统")
        self.root.geometry('%dx%d' % (500, 300))
        tk.Label(self).grid(row=0, stick=tk.W)
        tk.Label(self, text='账户: ').grid(row=1, stick=tk.W, pady=10)
        tk.Entry(self, textvariable=self.username).grid(row=1, column=1, stick=tk.E)
        tk.Label(self, text='密码: ').grid(row=2, stick=tk.W, pady=10)
        tk.Entry(self, textvariable=self.password, show='*').grid(row=2, column=1, stick=tk.E)
        tk.Button(self, text='登陆', command=self.login_check).grid(row=3, stick=tk.W, pady=10)
        tk.Button(self, text='退出', command=self.quit).grid(row=3, column=1, stick=tk.E)

    def login_check(self):
        name = self.username.get()
        password = self.password.get()
        if name == 'admin' and password == '123':
            self.pack_forget()
            MenuPage(self.master).pack()
        else:
            messagebox.showinfo(title='错误', message='账号或密码错误！')

# 主菜单页面类
class MenuPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.create_page()

    def create_page(self):
        self.root.geometry('%dx%d' % (500, 300))
        tk.Button(self, text='保存信息', command=self.save_data).pack()
        tk.Button(self, text='录入学生成绩', command=self.open_input_frame).pack()
        tk.Button(self, text='查询学生成绩', command=self.open_query_frame).pack()
        tk.Button(self, text='修改学生成绩', command=self.open_update_frame).pack()
        tk.Button(self, text='删除学生成绩', command=self.open_delete_frame).pack()

    def save_data(self):
        db.save_data()
        messagebox.showinfo(title='信息', message='数据已保存！')
    def open_input_frame(self):
        self.pack_forget()
        InputFrame(self.master).pack()

    def open_query_frame(self):
        self.pack_forget()
        QueryFrame(self.master).pack()

    def open_update_frame(self):
        self.pack_forget()
        UpdateFrame(self.master).pack()

    def open_delete_frame(self):
        self.pack_forget()
        DeleteFrame(self.master).pack()

# 录入成绩页面类
class InputFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.name = tk.StringVar()
        self.math = tk.StringVar()
        self.chinese = tk.StringVar()
        self.english = tk.StringVar()
        self.status = tk.StringVar()
        self.create_page()


    def create_page(self):
        self.root.geometry('%dx%d' % (500, 300))
        tk.Label(self).grid(row=0, stick=tk.W, pady=10)
        tk.Label(self, text="姓名:").grid(row=1, stick=tk.W, pady=10)
        tk.Entry(self, textvariable=self.name).grid(row=1, column=1, stick=tk.E)
        tk.Label(self, text="数学成绩:").grid(row=2, stick=tk.W, pady=10)
        tk.Entry(self, textvariable=self.math).grid(row=2, column=1, stick=tk.E)
        tk.Label(self, text="语文成绩:").grid(row=3, stick=tk.W, pady=10)
        tk.Entry(self, textvariable=self.chinese).grid(row=3, column=1, stick=tk.E)
        tk.Label(self, text="英语成绩:").grid(row=4, stick=tk.W, pady=10)
        tk.Entry(self, textvariable=self.english).grid(row=4, column=1, stick=tk.E)
        tk.Button(self, text="录入", command=self.record_student).grid(row=5, column=0, stick=tk.E, pady=10)
        tk.Label(self, textvariable=self.status).grid(row=6, column=1, stick=tk.E, pady=10)
        tk.Button(self, text="返回主菜单", command=self.return_to_menu).grid(row=5, column=1, stick=tk.E, pady=10)

    def return_to_menu(self):
        self.pack_forget()
        MenuPage(self.root).pack()

    def record_student(self):
        name = self.name.get()
        math = self.math.get()
        chinese = self.chinese.get()
        english = self.english.get()

        # 数据验证，确保成绩为数字
        if not (math.isdigit() and chinese.isdigit() and english.isdigit()):
            messagebox.showinfo(title='错误', message='成绩必须为数字！')
            return

        student = {
            "name": name,
            "math": int(math),
            "chinese": int(chinese),
            "english": int(english),
        }
        db.insert(student)
        self.status.set("插入数据成功！")
        self.clear_data()
        db.save_data()

    def clear_data(self):
        self.name.set("")
        self.math.set("")
        self.chinese.set("")
        self.english.set("")

# 查询成绩页面类
class QueryFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.create_page()

    def create_page(self):
        self.root.geometry('%dx%d' % (500, 300))
        self.create_tree_view()
        self.show_data_frame()
        tk.Button(self, text="刷新数据", command=self.show_data_frame).pack(anchor=tk.E, pady=5)
        tk.Button(self, text="返回主菜单", command=self.return_to_menu).pack(anchor=tk.W, pady=5)

    def return_to_menu(self):
        self.pack_forget()
        MenuPage(self.root).pack()

    def create_tree_view(self):
        columns = ("name", "chinese", "math", "english")
        self.tree_view = ttk.Treeview(self, show='headings', columns=columns)
        self.tree_view.column("name", width=80, anchor='center')
        self.tree_view.column("chinese", width=80, anchor='center')
        self.tree_view.column("math", width=80, anchor='center')
        self.tree_view.column("english", width=80, anchor='center')
        self.tree_view.heading("name", text='姓名')
        self.tree_view.heading("chinese", text='语文')
        self.tree_view.heading("math", text='数学')
        self.tree_view.heading("english", text='英语')
        self.tree_view.pack()

    def show_data_frame(self):
        for _ in map(self.tree_view.delete, self.tree_view.get_children("")):
            pass
        students = db.all()
        for index, stu in enumerate(students):
            self.tree_view.insert('', index, values=(stu["name"], stu["chinese"], stu["math"], stu["english"]))

# 删除成绩页面类
class DeleteFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.status = tk.StringVar()
        self.de_name = tk.StringVar()
        self.create_page()

    def create_page(self):
        self.root.geometry('%dx%d' % (500, 300))
        tk.Label(self).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(self, text='删除数据').grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=10)
        tk.Label(self, text="根据姓名删除信息").grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
        e1 = tk.Entry(self, textvariable=self.de_name)
        e1.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        tk.Button(self, text='删除', command=self.delete_student).grid(row=3, column=1, padx=10, pady=5,sticky=tk.E)
        tk.Label(self, textvariable=self.status).grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        tk.Button(self, text="返回主菜单", command=self.return_to_menu).grid(row=5, column=0, columnspan=2, pady=10,sticky=tk.W + tk.E)

    def return_to_menu(self):
        self.pack_forget()
        MenuPage(self.root).pack()

    def delete_student(self):
        name = self.de_name.get()
        if not name:
            messagebox.showinfo(title='错误', message='请输入学生姓名！')
            return
        result = db.delete_by_name(name)
        if result:
            self.status.set(f'{name}已经被删')
            self.de_name.set("")
        else:
            self.status.set(f'{name}不存在')

# 修改成绩页面类
class UpdateFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master
        self.name = tk.StringVar()
        self.math = tk.StringVar()
        self.chinese = tk.StringVar()
        self.english = tk.StringVar()
        self.status = tk.StringVar()
        self.create_page()

    def create_page(self):
        self.root.geometry('%dx%d' % (500, 300))
        tk.Label(self).grid(row=0, stick=tk.W, pady=10)
        tk.Label(self, text="姓名:").grid(row=1, stick=tk.W, pady=10)
        tk.Entry(self, textvariable=self.name).grid(row=1, column=1, stick=tk.E)
        tk.Label(self, text="数学:").grid(row=2, stick=tk.W, pady=10)
        tk.Entry(self, textvariable=self.math).grid(row=2, column=1, stick=tk.E)
        tk.Label(self, text="语文:").grid(row=3, stick=tk.W, pady=10)
        tk.Entry(self, textvariable=self.chinese).grid(row=3, column=1, stick=tk.E)
        tk.Label(self, text="英语:").grid(row=4, stick=tk.W, pady=10)
        tk.Entry(self, textvariable=self.english).grid(row=4, column=1, stick=tk.E)
        tk.Button(self, text='查询', command=self.search_student).grid(row=6, column=0, stick=tk.W, pady=10)
        tk.Button(self, text='修改', command=self.change_student).grid(row=6, column=0, stick=tk.E, pady=10)
        tk.Label(self, textvariable=self.status).grid(row=7, column=1, stick=tk.E, pady=10)
        tk.Button(self, text="返回主菜单", command=self.return_to_menu).grid(row=6, column=1, stick=tk.E, pady=10)

    def return_to_menu(self):
        self.pack_forget()
        MenuPage(self.root).pack()

    def search_student(self):
        name = self.name.get()
        if not name:
            messagebox.showinfo(title='错误', message='请输入学生姓名！')
            return
        student = db.search_by_name(name)
        if student:
            self.math.set(student["math"])
            self.chinese.set(student["chinese"])
            self.english.set(student["english"])
            self.status.set(f'查询到{name}同学的信息')
        else:
            self.status.set(f'没有查询到{name}同学的信息')

    def change_student(self):
        name = self.name.get()
        math = self.math.get()
        chinese = self.chinese.get()
        english = self.english.get()

        # 数据验证，确保成绩为数字（允许为空，表示不修改）
        if math and not math.isdigit():
            messagebox.showinfo(title='错误', message='数学成绩必须为数字！')
            return
        if chinese and not chinese.isdigit():
            messagebox.showinfo(title='错误', message='语文成绩必须为数字！')
            return
        if english and not english.isdigit():
            messagebox.showinfo(title='错误', message='英语成绩必须为数字！')
            return

        stu = {
            "name": name,
            "math": int(math) if math else None,
            "chinese": int(chinese) if chinese else None,
            "english": int(english) if english else None,
        }
        r = db.update(stu)
        if r:
            self.status.set(f"{name}同学的信息更新完毕")
        else:
            self.status.set(f"{name}同学的信息更新失败")

if __name__ == "__main__":
    db = Database()
    root = tk.Tk()
    LoginPage(root).pack()
    root.mainloop()