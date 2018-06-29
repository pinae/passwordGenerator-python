#!/usr/bin/python3
import binascii
import math
import cgi
import cgitb; cgitb.enable()
import html
from hashlib import pbkdf2_hmac

form = cgi.FieldStorage()

password_characters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHJKLMNPQRTUVWXYZ0123456789#!"X$%&/()[]{}=-_+*<>;:.')
#password_characters = list('abcdefghijklmnopqrstuvwxyzABCDEFGHJKLMNPQRTUVWXYZ0123456789#!"§$%&/()[]{}=-_+*<>;:.')
password_char_lists = { 0: list('abcdefghijklmnopqrstuvwxyz'),
                        1: list('ABCDEFGHJKLMNPQRTUVWXYZ'),
                        2: list('0123456789'),
                        3: list('#!"X$%&/()[]{}=-_+*<>X;:.') }
#                       3: list('#!"§$%&/()[]{}=-_+*<>X;:.') }
def convert_bytes_to_password( hashed_bytes, length):
  # this is for password 1
  number = int.from_bytes( hashed_bytes, byteorder='big')
  password = ''

  # this is for password 2
  remove = int(math.pow(2,32))
  selector = number % remove
  number2 = number // remove
  password2 = ''

  while number>0 and len(password)<length:
    #print( "Step:"+ str(len(password))+" Selector:"+str(selector) )
    # generate password 1
    password = password + password_characters[ number% len(password_characters) ]
    number = number // len( password_characters )

    # generate password 2
    act_list = password_char_lists.get( selector & 3 )
    password2 = password2 + act_list[ number2 % len(act_list) ]
    number2 = number2 // len( act_list )
    if selector:
      selector = selector // 4 

  return { 0:password, 1:password2 }

print( "Content-type: text/html" )
print()
print("<html><head>")
print("<title>Create password</title>")
print("<script language='JavaScript'>")
print("function copyToCB( id ) {")
print("    const value = document.getElementById( id ).innerHTML;")
print("    window.prompt(\"Copy to clipboard: Ctrl+C, Enter\", value);")
print("}</script>")
print("</head><body>")
print("<h1>Password generator</h1>")
print("<form action='/cgi-bin/genPW.py'>")
print("<table>")
print("<tr><td>Password for which account</td><td>:</td><td><input id='whom' name='whom' width='40' size='40' type='text'/><input type='submit' value='generate'/></td></tr>")
print("<tr><td>Master password <font size='-1'>(optional)</font></td><td>:</td><td><input id='mpw' name='mpw' width='40' size='40' type='text'/></td></tr>")
print("</table>")
print("</form>")

domain = form.getvalue( "whom", "(no value)")
master_password = form.getvalue( "mpw", "<here is your pepper>" )
converted = "error"

if not(domain=="(no value)"):
  salt = "<here is your salt>"
  hash_string = domain + master_password
  hashed_bytes = pbkdf2_hmac('sha512', hash_string.encode('utf-8'), salt.encode('utf-8'), 4096)
  print("<hr><pre>" + binascii.hexlify(hashed_bytes).decode("ascii") + "</pre><hr>" )

  converted = convert_bytes_to_password( hashed_bytes, 16 )

  print("<h3>Generated password:</h3>")
  print("<table>")
  print("<tr><td>For</td><td>:</td><td>" +html.escape( domain )+ "</td></tr>" )
  print("<tr><td>Password</td><td>:</td><td><div id='pwd1'>"+ html.escape( converted.get(0) ) +"</div></td><td><button onclick='copyToCB( \"pwd1\" );'>Copy</button></td></tr>" )
  print("<tr><td>Password2</td><td>:</td><td><div id='pwd2'>"+ html.escape( converted.get(1) ) +"</div></td><td><button onclick='copyToCB( \"pwd2\" );'>Copy</button></td></tr>" )
  print("</table>" )

print("</body></html>")
