class Test(object):

    def mymethod(self, line):
        full_line = line + "Artem"
        print(full_line)


line = "My name is "
name_line = Test()
name_line.mymethod(line)