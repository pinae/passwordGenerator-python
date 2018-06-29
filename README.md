# ctSESAM-python
This repository contains the ctSESAM password manager:

1. as command line Python c't password manager.
2. as a version which runs as CGI script on a CGI enabled webserver which allows to run Python CGI
(For example it is running on a raspberry pi with lighttpd)

# Installation
* Setup lighttpd with cgi enabled (searching the web helps;o)
* Just copy genPW.py into the cgi-bin folder
* Make sure you have your own values for master_password-default and salt (marked as <here is your salt> and <here is your pepper>)

# Changes made in the web-version
1. A second method to generate a password has been added (see description)
2. Passwords are better with 16 characters ;o)
3. The paragraph caused problems in the browsers even if the password was printed html encoded

# Description
Very soon it's been the case that the password which was generated did not have characters of all different types. Some password rules require this.
So another method has been implemented to create a password, which simply takes the first 32 bit of the "number" variable to decide which set of characters to use.
There is still a small chance that a password does not contain a character from all sets, but the chances are small enough that both passwords don't.

The master password is optional and defaults to a value given in the code. Again: You might want to change this in your version together with the salt.
This allows multi user usage where one user can't easily create passwords from other users by guessing the account.

Security issue:

Lighttpd does not log the access per default, which is good. If the access.log is written, the admin can of course read the account and master password used.
