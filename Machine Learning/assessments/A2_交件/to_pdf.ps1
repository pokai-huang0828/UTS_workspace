$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$docx = Join-Path $here "Huang_26254793_321513_A2.docx"
$pdf  = Join-Path $here "Huang_26254793_321513_A2.pdf"
$log  = Join-Path $here "to_pdf.log"
"start" | Out-File $log
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
"word started" | Out-File $log -Append
try {
  $d = $word.Documents.Open($docx, $false, $false, $false)
  "opened" | Out-File $log -Append
  $n = $d.TablesOfContents.Count
  "toc count $n" | Out-File $log -Append
  if ($n -gt 0) { $d.TablesOfContents.Item(1).Update() }
  "toc updated" | Out-File $log -Append
  $d.ExportAsFixedFormat($pdf, 17)
  "exported" | Out-File $log -Append
  ("pages: " + $d.ComputeStatistics(2)) | Out-File $log -Append
  ("words: " + $d.ComputeStatistics(0)) | Out-File $log -Append
  ("asian: " + $d.ComputeStatistics(6)) | Out-File $log -Append
  $d.SaveAs2($docx, 16)
  "saved" | Out-File $log -Append
  $d.Close(0)
} catch { ("ERROR " + $_.Exception.Message) | Out-File $log -Append }
finally { $word.Quit(); "quit" | Out-File $log -Append }
