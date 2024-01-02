from collections import UserDict
from datetime import date, datetime


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError
        self.__value = new_value

    def is_valid(self, value):
        return True

    def __str__(self):
        return str(self.__value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.is_valid_phone_number(value):
            raise ValueError
        super().__init__(value)

    def is_valid(self, value):
        return self.is_valid_phone_number(value)

    def is_valid_phone_number(self, value):
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    def __init__(self, value):
        if not self.is_valid_birthday(value):
            raise ValueError
        super().__init__(value)

    def is_valid(self, value):
        return self.is_valid_birthday(value)

    def is_valid_birthday(self, new_birthday):
        if new_birthday is not None:
            try:
                datetime.strptime(new_birthday, "%Y-%m-%d")
                return True
            except ValueError:
                return False
        return True


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, value):
        try:
            self.phones.append(Phone(value))
        except ValueError:
            print(f"Phone can not be added {value}")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    def edit_phone(self, phone, new_phone):
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                try:
                    self.phones[i] = Phone(new_phone)
                    return True
                except ValueError:
                    print(f"Phone {phone} can not be replaced by {new_phone}")
                    return False
        raise ValueError(f"Phone {phone} not found in the record.")

    def find_phone(self, phone):
        for i in range(len(self.phones)):
            if self.phones[i].value == phone:
                return self.phones[i]

    def days_to_birthday(self):
        if self.birthday.value is not None:
            birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d")
            today = date.today()
            next_birthday = datetime(today.year, birthday.month, birthday.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, birthday.month, birthday.day).date()
            days_left = (next_birthday - today).days
            return days_left
        return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            print(f"{name} does not exist in dictionary")

    def delete(self, name):
        if name in self.data:
            self.data.pop(name)
        else:
            print(f"{name} does not exist in dictionary")

    def __iter__(self):
        return AddressBookIterable(self, 1)


class AddressBookIterable:
    def __init__(self, address_book, records_number):
        self.record = list(address_book.data.values())
        self.N = records_number
        self.index = 0

    def __next__(self):
        stop = min(self.N, len(self.record))
        if self.index < stop:
            contact = self.record[self.index]
            self.index += 1
            return contact
        else:
            raise StopIteration


john_record = Record("John", "2002-1-31")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
days = john_record.days_to_birthday()
print(f"Left {days} days to John's birthday")

try:
    john_record.edit_phone("5555555555", "7d777777777")
except ValueError as err:
    print(err)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_phone("9876f43210")

book = AddressBook()
book.add_record(john_record)
book.add_record(jane_record)

book.delete('jane')

print("Address Book")
for index, record in enumerate(book):
    print(f"{index + 1} contact = Name: {record.name}; Phones: {', '.join(p.value for p in record.phones)}; Birthday: {record.birthday}")
