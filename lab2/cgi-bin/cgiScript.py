import cgi
import os
import http.cookies

form = cgi.FieldStorage()

firstName = form.getvalue('firstName',"")
secondName = form.getvalue('secondName', "")
sex = form.getvalue('sex', "")
fruits = form.getvalue('fruits', "")

print(f"Set-cookie: firstName={firstName}")
print(f"Set-cookie: secondName={secondName}")
print(f"Set-cookie: sex={sex}")

cookies = http.cookies.SimpleCookie(os.environ["HTTP_COOKIE"])

firstName_cookie = cookies.get('firstName').value
secondName_cookie = cookies.get('secondName').value
sex_cookie = cookies.get('sex').value

cookieKeys = ["firstName", "secondName", "sex"]

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

print("<br><br>")
print(f"<h1>Data from cookie</h1>")
print(f"<p>{firstName_cookie=}</p>")
print(f"<p>{secondName_cookie=}</p>")
print(f"<p>{sex_cookie=}</p>")

deleteCookieForm = """ <br><br>
    <form method="POST">
        Do you want to remove cookies? <br><br>
        <input type="submit" name="deleteCookies" value="Remove">
    </form>
"""
print(deleteCookieForm)
        