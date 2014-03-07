<script language = "javascript">
<!--

function LmOver(elem, clr)
{elem.style.backgroundColor = clr;
elem.style.cursor = 'hand'}
//elem.children.tags('A')[0].style.color = "#FF3300";

function LmOut(elem, clr)
{elem.style.backgroundColor = clr;}
//elem.children.tags('A')[0].style.color = "#FF0000";}

function LmDown(elem, clr)
{elem.style.backgroundColor = clr;}
//elem.children.tags('A')[0].style.color = "#FF3300";}

function LmUp(path)
{location.href = path;}

//-->
</script>
</head>
<body>
<table width="90%" align=center>
<tr><td colspan=2 align=center class=header>$COMPANYNAME Invoicing System</td></tr>
<tr><td colspan=2 align=center>Logged in as: $LOGNAME</td></tr>
<tr><td width=220 valign=top>
	<TABLE border=0 cellPadding=0 cellSpacing=0 width=180>
        <TBODY>
        <TR><TD colSpan=3><IMG border=0 height=29 src="../images/boxtop.gif" width=180></TD></TR>
        <TR><TD width=17><img src='../images/boxside1.gif' height="220" width="21"></TD>
            <TD bgColor=#ffffff vAlign=top align=left><FONT face=Verdana size=1><IMG height=9 src="../images/arrow.gif" width=9> <FONT class=smallhead color=#363636><B>Main Menu</B></FONT><br>
		<table border="0" cellspacing="1" cellpadding="1" width=130>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('../index.htm')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="../index.htm" Class="navlink">Home</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('../companies/list.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="../companies/list.cgi" Class="navlink">List / Edit</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('../companies/add.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="../companies/add.cgi" Class="navlink">Add</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('../companies/remove.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="../companies/remove.cgi" Class="navlink">Delete</a></td></tr>
		<tr><td class='navlink'>&nbsp;</td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('../main/invoicing.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="../main/invoicing.cgi" Class="navlink">Invoicing</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('../main/reporting.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="../main/reporting.cgi" Class="navlink">Reporting</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('../main/management.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="../main/management.cgi" Class="navlink">Management</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('../main/help.cgi')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="../main/help.cgi" Class="navlink">Help</a></td></tr>
		<tr><td onMouseover="LmOver(this, '#99FFFF')" onMouseout="LmOut(this, '#ffffFF')" onMouseDown="LmDown(this, '#99FFFF')" onMouseUp="LmUp('../about.htm')" bgcolor="#ffffff"><IMG height=8 src="../images/bulletbb.gif" width=8><A HREF="../about.htm" Class="navlink">About</a></td></tr>
		</table>
	</TD>
        <TD width=17><img src='../images/boxside2.gif' height="220" width="23"></TD></TR>
	<TR><TD colSpan=3><FONT face=Verdana size=1><IMG border=0 height=21 src="../images/boxbottom.gif" width=180></FONT></TD> </TR>
	</TBODY>
        </TABLE></td>
