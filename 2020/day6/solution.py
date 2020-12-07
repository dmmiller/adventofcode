import functools

class Person:

    @classmethod
    def from_line(cls, line):
        person = Person()
        person.set = set(line)
        return person

class Group:

    def __init__(self):
        self.people = []

    def add_person(self, person):
        self.people.append(person)

    def get_anyone_answer_count(self):
        merged_set = functools.reduce(set.union, (p.set for p in self.people))
        return len(merged_set)
    
    def get_everyone_answer_count(self):
        merged_set = functools.reduce(set.intersection, (p.set for p in self.people))
        return len(merged_set)

with open('input.txt') as f:
    groups = []
    active_group = Group()
    for line in f:
        line = line.strip()
        # non empty lines contain people data
        # empty lines indicate we are done with a group
        if len(line) > 0:
            active_group.add_person(Person.from_line(line))
        else:
            groups.append(active_group)
            active_group = Group()
    groups.append(active_group)
    total_anyone = sum(group.get_anyone_answer_count() for group in groups)
    total_everyone = sum(group.get_everyone_answer_count() for group in groups)
    print(f"The total of counts that anyone answered is {total_anyone}")
    print(f"The total of counts that everyone answered is {total_everyone}")