from __future__ import unicode_literals
import sys, glob, csv, pytz, shutil
from os import access, W_OK
from os.path import abspath, join, dirname, split
sys.path.append("/randominfo/")
from random import randint, choice, sample, randrange
from datetime import datetime
from math import ceil

__title__ = 'randominfo'
__version__ = '2.0.2'
__author__ = 'Bhuvan Gandhi'
__license__ = 'MIT'

full_path = lambda filename: abspath(join(dirname(__file__), filename))

# CSV columns: 0=firstname, 1=lastname, 2=gender, 3=hobbies,
#              4=street, 5=landmark, 6=area, 7=city, 8=state, 9=pincode


def get_id(length=6, seq_number=None, step=1, prefix=None, postfix=None):
    generated_id = ""
    if seq_number is None:
        for _ in range(length):
            generated_id += str(randint(0, 9))
    else:
        if not isinstance(seq_number, int) or not isinstance(step, int):
            raise TypeError("Sequence number must be an integer.")
        generated_id = str(seq_number + step)
    if prefix is not None:
        prefix += generated_id
        generated_id = prefix
    if postfix is not None:
        generated_id += postfix
    return generated_id


def get_first_name(gender=None):
    with open(full_path('data.csv'), 'r', encoding='utf-8-sig') as f:
        firstNameFile = list(csv.reader(f))
    filteredData = []
    if gender is None:
        for data in firstNameFile:
            if data[0] != '':
                filteredData.append(data)
    else:
        if gender.lower() == "male":
            for data in firstNameFile:
                if data[0] != '' and data[2] == "male":
                    filteredData.append(data)
        elif gender.lower() == "female":
            for data in firstNameFile:
                if data[0] != '' and data[2] == "female":
                    filteredData.append(data)
        else:
            raise ValueError("Enter gender male or female.")
    return choice(filteredData)[0]


def get_last_name():
    with open(full_path('data.csv'), 'r', encoding='utf-8-sig') as f:
        lastNameFile = list(csv.reader(f))
    filteredData = [row[1] for row in lastNameFile if row[1] != '']
    return choice(filteredData)


def get_gender(first_name):
    with open(full_path('data.csv'), 'r', encoding='utf-8-sig') as f:
        firstNameFile = list(csv.reader(f))
    for data in firstNameFile:
        if data[0] != '' and data[0] == first_name:
            return data[2]
    return ""


def get_country(first_name=None):
    with open(full_path('data.csv'), 'r', encoding='utf-8-sig') as f:
        rows = list(csv.reader(f))
    if first_name is not None:
        for data in rows:
            if data[0] != '' and data[0] == first_name:
                return data[8]  # state column
        print("Specified user data is not available. Tip: Generate random country.")
        return choice([row[8] for row in rows if len(row) > 8 and row[8] != ''])
    else:
        states = [row[8] for row in rows if len(row) > 8 and row[8] != '']
        return choice(states)


def get_full_name(gender=None):
    return get_first_name(gender) + " " + get_last_name()


def get_otp(length=6, digit=True, alpha=True, lowercase=True, uppercase=True):
    lwrChars = "qwertyuioplkjhgfdsazxcvbnm"
    uprChars = "QWERTYUIOPLKJHGFDSAZXCVBNM"
    digs = "0123456789"
    chars = ""
    otp = ""
    if digit or alpha:
        if digit:
            chars += digs
        if alpha:
            if lowercase:
                chars += lwrChars
            if uppercase:
                chars += uprChars
        for _ in range(length):
            otp += str(chars[randint(0, len(chars) - 1)])
        return otp
    else:
        raise ValueError("From parameters 'digit' and 'alpha' anyone must be True.")


def get_formatted_datetime(outFormat, strDate, strFormat="%d-%m-%Y %H:%M:%S"):
    return datetime.strptime(strDate, strFormat).strftime(outFormat)


def get_email(prsn=None):
    domains = ["gmail", "yahoo", "hotmail", "express", "yandex", "nexus", "online", "omega",
               "institute", "finance", "company", "corporation", "community"]
    extentions = ['com', 'in', 'jp', 'us', 'uk', 'org', 'edu', 'au', 'de', 'co', 'me',
                  'biz', 'dev', 'ngo', 'site', 'xyz', 'zero', 'tech']
    if prsn is None:
        prsn = Person()
    c = randint(0, 2)
    dmn = '@' + choice(domains)
    ext = choice(extentions)
    if c == 0:
        email = prsn.first_name + get_formatted_datetime("%Y", prsn.birthdate, "%d %b, %Y") + dmn + "." + ext
    elif c == 1:
        email = prsn.last_name + get_formatted_datetime("%d", prsn.birthdate, "%d %b, %Y") + dmn + "." + ext
    else:
        email = prsn.first_name + get_formatted_datetime("%y", prsn.birthdate, "%d %b, %Y") + dmn + "." + ext
    return email


