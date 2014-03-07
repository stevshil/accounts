#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use DBI();

my $CoID=param("id"); # company id
my $DoWhat=param("DoWhat");

sub updateContact
{
	my $id=param("id");
	my $compid=param("compid");
	my $custname=param("custname");
	$custname=~s/'/''/g;
        my $add1=param("add1");
        my $add2=param("add2");
        my $add3=param("add3");
        my $town=param("town");
        my $county=param("county");
        my $pcode=param("pcode");
        my $country=param("country");
        my $phone=param("phone");
	my $mobile=param("mobile");
        my $fax=param("fax");
	my $email=param("Email");
	my $notes=param("notes");
	$notes=~s/'/''/g;

        my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
        $dbh->do("UPDATE CustomerContacts SET Name='$custname', Address1='$add1', Address2='$add2', Address3='$add3', TownCity='$town', County='$county', Postcode='$pcode', Country='$country', Phone='$phone', Fax='$fax', email='$email', mobile='$mobile', notes='$notes' WHERE CoID=$compid AND CustContactID=$id");

	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"CustomerContacts","$id","UPDATE","$ENV{'REMOTE_USER'}");
        $dbh->disconnect();
        print "<td valign=top align=left><h1>Contact updated successfully</h1><br>";
        print "<form><input type=button name=here value='Back to list' onClick='location.href=\"CoContacts.cgi?id=$compid&DoWhat=list\"'></form></td></tr>";

}

sub addContact
{
	my $id=param("id");
	my $compid=param("compid");
	my $custname=param("custname");
	$custname=~s/'/''/g;
        my $add1=param("add1");
        my $add2=param("add2");
        my $add3=param("add3");
        my $town=param("town");
        my $county=param("county");
        my $pcode=param("pcode");
        my $country=param("country");
        my $phone=param("phone");
	my $mobile=param("mobile");
        my $fax=param("fax");
	my $email=param("Email");
	my $notes=param("notes");
	$notes=~s/'/''/g;

        my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
        $dbh->do("INSERT INTO CustomerContacts (Name,Address1,Address2,Address3,TownCity,County,Postcode,Country,Phone,Fax,email,mobile,notes,CoID) VALUES('$custname','$add1','$add2','$add3','$town','$county','$pcode','$country','$phone','$fax','$email','$mobile','$notes',$id)");

	my $sth = $dbh->prepare("SELECT CustContactID FROM CustomerContacts WHERE CoID=$id AND Name='$custname'");
	$sth->execute();
	my $ref=$sth->fetchrow_hashref();
	my $CCID=$ref->{CustContactID};
	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"CustomerContacts","$CCID","ADD","$ENV{'REMOTE_USER'}");
        $dbh->disconnect();
        print "<td valign=top align=left><h1>Contact added successfully</h1><br>";
        print "<form><input type=button name=here value='Back to list' onClick='location.href=\"CoContacts.cgi?id=$id&DoWhat=list\"'></form></td></tr>";

}

sub deleteContact
{
	my $id=param("id");
	my $compid=param("compid");

	my $dbh =DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to databas";
	$dbh->do("DELETE FROM CustomerContacts WHERE CustContactID=$id AND CoID=$compid");
	$dbh->do("INSERT INTO History (TableName,ID,Action,ModifiedBy,ModifiedDate) VALUES(?,?,?,?,Now())",undef,"CustomerContacts","$id","DELETE","$ENV{'REMOTE_USER'}");
	$dbh->disconnect();
        print "<td valign=top align=left><h1>Contact has been removed from database</h1><br>";
        print "<form><input type=button name=here value='Back to list' onClick='location.href=\"CoContacts.cgi?id=$compid&DoWhat=list\"'></form></td></tr>";
}

