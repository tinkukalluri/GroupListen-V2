# from hashlib import new


# def fun1():
#     return "hello tinku"


# def fun2():
#     fun3=fun1
#     #print(fun3())

# class c1:
#     x1=[]
#     def __init__(self ):
#         pass
#     def get(self):
#         #print("in c1")
#     def __str__(self):
#         return "toString()"

# class c2:
#     def __init__(self,class_name):
#         self.class_name = class_name
#     def call_class(self):
#         obj1=self.class_name()
#         #print(obj1)


# fun2()

# obj_c2_1= c2(c1)

# obj_c2_1.call_class()


# class_name= c1

# cc1= c1()

# cc1.get()

# cc2=class_name()

# cc2.get()


# class_name=c1("lets goo")

# cc= c1("tinku", "kalluri")

# # cc2 = class_name("tunkunbaudbuiabduiwabiu")
# cc.get_x1()
# class_name.get_x1()


# dic={
#     'arr':[1 ,2 , 3 ,4 , 5]
# }

# if 0 in dic['arr']:
#     #print("yupp")

from abc import abstractclassmethod, abstractmethod


class abs:
    @abstractclassmethod
    def fun1(self):
        pass

    @abstractmethod
    def fun3():
        #print('i m a static method')

    def fun2(self):
        #print("from fun2 in abs")

class c1(abs):
    def fun1(self):
        #print('from c1')
        super().fun2()

abs_obj1= c1()

abs_obj1.fun1()

