'Copies Spotlight images from Assets folder to "Pictures\Spotlight Collections"
'Picks up only the Landscape images, and having size >250KB.
'Filename: spotlight_collect.vbs © Ramesh Srinivasan - winhelponline.com
'For Windows 10 systems.
'Feel free to modify the script as you need.

Option Explicit
Dim objFSO : Set objFSO = CreateObject("Scripting.FileSystemObject")
Dim WshShell : Set WshShell = WScript.CreateObject("WScript.Shell")
Dim objFolder, oPic
Dim strAssetsFldr, strSpotlightFldr

strAssetsFldr = WshShell.ExpandEnvironmentStrings("%localappdata%") & _
"\Packages\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\LocalState\Assets"

strSpotlightFldr = WshShell.ExpandEnvironmentStrings("%userprofile%") & _ 
"\Pictures\Spotlight Collection"

If Not objFSO.FolderExists (strSpotlightFldr) Then objFSO.CreateFolder strSpotlightFldr
strSpotlightFldr = strSpotlightFldr & "\"

If objFSO.FolderExists (strAssetsFldr) Then   
   Set objFolder = objFSO.GetFolder(strAssetsFldr)   
   Dim file, iHeight, iWidth
   For Each file In objFolder.Files
      If objFSO.FileExists(strSpotlightFldr & file.Name & ".jpg") <> True _
         And LCase(file.Name) <> "thumbs.db" Then
         If file.Size > 250000 Then
            On Error Resume Next
            Set oPic = LoadPicture(file)
            'Skip pictures that can't be loaded
            If err.number = 0 Then
               iWidth = CInt(round(oPic.width / 26.4583))
               iHeight = CInt(round(oPic.height / 26.4583))
               'Lets copy only Landscape images of size >250KB
               If iHeight < iWidth Then
                  objFSO.CopyFile file, strSpotlightFldr & file.name & ".jpg", False
                  If err.number <> 0 And err.number <> 58 Then
                     WScript.Echo err.number & vbCrLf & err.Description
                  End If
               End If
            End If
            On Error GoTo 0
         End If
      End If
   Next
End If