sub listContacts
{
	# Select company detail from database
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	# Check that we have something to list first
	my $sth = $dbh->prepare("SELECT count(*) AS total FROM CustomerContacts WHERE CoID=$CoID");
	$sth->execute();
	$ref=$sth->fetchrow_hashref();
	my $custcount=$ref->{'total'};
	$sth->finish();

	# Now list them
	$sth = $dbh->prepare("SELECT * FROM CustomerDetails WHERE CoID=$CoID");
	$sth->execute();
	$ref=$sth->fetchrow_hashref();
	$coname=$ref->{'CompanyName'};
	$sth->finish();

	print <<"__END__";
        <td align=left valign=top><h1>Contacts for $coname</h1>
        <p>Click on the ID column number to view/edit contact details.<br><br>
        <table width="100%" border=0 cellspacing=0 cellpadding=0>
        <tr><th align=left width=25>ID</th><th align=left width=250>Name</th><th align=left width=150>Mobile</th><th align=left width=150>Phone</th><th align=left width=150>Fax</th><th align=center>Email</th></tr>
__END__

	if ( $custcount > 0 )
	{
		$sth = $dbh->prepare("SELECT * FROM CustomerContacts WHERE CoID=$CoID Order by Name");
		$sth->execute();
		while ( my $ref = $sth->fetchrow_hashref() )
		{
			print "<tr><td><a href=\"CoContacts.cgi?DoWhat=Display&id=$ref->{'CustContactID'}&coname=$coname&compid=$CoID\">$ref->{'CustContactID'}</a></td>";
			print "<td>$ref->{'Name'}</td>";
			print "<td>$ref->{'Mobile'}</td>";
			print "<td>$ref->{'Phone'}</td>";
			print "<td>$ref->{'Fax'}</td>";
			print "<td><a href=\"mailto:$ref->{'email'}\">$ref->{'email'}</a></td></tr>";
		}
		$sth->finish();
	}

	$dbh->disconnect();

	print "<tr><td colspan=5>&nbsp;</td></tr>";
	print "<tr><td colspan=5 align=center><input type=button name=add value='Add Contact' onClick='location.href=\"CoContacts.cgi?id=$CoID&DoWhat=New&DoNext=Add&coname=$coname\"'> &nbsp; <input type=button name=back value=Back onClick='history.go(-1)'></td></tr>";
}

sub displayDetails
{
	my $coname=param("coname");
	my $companyid=param("compid");
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT * FROM CustomerContacts WHERE CustContactID=$CoID");
	$sth->execute();
	$ref=$sth->fetchrow_hashref();
	$sth->finish();

	print <<"__END__";
		<td align=left valign=top><h1>View Contact for $coname</h1>
		<table>
		<tr><td>Contact Name:</td><td>$ref->{'Name'}</td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td valign=top>Address:</td><td>$ref->{'Address1'}<br>
					$ref->{'Address2'}<br>
					$ref->{'Address3'}</td></tr>
		<tr><td>Town/City:</td><td>$ref->{'TownCity'}</td></tr>
		<tr><td>County:</td><td>$ref->{'County'}</td></tr>
		<tr><td>Post Code:</td><td>$ref->{'Postcode'}</td></tr>
__END__

	print "<tr><td>Country:</td><td>";
	my $sth2 = $dbh->prepare("SELECT * FROM Countries WHERE CountryID='$ref->{'Country'}'");
	$sth2->execute();
	my $ref2 = $sth2->fetchrow_hashref();
	print "$ref2->{'CountryText'}";
	$sth2->finish();
	print "</td></tr>";

	print <<"__END__";
		<tr><td>&nbsp;</td></tr>
		<tr><td>Telephone:</td><td>$ref->{'Phone'}</td></tr>
		<tr><td>Mobile:</td><td>$ref->{'Mobile'}</td></tr>
		<tr><td>Fax:</td><td>$ref->{'Fax'}</td></tr>
		<tr><td>Email:</td><td>$ref->{'email'}</td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td>Notes:</td><td>$ref->{'Notes'}</td></tr>
__END__
	
	print <<"__END__";
		<tr><td>&nbsp;</td></tr>
		<tr><td colspan=2 align=center><input type=button name=edit onClick="location.href='CoContacts.cgi?id=$CoID&DoWhat=Edit&compid=$ref->{'CoID'}&coname=$coname&DoNext=Update'" value="Edit"> &nbsp; <input type=button name=del value=Delete onClick="location.href='CoContacts.cgi?id=$CoID&DoWhat=Delete&compid=$ref->{'CoID'}&coname=$coname'"> &nbsp; <input type=button name=back onClick="history.go(-1)" value="Back"></td></tr>
		</table>
		</td></tr>
	</table>
__END__
}

