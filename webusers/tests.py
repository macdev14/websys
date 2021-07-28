from django.test import Client, TestCase
from .models import User
# Create your tests here.
class UserCreateTest(TestCase):
    def setUp(self):
        cpf = ['52998224725', '33177446423', '07350445113', '27223327600',
        '21802236503', '92390401961',
        '18855398865', '53922631860', '47131158437', '36533335715']
        # create users
        email_test = [
            'hiram67@gleichner.net',
            'aurore99@yahoo.com',
            'katheryn.sawayn@pollich.net',
            'renee39@bins.com',
            'ileffler@yahoo.com',
            'murray.kaycee@hotmail.com',
            'yrunolfsson@hotmail.com',
            'dominique.mraz@gmail.com',
            'gladyce11@ullrich.com',
            'haylee.fritsch@yahoo.com'
        ]
        user1=User.objects.create(name='pessoa1', identity=cpf[0], 
        email=email_test[0],
        pis='123', country='Brasil', 
        state='sp', city='sp', 
        zipcode='12900300', street='Avenida', 
        number=1111, reference='ref')
   
    def test_identity(self):
        #identity test 
        user = User.objects.get(name='pessoa1')
        total = 0
        i = 10
        for char in user.identity[:-2]:
            tot = int(char) * i 
            total = tot + total
            i = i - 1
        res = round((total * 10) % 11, 1)
        self.assertTrue(res==int(user.identity[-2]))
   

if __name__ == '__main__':
    UserCreateTest.main()