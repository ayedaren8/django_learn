class Process:
    def __init__(self, data):
        self.data = data
        self.Rdata = ""

    def check(self):
        if len(self.data[0]) > 0:
            self.wrongMes()
        else:
            self.normalMes()

    def wrongMes(self):
        dic = {
            "STATUS": "Error",
            "message": self.data[0]
        }
        self.Rdata = dic

    def clear(self):
        pass

    def normalMes(self):

        dic = {
            "STATUS": "OK",
            "message": self.data[1]
        }
        self.Rdata = dic

    def run(self):
        self.check()
        return self.Rdata