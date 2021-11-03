class C:

    def m(self):

        return "result"


an_object = C()


class_method = getattr(C, "m")

result = class_method(an_object)


print(result)