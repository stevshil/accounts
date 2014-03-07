#!/usr/bin/perl

use lib "../include";
use personalise;
use CGI ':standard';
use CGI::Carp 'fatalsToBrowser';

print header();

print <<"__END__";
<html>
<head>
<title>$COMPANYNAME, Accounting System</title>
<link rel="stylesheet" href="../main.css" type="text/css">
<link rel="stylesheet" href="../style.css" type="text/css">
__END__

open (INCFILE, "<../include/help.inc") || die "No such file";
my @INCFILE = <INCFILE>;
close INCFILE;
@INCFILE=doPersonalise(@INCFILE);
print "@INCFILE";

print <<"__END__";
	<td align=left valign=top><h1>Help on Invoicing</h1>
<h2>The main page</h2>
<p>When you select Invoicing from the main list you will be shown a page with the normal menu system and options for invoicing, as well as a list of unpaid invoices.<br>
If you click on one of the invoice numbers from the list you will have the following capabilities;
<ul><li>be shown the detail about that invoice
<li>be able to edit the invoice details, see later
<li>enter UK monetary amount for foreign invoices
<li>print or re-print the invoice
</ul>
<p>From the menu you have the options to view;
<ul><li>Unpaid invoices
<li>List or edit invoices in the sysem (regardless of date)
<li>Create invoices
<li>Print or re-print invoices
<li>Post an invoice once it is printed and has the UK monetary amount in it (see Posting)
<li>Reporting menu
</ul>
<hr>
<h2>Unpaid Invoices</h2>
<p>As mentioned above the Unpaid invoices list allows you to select an invoice number from the displayed list and view the details about that invoice as well as enter the UK monetary amount for foreign currency invoices, once the Bank has sent through the letter announcing the amounts.  You are also able to change details on the invoice provided it has not been posted.

<hr>
<h2>List / Edit</h2>
<p>This option will provide you with a numerical list of all invoices created in the system.<br>
You can view the details of an invoice by clicking on the Invoice number.  This will then allow you to;
<ul><li>view the invoice details
<li>Edit the invoice details provided the invoice has <b>not</b> been posted
<li>Enter a UK monetary amount for foreign invoices
<li>Print or re-print the invoice
</ul>
<p>There is no limit to the length of this list, yet.  This screen may change to ask for a date range when the system become bigger.

<hr>
<h2>Create Invoice</h2>
<p>By clicking on this option you will want to create an invoice for a company.  If the company is not in the <b>Company Name List</b> which is alphabetically sorted, then you will need to click on the <b>Home</b> option from the menu and then go to <b>Manage Companies</b> to add the new company, and also a contact for that company.
<p>The first screen to create invoice requests the following information;
<table>
<tr><td>Company Name</td><td>The company you wish to Invoice</td></tr>
<tr><td>Invoice Date</td><td>This automatically displays todays date, but allows you to modify it accordingly to future or back date invoices</td></tr>
<tr><td>Currency Type</td><td>This option should be changed from UK Sterling for invoices that need to be raised in a different currency.  Select the currency you require</td></tr>
<tr><td>Exchange Rate</td><td>The value for this defaults to 1.00 which should be left when invoicing in UK Sterling.<br>Change this value to 0.00 if you are invoicing in a different currency and you do not know the current exchange rate.<br>Change the value to the exchange rate if you do know what the rate is.  This will also take care of the exchange rate conversion for you later in the process</td></tr>
<tr><td>Category</td><td>Select the area that the invoice applies to in the business.  If not sure select <b>Other Income</b></td></tr>
</table>
<p>The <b>Clear Fields</b> button will reset the form to it's defaults.  If you are satisfied with the information click on <b>Add Detail</b> which will then allow you to enter the information about your invoice.
<h3>The Invoice Detail Screen</h3>
<p>First select your contact, which should have been entered in the <b>Manage Companies</b> screen.<br>
You will then see below <b>Invoice Detail</b> the various boxes to enter or select information from.<br>
The <b>Detail</b> box should contain information for one chargeable item, e.g. the delivery of a training course and details about it.  You can use the ENTER key for a new line whilst in the box, and don't worry about the text wrapping around.<br>
The <b>Qty</b> box should say how many of the items in the detail have been ordered, e.g. 5  if the course ran for 5 days, or 3  if the number of CD's ordered.<br>
The <b>Amount in Currency</b> box should be the unit amount for the item written in <b>Detail</b>.  So if you were charging &pound;600 per day for the course then 600.00 should be written in to the box.  Ideally this should be the amount excluding VAT, and should also be in the currency of the country you are invoicing (from the previous screen).  If you only know the amount including VAT, don't worry, that's what the tick box is for at the end.<br>
The <b>VAT Rate</b> selection allows you to specify the rate of tax to be added/subtracted from the currency amount.  Refer to the Inland Revenue for further details.<br>
Finally the <b>Tick if Amount Inc. VAT</b> should only be ticked if the amount entered in the <b>Amount in Currency</b> was a value including the VAT.
<p><br>If you have more items to enter, e.g. expenses, or what ever you should click on the <b>Add Detail</b> button and another row will appear for you to enter information.  You can continue doing this for every different item you need to enter.
<p>Once you have all the detail for your invoice click on <b>Create Invoice</b>.  The system will then add the information and display you back the <b>Invoice number</b>, the company you invoiced and the date of the invoice.
<p>To print the invoice you will need to go to the <b>Print</b> option in the menu.
<hr>
<h2>Print</h2>
<p>In this screen you will be provided with a list of Unpaid invoices.  A tick box is displayed for those invoices that have not been Posted.<br>
To print several invoices you will;
<ul><li>need to tick the boxes of the invoices to print
<li>click on the <b>Print Invoices</b> button
</ul>
<p>When you click on the Print Invoices button the system will then open several web pages with the Invoice in each new window.  Use the Web Browsers Print button to print the invoice, and then close that window.  Repeat for each invoice.
<p>If an invoice has been posted then the <b>Reprint</b> link appears next to the invoice.  Clicking on that link will open a new window with the printable invoice.  Click on the Web Browsers Print button to print that invoice.
<p>From this list you can also select the invoice number to view or modify invoice details.
<hr>
<h2>Post</h2>
<p>Once an invoice has been printed and sent to the customer, and as long as that invoice is in UK Sterling you should post it.<br>
<b>DO NOT</b> post invoices that are in a foreign currency without a UK Sterling amount being added to them.
<p>To post an invoice tick the box next to the invoice number for all the invoces you wish to post and then click on the <b>Post Invoices</b> button.<b>
The system will provide you with a report of those invoices that posted successfully.


</table>
</body>
</html>
__END__
