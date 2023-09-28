import hashlib
import requests

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

ABORT_AFTER = timedelta(seconds=20)


def decryptMD5(testHash):
    s = []

    dt1 = datetime.now()
    while True:
        dt2 = datetime.now()
        if (dt2 - dt1) > ABORT_AFTER:
            return ""

        m = hashlib.md5()

        for c in s:
            m.update(chr(c).encode("utf-8"))

        hash = m.hexdigest()

        if hash == testHash:
            return "".join([chr(c) for c in s])

        wrapped = True

        for i in range(0, len(s)):
            s[i] = (s[i] + 1) % 256

            if s[i] != 0:
                wrapped = False
                break

        if wrapped:
            s.append(0)


# Перед использованием кода надо в терминале написать: pip3 install bs4, pip3 install requests

url = input("Введите ссылку на тест: ")
print(f"")

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
allVal = soup.find_all("input")
i = 0
d = 1

for data in allVal:
    ans = data["value"]
    tp = data["type"]
    if len(ans) > 20:
        d = d + 1
        res = decryptMD5(ans)
        print("")
        print(f"Номер{d}: {res} ({ans})")
    if len(ans) == 1 and tp == "radio" or tp == "checkbox":
        if i == 5:
            d = d + 1
            i = 0
            print("")
        print(f"Номер{d}: {ans}")
        i = i + 1