def random_password(length=8, special_chars=True, digits=True):
    spec_chars = ['!', '@', '#', '$', '%', '^', '&', '*']
    alpha = "QWERTYUIOPLKJHGFDSAZXCVBNMmnbvcxzasdfghjklpoiuytrewq"
    spec_char_len = dig_char_len = 0
    chars = ""
    if special_chars:
        spec_char_len = randint(1, ceil(length / 4))
        for _ in range(spec_char_len):
            chars += choice(spec_chars)
    if digits:
        dig_char_len = randint(1, ceil(length / 3))
        for _ in range(dig_char_len):
            chars += str(randint(0, 9))
    remaining = length - (dig_char_len + spec_char_len)
    for _ in range(remaining):
        chars += choice(alpha)
    return ''.join(sample(chars, len(chars)))


def get_phone_number(country_code=True):
    phone = ""
    if country_code:
        cCodes = [91, 144, 141, 1, 44, 86, 52, 61, 32, 20, 33, 62, 81, 31, 7]
        phone = "+" + str(choice(cCodes)) + " "
    for i in range(0, 10):
        phone += str(randint(6, 9) if i == 0 else randint(0, 9))
    return phone


def get_today(_format="%d-%m-%Y %H:%M:%S"):
    return datetime.today().strftime(_format)


def get_date(tstamp=None, _format="%d %b, %Y"):
    startRange = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)
    endRange = datetime.today()
    if tstamp is None:
        startTs = startRange.timestamp()
        endTs = datetime.timestamp(endRange)
        tstamp = randrange(int(startTs), int(endTs))
    else:
        if not isinstance(tstamp, int):
            raise ValueError("Timestamp must be an integer.")
    return datetime.utcfromtimestamp(tstamp).strftime(_format)


def get_birthdate(startAge=None, endAge=None, _format="%d %b, %Y"):
    _startRange = datetime.today()
    _endRange = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.UTC)
    if startAge is not None:
        if not isinstance(startAge, int):
            raise ValueError("Starting age value must be integer.")
    if endAge is not None:
        if not isinstance(endAge, int):
            raise ValueError("Ending age value must be integer.")
    if startAge is not None and endAge is not None:
        if startAge >= endAge:
            raise ValueError("Starting age must be less than ending age.")
        _startRange = datetime(datetime.now().year - startAge, 12, 31, 23, 59, 59, 0, pytz.UTC)
        _endRange = datetime(datetime.now().year - endAge, 1, 1, 0, 0, 0, 0, pytz.UTC)
    elif startAge is not None or endAge is not None:
        ageYear = startAge if startAge is not None else endAge
        _startRange = datetime(datetime.now().year - ageYear, 12, 31, 23, 59, 59, 0, pytz.UTC)
        _endRange = datetime(datetime.now().year - ageYear, 1, 1, 0, 0, 0, 0, pytz.UTC)
    startTs = _startRange.timestamp()
    endTs = _endRange.timestamp()
    return datetime.fromtimestamp(randrange(int(endTs), int(startTs))).strftime(_format)


def get_address():
    addrParam = ['street', 'landmark', 'area', 'city', 'state', 'pincode']
    full_addr = []
    for i in range(4, 10):
        with open(full_path('data.csv'), 'r', encoding='utf-8-sig') as f:
            addrFile = list(csv.reader(f))
        allAddrs = []
        for addr in addrFile:
            try:
                if len(addr) > i and addr[i] != '':
                    allAddrs.append(addr[i])
            except IndexError:
                pass
        full_addr.append(choice(allAddrs))
    return dict(zip(addrParam, full_addr))


def get_hobbies():
    with open(full_path('data.csv'), 'r', encoding='utf-8-sig') as f:
        hobbiesFile = list(csv.reader(f))
    allHobbies = [row[3] for row in hobbiesFile if row[3] != '']
    hobbies = []
    for _ in range(1, randint(2, 6)):
        hobbies.append(choice(allHobbies))
    return hobbies


class Person:
    def __init__(self, gender=None):
        firstName = get_first_name(gender)
        self.first_name = firstName
        self.last_name = get_last_name()
        self.full_name = self.first_name + " " + self.last_name
        self.birthdate = get_birthdate()
        self.phone = get_phone_number()
        self.email = get_email(self)
        self.gender = get_gender(firstName)
        self.country = get_country(firstName)
        self.paswd = random_password()
        self.hobbies = get_hobbies()
        self.address = get_address()
        self.customAttr = {}

    def set_attr(self, attr_name, value=None):
        if attr_name.isalnum():
            if attr_name[0].isalpha():
                self.customAttr[attr_name] = value
                print("Attribute '" + str(attr_name) + "' added.")
            else:
                raise ValueError("First character of attribute must be an alphabet.")
        else:
            raise ValueError("Attribute name only contains alphabets and digits.")

    def get_attr(self, attr_name):
        if attr_name.isalnum():
            if attr_name[0].isalpha():
                if attr_name in self.customAttr:
                    return self.customAttr[attr_name]
                else:
                    raise AttributeError("Specified attribute does not exist.")
            else:
                raise ValueError("First character of attribute must be an alphabet.")
        else:
            raise ValueError("Attribute name only contains alphabets and digits.")

    def get_details(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "email": self.email,
            "phone": self.phone,
            "paswd": self.paswd,
            "country": self.country,
            "hobbies": self.hobbies,
            "address": self.address,
            "other_attr": self.customAttr
        }
