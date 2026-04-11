class test:
    xd = "xd"
    a = 1
    b = 2

    @classmethod
    def get_a(cls):
        return cls.a
    
    def zm_a(self, inc):
        self.a += inc
    def dodaj(self):
        print(self.a + self.b)
    

    # def co_mam():

t = test()
t.zm_a(3)
t.dodaj()