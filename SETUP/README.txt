This software is published and licensed from TPS Services LTD.  All rights reserved 2012, TPS Services Ltd.

It follows the GNU GPL licensing agreement, and in short means that you can use it for free and make modifications to it (see modifications), as long as you do not sell the original software or other components thereof which are under 
GPL licnese required to run the software.

DOWNLOAD
To use the software you will require a password.  To get the password contact us through our web site and we will send the password to you via Email.

ABOUT
This is a web based (client/server) software that will work with any web browser
and web server (manual configuration if not Apache and Linux). It was written to
make creating invoice and credit notes simpler to work with and to allow
multi-user capabilities, so many invoices can be raised at the same time. It
also records all transactions in the database in it's own transaction table, and
which user performed the action.
It copes with multiple currency so you can raise an invoice in any currency you
like and print and send, and once payment has been made simply enter the amount
paid in your local currency and it does the rest, allowing you to then print an
invoice with both currencies for your records.
There are various reports available with the system, such as late payers and who
owes you money. You can also write your own batch job to remind you when people
should be paying you as there is a report that lets you know what is due.

If you have any features you would like to add or have added see the modifications section in this document.


REQUIREMENTS
	This software requires you to have the following installed on your system;
	- MySQL (latest version will work fine)
		If you chose to use another database you will need to make
		changes to the SQL scripts (create.sql, setup.sql and 
		populate.sql)
	- Web Server
		The system was written with Apache in mind and the accounts.conf
		file contains the required apache configuration that can be
		placed directly into your /etc/httpd/conf.d directory.
		If you use any other web server then you should configure it
		to run Perl CGI on the directory where you deploy the files to.
		You will also need to set up relevant security to enable user
		tracking as the system uses the logged in user to track changes.

INSTALLATION

Install script:
	REQUIRES: RPM based system.

	An ISO image of the entire software and installation for rpm based 
	systems is available for download from our web site, and comes with a 
	config file that you use to personalise the system.  Once you have 
	changed the configure file and removed the comment at the top of the 
	file you can the run the install script to have the system install for 
	you.

	Also in the Invoice.zip file the same set of scripts also exist for
	you to be able to install without having to make a CD-ROM first.

Manual Installation:
	1. Install required software;
		- Database server
		- Web server

	2. What you will need;
		- Company logo in gif format
		- Company header in gif format
		- accounts.tgz file (contains the code for the application)

	3. Create a directory for the software to be served from by the web 
	   server.
		e.g. /home/web-apps/accounts

	4. Extract the accounts.tgz file into the directory created in step 3.

	5. Create a security directory if you intend to use htpasswd users.
		e.g. /home/web-apps/accounts/security
	   Ensure that only the web service has access to this file and admins.

	6. Change the ownership, recursively, of all files and directories in
	   the directory created in step 3.

	7. Configure your web server to see the directory and its URL.
		For Apache see the accounts.conf file
	   NOTE: If you are using security that is not htpasswd you do not need
	   the following lines;
		AuthType Basic
		AuthName "TCOMPANYNAME Accounts"
		AuthUserFile TAPPHOME/security/allowed_users
	   What you will need to do is to change the AuthType to the correct
	   setting, so consult the Apache documentation.

	   You will also need to change the TURLROOT and "TAPPHOME" to you URL
	   and the location of the directory in step 3 for TAPPHOME.


	8. Edit the personalise.pm file and change all the values that begin T
		e.g. TCOMPANYNAME, TCOMPANYADDRESS, TDBUSER, etc for all the our
		variables at the top of the file after the EXPORT line, and
		before the sub doPersonalise line.

	   For information on what each one should be take a look at the
	   configure file which has the names and descriptions, or the
	   configure.example file for an example of values.

	9. Copy the personalise.pm file that you have just created into the
	   directory you created in step 3 into the include directory within
	   there.

	10. Copy your logo and title GIF files into the directory created in
	    step 3 into the images directory and rename as follows;
		The logo should be called tps2.gif
		The title should be called title.gif

	11. Create a database called accounts.

	12. Add the user you specified for TDBUSER to the database with the
	    password you specified for TDBPASS in the personalise.pm file.

	13. Grant all rights to the database for the user you added in step 12.
		e.g. for MySQL;
			CREATE DATABASE accounts;
			CREATE USER 'TDBUSER'@'%' IDENTIFIED BY 'TDBPASS';
			CREATE USER 'TDBUSER'@'localhost' IDENTIFIED BY 'TDBPASS';
			use accounts;
			GRANT ALL PRIVILEGES ON accounts.* TO 'TDBUSER'@'%';
			GRANT ALL PRIVILEGES ON accounts.* TO 'TDBUSER'@'localhost';

	14. To create the tables and populate with essential data you should
	    run the setup.sql and populate.sql scripts against the database.

	    For MySQL you can do that using the following;
		mysql -u TDBUSER -p TDBPASS accounts < setup.sql
		mysql -u TDBUSER -p TDBPASS accounts < populate.sql

	    Where TDBUSER and TDBPASS are the values from your personalise.pm.

	15. You should now be ready to use your system.
	    If you are using htpasswd ensure that you create the users and their
	    passwords using MD5 hash.  Check the htpasswd manual page.


MODIFICATIONS
You are free to modify the software for your own use, but if you would like to
have your changes included into new releases you should ensure that you
feedback any updates or changes you make to the code to us for verification
and inclusion into future releases.

SUPPORT
Training and support can be purchased.  Some support will be provided for free
via Email, depending on the nature of the request which will be at the
discretion of TPS Services Ltd, and we will inform you if payment will be
required before handling your request.

Training courses can be provided and are charged for, and are generally 1 day
in length at this time.  Please call for requirements and pricing.
