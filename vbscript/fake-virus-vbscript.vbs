' Write this code first-
' X=MsgBox("Message Description",0+16,"Title") 

' 1.  You can write any number from 1,2,3 or 4 instead of 0 (before the '+' symbol) 
' Below is the meaning of these numbers:

' 0 = OK Button, 
' 1 = OK / Cancel Button, 
' 2 = Abort / Retry / Ignore Button, 
' 3 = Yes / No / Cancel Button, 
' 4 = Yes / No Button, 
' 5 = Retry / Cancel Button

' 2.  You can write 32 or 48 or 64 instead of 16.
' Below is the meaning of each number:

' 16 = Critical Icon, 
' 32 = Help Icon, 
' 48 = Warning Icon, 
' 64 = Information Icon,

' Code

X=MsgBox("Do You want to open",4+32,"Virus") 
X=MsgBox("Do Really to open",3+64,"Virus") 
X=MsgBox("Opening...",0+16,"Virus") 
X=MsgBox("a Virus found. Do you want to delete it",4+64,"Virus") 
X=MsgBox("Deleting...",0+16,"Virus") 
X=MsgBox("Cant delete deleting system32...",0+48,"Virus") 
X=MsgBox("Computer Hacked",0+16,"Virus") 
X=MsgBox("It was a prank",0+64,"Virus") 
