<STYLE>
#hideme {position:relative; visibility:visible;}
</STYLE>
<script>
function hidebtn()
{
	if ( navigator.appName != "Netscape" )
	{
		hideme.style.visibility='hidden';
	}
	else
	{
		// Firefox
		document.getElementById("hideme").style.display='none';

		// Old Netscape
		/*if ( document.hideme.visibility=='show' )
		{	
			document.hideme.visibility='hidden';
		}
		*/
	}
}
</script>