sub editForm
{
	my ($nextAction)=@_;
	my $id=param("id");
	my $compid=param("compid");
	my $coname=param("coname");
	undef $ref;

	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	if ( $nextAction eq "Update" )
	{
		my $sth = $dbh->prepare("SELECT * FROM CustomerContacts WHERE CustContactID=$CoID");
		$sth->execute();
		$ref=$sth->fetchrow_hashref();
		$sth->finish();
	}
	print <<"__END__";
		<td align=left valign=top><h1>Edit Contact for $coname</h1>
		<form name=contactadd method=post action="CoContacts.cgi">
		<input type=hidden name=DoWhat value=$nextAction>
		<input type=hidden name=compid value="$compid">
		<input type=hidden name=id value=$id>
		<table>
		<tr><td>Name:</td><td><input type=text name=custname value="$ref->{'Name'}" size=80></td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td valign=top>Address:</td><td><input type=text name=add1 value="$ref->{'Address1'}" size=80><br>
					<input type=text name=add2 value="$ref->{'Address2'}" size=80><br>
					<input type=text name=add3 value="$ref->{'Address3'}" size=80></td></tr>
		<tr><td>Town/City:</td><td><input type=text name=town value="$ref->{'TownCity'}" size=60></td></tr>
		<tr><td>County:</td><td><input type=text name=county value="$ref->{'County'}" size=60></td></tr>
		<tr><td>Post Code:</td><td><input type=text name=pcode value="$ref->{'Postcode'}" size=20></td></tr>
__END__

	print "<tr><td>Country:</td><td><select name=country>";
	my $sth2 = $dbh->prepare("SELECT * FROM Countries Order By CountryText");
	$sth2->execute();
	while ( my $ref2 = $sth2->fetchrow_hashref() )
	{
		if ( $ref2->{'CountryID'} eq $ref->{'Country'} )
		{
			print "<option value=$ref2->{'CountryID'} selected>$ref2->{'CountryText'}</option>";
		}
		else
		{
			print "<option value=$ref2->{'CountryID'}>$ref2->{'CountryText'}</option>";
		}
	}
	$sth2->finish();
	print "</select></td></tr>";

	print <<"__END__";
		<tr><td>&nbsp;</td></tr>
		<tr><td>Telephone:</td><td><input type=text name=phone value="$ref->{'Phone'}" size=30></td></tr>
		<tr><td>Mobile:</td><td><input type=text name=mobile value="$ref->{'Mobile'}" size=30></td></tr>
		<tr><td>Fax:</td><td><input type=text name=fax value="$ref->{'Fax'}" size=30></td></tr>
		<tr><td>Email:</td><td><input type=text name=Email value="$ref->{'email'}" size=30></td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td>Notes:</td><td><textarea name=notes cols=60 rows=5>$ref->{'Notes'}</textarea></td></tr>
		<tr><td>&nbsp;</td></tr>
		<tr><td colspan=2 align=center><input type=submit value='$nextAction Contact' name='Add'> &nbsp; <input type=reset value='Clear Fields'></td></tr>
		</table>
	</td></tr>
__END__

	$sth->finish();
	$dbh->disconnect();
}

sub general
{
	# Select company detail from database
	my $dbh = DBI->connect("DBI:mysql:database=accounts;host=localhost","$DBUSER","$DBPASS") || die "Unable to connect to database";
	my $sth = $dbh->prepare("SELECT * FROM CustomerContacts WHERE CoID=$CoID");
	$sth->execute();
	while ( my $ref = $sth->fetchrow_hashref() )
	{
		$name=$ref->{'Name'};
		$add1=$ref->{'Address1'};
		$add2=$ref->{'Address2'};
		$add3=$ref->{'Address3'};
		$town=$ref->{'TownCity'};
		$county=$ref->{'County'};
		$pcode=$ref->{'Postcode'};
		$country=$ref->{'Country'};
		$phone=$ref->{'Phone'};
		$mobile=$ref->{'Mobile'};
		$fax=$ref->{'Fax'};
		$notes=$ref->{'Notes'};
	}
	$sth->finish();

	my $sth = $dbh->prepare("SELECT * FROM CustomerContacts WHERE CoID=$CoID");
	$sth->execute();
	$ref=$sth->fetchrow_hashref();
	$coname=$ref->{'CompanyName'};
	$sth->finish();
	$dbh->disconnect();
}

print header();
print <<"__END__";

<html>
<head>
<title>$COMPANYNAME, Accounting System for Invoicing, Company Details</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

# include header file
open (INCFILE, "<../include/companies.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

if ( "$DoWhat" eq "Display" )
{
	general;
	displayDetails;
}
elsif ( "$DoWhat" eq "Edit" )
{
	my $nextAction=param("DoNext");
	general;
	editForm($nextAction);
}
elsif ( "$DoWhat" eq "Update")
{
	general;
	updateContact;
}
elsif ( "$DoWhat" eq "Add")
{
	general;
	addContact;
}
elsif ( "$DoWhat" eq "Delete" )
{
	general;
	deleteContact;
}
elsif ("$DoWhat" eq "New")
{
	my $nextAction=param("DoNext");
	general;
	editForm($nextAction);
}
else
{
	listContacts;
}

print <<"__END__";
</body>
</html>
__END__
