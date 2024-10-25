class Customer:
    def __init__(self,FullName,Email,Number):
        self.FullName=FullName
        self.Email=Email
        self.Number=Number
    def __str__(self):
        return str(self.FullName) +" - "+self.Email +"-"+str(self.Number)