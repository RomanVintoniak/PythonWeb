import cgi

form = cgi.FieldStorage()

firstName = form.getvalue('firstName')
secondName = form.getvalue('secondName')
sex = form.getvalue('sex')
fruits = form.getvalue('fruits')

print("Content-type:text/html\r\n\r\n")
print("<h1>Data from user</h1>")
print(f"<p>First name: {firstName}</p>")
print(f"<p>Second name: {secondName}</p>")
print(f"<p>Sex: {sex}</p>")

print(f"<p>Favourite fruits: ", end="")

if isinstance(fruits, list):
    for item in fruits:
        print(f"{item} ", end="")
    print("</p>")
else:
    print(f"{fruits}")
