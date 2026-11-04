import json
from abc import ABC, abstractmethod
from turtledemo.chaos import line


class Book:
    def __init__(self, book_id, title, author, total_num):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.total_num = total_num
        self.__available_num = total_num

    def borrow_book(self):
        if self.__available_num > 0:
            self.__available_num -= 1
            return True
        return False

    def return_book(self):
        self.__available_num += 1
        return True

    def get_availabe_num(self):
        return self.__available_num


class Member(ABC):
    """
    继承了ABC类，表示这是一个抽象类，只能被继承不能被实例化
    """
    def __init__(self, member_id, name, password, borrowed_books):
        self.member_id = member_id
        self.name = name
        self.__password = password
        self.borrowed_books = borrowed_books

    def borrow_book(self, book: Book):
        # 是否达到借书上限
        if len(self.borrowed_books) >= self.get_max_borrow_num():
            print("借书失败，已达到借书上限")
            return False

        if book.borrow_book():
            self.borrowed_books.append(book)
            print("借书成功")
            return True
        else:
            print("借书失败，图书已借完")
            return False

    def return_book(self, book: Book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.return_book()
            print("还书成功")
            return True
        else:
            print(f"还书失败，你没借过这本书{book.title}")
            return False

    def get_password(self) -> str:
        return self.__password

    def get_borrowed_books(self) -> list:
        return self.borrowed_books

    @abstractmethod
    def get_max_borrow_num(self) -> int:
        pass

class NormalMember(Member):
    def get_max_borrow_num(self) -> int:
        return 3

class VipMember(Member):
    def __init__(self, member_id, name, password, borrowed_books, vip_level):
        super().__init__(member_id, name, password, borrowed_books)
        self.vip_level = vip_level

    def get_max_borrow_num(self) -> int:
        return 6 + self.vip_level


class Library:
    def __init__(self):
        self.books = {} # 字典存储
        self.members = {}
        self.current_member : None | Member = None # 当前登录的成员
        self.load_books() # 加载图书
        self.load_members() # 加载成员

    def load_books(self):
        with open("data/books.json", "r", encoding="utf-8") as f:
            book_data = json.load(f)
            for book in book_data:
                self.books[book["编号"]] = Book(book["编号"], book["标题"], book["作者"], int(book["数量"]))
        print("图书加载完成")

    def load_members(self):
        with open("data/members.json", "r", encoding="utf-8") as f:
            member_data = json.load(f)
            for member in member_data:
                if member["卡号"].startswith("N"):
                    self.members[member["卡号"]] = NormalMember(member["卡号"], member["姓名"], member["密码"], [])
                elif member["卡号"].startswith("V"):
                    self.members[member["卡号"]] = VipMember(member["卡号"], member["姓名"], member["密码"], [], member["会员等级"])
        print("成员加载完成")

    def login(self):
        while True:
            print("开始登录~\n")
            member_id = input("请输入卡号：")
            password = input("请输入密码：")

            if member_id not in self.members:
                print("登录失败，会员卡号不存在")
                continue

            member = self.members[member_id]
            if member.get_password() == password:
                self.current_member = member
                print(f"登录成功， 欢迎回来，{member.name}")
                return True

            print(f"登录失败，卡号或密码错误，会员{member.name}")
            continue

    def run(self):
        if self.login():
            while True:
                print("--------------------------")
                print("1. 借书")
                print("2. 还书")
                print("3. 查看借阅")
                print("5. 退出")
                print("--------------------------")
                choice = input("请输入你的选择：")

                if choice == "1":
                    self.borrow_book()
                elif choice == "2":
                    self.return_book()
                elif choice == "3":
                    self.view_borrowed_books()
                elif choice == "5":
                    print("退出系统，欢迎下次光临！")
                    break
                else:
                    print("无效的选择，请重新输入")

    def borrow_book(self):
        print("开始借书~")
        # 可借的图书列表
        available_books = [book for book in self.books.values() if book.get_availabe_num() > 0]
        for book in available_books:
            print(f"编号：{book.book_id}, 标题：{book.title}, 作者：{book.author}, 剩余数量：{book.get_availabe_num()} ")

        book_id = input("请输入图书编号：")
        if book_id not in self.books:
            print("图书不存在")
            return
        book = self.books[book_id]
        if self.current_member.borrow_book(book):
            self.books[book_id] = book
        print("借书完成")

    def return_book(self):
        print("开始还书~")
        # 借阅的图书列表
        borrowed_books = self.current_member.get_borrowed_books()
        for book in borrowed_books:
            print(f"编号：{book.book_id}, 标题：{book.title}, 作者：{book.author}, 剩余数量：{book.get_availabe_num()} ")

        book_id = input("请输入图书编号：")
        if book_id not in self.books:
            print("图书不存在")
            return
        self.current_member.return_book(self.books[book_id])
        print("还书完成")

    def view_borrowed_books(self):
        # 借阅的图书列表
        borrowed_books = self.current_member.get_borrowed_books()
        if borrowed_books == []:
            print("你没有借书哦")
            return
        for book in borrowed_books:
            print("你当前的借书列表：")
            print(f"编号：{book.book_id}, 标题：{book.title}, 作者：{book.author}, 剩余数量：{book.get_availabe_num()} \n")

def main():
    ls = Library()
    ls.run()
if __name__ == "__main__":
    main()