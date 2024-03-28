from datetime import datetime
import pygal
import smtplib


class Stock:

    def __init__(self, prod, categ, um='Pcs', balance=0):
        self.prod = prod
        self.categ = categ
        self.balance = balance
        self.um = um
        self.i = {}
        self.e = {}
        self.d = {}

    def enter(self, qty, date=str(datetime.now().strftime('%D'))):
        self.date = date
        self.qty = qty
        self.balance += qty
        if self.d.keys():
            key = max(self.d.keys()) + 1
        else:
            key = 1
        self.i[key] = qty
        self.d[key] = self.date

    def exit(self, qty, date=str(datetime.now().strftime('%D'))):

        self.date = date
        self.qty = qty
        self.balance -= self.qty
        if self.d.keys():
            key = max(self.d.keys()) + 1
        else:
            key = 1
        self.e[key] = self.qty
        self.d[key] = self.date

    def product_sheet(self):

        print('Product sheet ' + self.prod + ': ' + self.um)
        print(28 * '-')
        print(' Nrc ', '  Date ', 'Entries', 'Exits')
        print(28 * '-')
        for v in self.d.keys():
            if v in self.i.keys():
                print(str(v).rjust(5), self.d[v], str(self.i[v]).rjust(6), str(0).rjust(6))
            else:
                print(str(v).rjust(5), self.d[v], str(0).rjust(6), str(self.e[v]).rjust(6))
        print(28 * '-')
        print('Current stock:      ' + str(self.balance).rjust(10))
        print(28 * '-' + '\n')

    def projection(self):    #1,#9
        """Graphical projection of entries and exits --- Stacked Bar"""

        self.x=[]
        for v in self.d.values():
            self.x.append(v)
        self.x1= []
        self.x2= []
        self.h = {}
        self.f = {}
        self.c=0
        for v in self.d.keys():
            self.c+=1
        for v in range (1,self.c+1):
            self.h[v]=0
            self.f[v]=0
        for v in self.i.keys():
            self.h[v] = self.i[v]
        for v in self.e.keys():
            self.f[v] = self.e[v]
        for v in self.h.values():
            self.x1.append(v)
        for v in self.f.values():
            self.x2.append(v)

        ob = pygal.StackedBar()
        ob.title = 'Graphical projection of entries and exits for ' + self.prod
        ob.add('Entries',self.x1)
        ob.add('Exits', self.x2)
        ob.x_labels = self.x
        ob.render_to_file('Projection.svg')
        print('You will find the graphical projection of entries and exits under the name Projection.svg')

    def minimum(self, min=0):
        """Warning by email in case of exceeding a minimum at a product"""

        if self.balance < min:
            print('Minimum', min, 'at', self.prod, 'has been exceeded!')
            self.sender = 'enterMail@email.com'
            self.recipient = input('Enter the address where you want to send the warning email for exceeding the minimum')
            self.password = 'enterPassword'
            self.message = """THIS IS JUST A WARNING MESSAGE
               Minimum """+str(min)+' at '+self.prod+' has been exceeded!!'
            self.ob = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.ob.login(self.sender, self.password)
            self.ob.sendmail(self.sender, self.recipient, self.message)

        else:
            print('Minimum ', min, 'at', self.prod, 'has not been exceeded!!')

    def info(self):
        """Sending the product sheet by email"""

        self.message = 'Product sheet' + self.prod + ': ' + self.um+'\n'
        self.message+=55 * '-'+'\n'
        self.message+=' Nrc '+ '\t    Date '+ 'Entries'+ ' Exits'+'\n'
        for v in self.d.keys():
            if v in self.i.keys():
                self.message+=str(v).rjust(5)+'| '+ self.d[v]+'  '+ str(self.i[v]).rjust(6)+' '+ str(0).rjust(6)+'\n'
            else:
                self.message+=str(v).rjust(5)+'| '+ self.d[v]+'  '+ str(0).rjust(6)+' '+ str(self.e[v]).rjust(6)+'\n'
        self.message+=35 * '-'+'\n'
        self.message+='Current stock:      ' + str(self.balance).rjust(10)+'\n'
        self.message+=35 * '-' + '\n'
        self.sender = 'enterMail@email.com'
        self.recipient = input('Enter the address where you want to receive the product sheet:')
        self.password = 'enterPassword'
        self.ob = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.ob.login(self.sender, self.password)
        self.ob.sendmail(self.sender, self.recipient, self.message)


strawberries = Stock('strawberries', 'fruits', 'kg')
milk = Stock('milk', 'dairy', 'litre')


strawberries.enter(100)
strawberries.exit(73)
strawberries.enter(100)
strawberries.exit(85)
strawberries.enter(100)
strawberries.exit(101)
strawberries.enter(500)
strawberries.enter(79)
strawberries.exit(520)

strawberries.product_sheet()


milk.enter(1500)
milk.exit(975)
milk.enter(1200)
milk.exit(1490)
milk.enter(1000)
milk.exit(1200)

milk.product_sheet()


strawberries.projection()
strawberries.minimum(35)
strawberries.info()