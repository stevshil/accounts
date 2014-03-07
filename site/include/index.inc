<script language = "javascript">
<!--

function LmOver(elem, clr)
{elem.style.backgroundColor = clr;
elem.style.cursor = 'hand'}

function LmOut(elem, clr)
{elem.style.backgroundColor = clr;}

function LmDown(elem, clr)
{elem.style.backgroundColor = clr;}

function LmUp(path)
{location.href = path;}

//-->
</script>
</head>
<body>
<table width="90%" align=center>
<tr><td colspan=2 align=center class=header>$COMPANYNAME Invoicing System</td></tr>
<tr><td colspan=2 align=center>Logged in as: $LOGNAME</td></tr>
<tr><td colspan=2 align=center>&nbsp;</td></tr>
<tr><td width=220 valign=top>
	<TABLE border=0 cellPadding=0 cellSpacing=0 width=180>
        <TBODY>
        <TR><TD colSpan=3><IMG border=0 height=29 src="../images/boxtop.gif" width=180></TD></TR>
        <TR><TD width=17><img src='../images/boxside1.gif' height="220" width="21"></TD>
            <TD bgColor=#ffffff vAlign=top align=left><FONT face=Verdana size=1><IMG height=9 src="../images/arrow.gif" width=9> <FONT class=smallhead color=#363636><B>Main Menu</B></FONT><br>
		<table border="0" cellspacing="1" cellpadding="1" width=130>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('index.htm')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="index.htm" Class="navlink">Home</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('companies.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="companies.cgi" Class="navlink">Manage Companies</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('invoicing.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="invoicing.cgi" Class="navlink">Invoicing</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('payments.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="payments.cgi" Class="navlink">Payments</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('reporting.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="reporting.cgi" Class="navlink">Reporting</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('management.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="management.cgi" Class="navlink">Management</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('help.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="help.cgi" Class="navlink">Help</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('about.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="about.cgi" Class="navlink">About</a></td></tr>
		</table>
	</TD>
        <TD width=17><img src='../images/boxside2.gif' height="220" width="23"></TD></TR>
	<TR><TD colSpan=3><FONT face=Verdana size=1><IMG border=0 height=21 src="../images/boxbottom.gif" width=180></FONT></TD> </TR>
	</TBODY>
        </TABLE>
</td><td align=left valign=top>Accounting system created by Steve Shilling 2005 of TPS Services Ltd.<br><br>This software can be used to create invoices in different currencies and enables reprinting of invoice once UK values are known.  It will also allow the generation of Invoices in other currencies.<br><br>This software also allows for simple reporting on companies and who takes too long to pay.<br><br>This software is intended to make creating invoices simple and quick, and with a web based front end, Apache web server and mySQL database makes it a cheap viable to a lot of other expensive invoicing systems for small businesses.</td></tr>
</table>
</body>

</html>
