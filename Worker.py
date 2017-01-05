import re
a = re.compile('omer')
match = a.findall('omeromeromeromeromeromeomer')
for m in match:
    print(m)