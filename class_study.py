class Employe:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.salary = 10000
    
    company = 'Google'
  
    def add_salary(self, quantity):
        self.salary += quantity


a = Employe('Bobby', 'Brown')
b = Employe('James', 'Show')
employees = []


def add_emp(emp):
    employees.append(emp)


add_emp(a)
add_emp(b)

for guy in employees:
    print(guy.name, guy.surname, guy.company, guy.salary)

b.add_salary(500)
print(b.salary)
print(a.salary)

#print(a.name, a.surname, 'works at', a.company, 'with a salary of',a.salary)
#print(a.company)
#print(Employe.company)