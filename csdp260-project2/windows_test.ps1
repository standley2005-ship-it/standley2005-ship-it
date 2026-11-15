$ErrorActionPreference = "Stop"
$project = Join-Path $PSScriptRoot "build\Calculator.exe"
$evidence = Join-Path $PSScriptRoot "evidence"
New-Item -ItemType Directory -Force $evidence | Out-Null
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
using System.Text;
public static class NativeWin {
 [DllImport("user32.dll",CharSet=CharSet.Ansi)] public static extern IntPtr FindWindow(string c,string n);
 [DllImport("user32.dll")] public static extern IntPtr GetDlgItem(IntPtr h,int id);
 [DllImport("user32.dll",CharSet=CharSet.Ansi)] public static extern bool SetWindowText(IntPtr h,string t);
 [DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h,int m,IntPtr w,IntPtr l);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h,IntPtr hdc,uint flags);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out RECT rect);
 [DllImport("user32.dll",CharSet=CharSet.Ansi)] public static extern int GetWindowText(IntPtr h,StringBuilder t,int max);
 [DllImport("user32.dll",CharSet=CharSet.Ansi)] public static extern IntPtr FindWindowEx(IntPtr parent,IntPtr after,string name,string title);
 [StructLayout(LayoutKind.Sequential)] public struct RECT {public int L,T,R,B;}
}
'@
$proc = Start-Process -FilePath $project -PassThru
try {
 $w=[IntPtr]::Zero
 for($i=0;$i -lt 25;$i++){
   Start-Sleep -Milliseconds 400
   $w=[NativeWin]::FindWindow("CSDP260NASMCalc","CSDP 260 - NASM Assembly Calculator")
   if($w -ne [IntPtr]::Zero){ break }
   if($proc.HasExited){throw "Calculator exited with code $($proc.ExitCode)"}
 }
 if($w -eq [IntPtr]::Zero){ throw "GUI window not found" }
 $one=[NativeWin]::GetDlgItem($w,301)
 $two=[NativeWin]::GetDlgItem($w,302)
 if($one -eq [IntPtr]::Zero -or $two -eq [IntPtr]::Zero){throw "Input fields not found"}
 function Snapshot([string] $name){
  $rect=New-Object NativeWin+RECT
  [NativeWin]::GetWindowRect($w,[ref]$rect) | Out-Null
  $width=[Math]::Max(610,$rect.R-$rect.L)
  $height=[Math]::Max(350,$rect.B-$rect.T)
  $bmp=New-Object System.Drawing.Bitmap($width,$height)
  $g=[System.Drawing.Graphics]::FromImage($bmp)
  $hdc=$g.GetHdc()
  try { $ok=[NativeWin]::PrintWindow($w,$hdc,2) }
  finally { $g.ReleaseHdc($hdc) }
  if(-not $ok){throw "PrintWindow failed for $name"}
  $bmp.Save((Join-Path $evidence "$name.png"),[System.Drawing.Imaging.ImageFormat]::Png)
  $g.Dispose();$bmp.Dispose()
 }
 function ResultAndStatus{
  $strings=@()
  $cur=[IntPtr]::Zero
  while($true){
    $cur=[NativeWin]::FindWindowEx($w,$cur,"STATIC",$null)
    if($cur -eq [IntPtr]::Zero){break}
    $buf=New-Object System.Text.StringBuilder 1000
    [void][NativeWin]::GetWindowText($cur,$buf,$buf.Capacity)
    $strings+= $buf.ToString()
  }
  return ($strings -join " | ")
 }
 $tests=@(
   @{id="01-add"; first="10";second="5"; button=101;expected="15"},
   @{id="02-subtract";first="20";second="8";button=102;expected="12"},
   @{id="03-multiply";first="6";second="4";button=103;expected="24"},
   @{id="04-divide";first="15";second="2";button=104;expected="7.5"},
   @{id="05-zero-divisor";first="10";second="0";button=104;expected="Cannot divide by zero."},
   @{id="06-invalid-input";first="abc";second="3";button=101;expected="Invalid input."}
 )
 $results=@()
 Snapshot "00-start"
 foreach($case in $tests){
  $was1=[NativeWin]::SetWindowText($one,$case.first)
  $was2=[NativeWin]::SetWindowText($two,$case.second)
  $inputText1=New-Object System.Text.StringBuilder 500
  $inputText2=New-Object System.Text.StringBuilder 500
  [void][NativeWin]::GetWindowText($one,$inputText1,$inputText1.Capacity)
  [void][NativeWin]::GetWindowText($two,$inputText2,$inputText2.Capacity)
  Write-Host "TEST $($case.id) SET1=$was1 SET2=$was2 INPUT1=($($inputText1.ToString())) INPUT2=($($inputText2.ToString()))"
  [void][NativeWin]::SendMessage($w,273,[IntPtr]$case.button,[IntPtr]::Zero)
  Start-Sleep -Milliseconds 450
  Snapshot $case.id
  $text=ResultAndStatus
  Write-Host "OBSERVED=$text EXPECTED=$($case.expected)"
  $match=$text.Contains($case.expected)
  $results += [PSCustomObject]@{Case=$case.id;Input1=$case.first;Input2=$case.second;Expected=$case.expected;Observed=$text;Pass=$match}
 }
 $results | Export-Csv -NoTypeInformation -Path (Join-Path $evidence "verified_test_results.csv")
 if(($results | Where-Object {-not $_.Pass}).Count -gt 0){throw "Calculator returned incorrect values in one or more GUI tests"}
 [void][NativeWin]::SendMessage($w,273,[IntPtr]105,[IntPtr]::Zero)
 Start-Sleep -Milliseconds 250
 Snapshot "07-clear"
 Write-Host "SUCCESS: GUI launched and tests passed"
} finally {
 if(-not $proc.HasExited){$proc.CloseMainWindow() | Out-Null;Start-Sleep -Milliseconds 500}
 if(-not $proc.HasExited){Stop-Process -Id $proc.Id -Force}
}
