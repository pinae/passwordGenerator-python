# ctSESAM-python
This is a fork from pinae/ctSESAM-python.

It contains the original version of the command line Python c't password manager.
And it contains a version which works on a python enabled cgi capable webserver.
I have it running on a raspberry pi with lighttpd.

#Installation
* Setup lighttpd with cgi enabled (searching the web helps;o)
* Just copy genPW.py into the cgi-bin folder
* Make sure you have your own values for master_password-default and salt

#Changes made
1. I added a second method to generate a password
2. Passwords are better with 16 characters ;o)
3. The paragraph caused problems in the browsers even if the password was html encoded

#Description
Very soon I had the case that the password which was generated did not have characters of all different types. Some password rules require this.
So I created another method to create a password, which simply takes the first 32 bit of the number to decide which set of characters to use.
There is still a small chance that a password does not contain a character from all sets, but I think the chances are small enough.

The master password is optional and would default to a value given in the code. You might want to change this in your version together with the salt.
This allows multi user usage where one user can't easily create passwords from other users by guessing the account.

Security issue:

Lighttpd does not log the access per default, which is good. If the access.log is written, the admin can of course read the account and master password used.
