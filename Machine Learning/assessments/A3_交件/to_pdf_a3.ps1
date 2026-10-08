$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$docx = Join-Path $here "Huang_26254793_321513_A3.docx"
$pdf  = Join-Path $here "Huang_26254793_321513_A3.pdf"
$log  = Join-Path $here "to_pdf_a3.log"
$docx = [string]$docx; $pdf = [string]$pdf
"start" | Out-File $log -Encoding utf8
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
"word started" | Out-File $log -Append -Encoding utf8
try {
  $d = $word.Documents.Open($docx, $false, $false, $false)
  "opened" | Out-File $log -Append -Encoding utf8
  $n = $d.TablesOfContents.Count
  "toc count $n" | Out-File $log -Append -Encoding utf8
  if ($n -gt 0) { $d.TablesOfContents.Item(1).Update() }
  "toc updated" | Out-File $log -Append -Encoding utf8
  $d.Fields.Update() | Out-Null
  $d.ExportAsFixedFormat($pdf, 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $false)
  "exported" | Out-File $log -Append -Encoding utf8
  ("pages: " + $d.ComputeStatistics(2)) | Out-File $log -Append -Encoding utf8
  $d.SaveAs2($docx, 16)
  "saved" | Out-File $log -Append -Encoding utf8
  $d.Close(0)
} catch { ("ERROR " + $_.Exception.Message) | Out-File $log -Append -Encoding utf8 }
finally { $word.Quit(); "quit" | Out-File $log -Append -Encoding utf8 }
