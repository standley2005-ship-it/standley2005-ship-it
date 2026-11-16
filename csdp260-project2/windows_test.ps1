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
 [DllImport("user32.dll",EntryPoint="SendMessageA",CharSet=CharSet.Ansi)] public static extern IntPtr ReadText(IntPtr h,int m,IntPtr length,StringBuilder text);
 [DllImport("user32.dll",CharSet=CharSet.Ansi)] public static extern IntPtr FindWindow(string c,string n);
 [DllImport("user32.dll")] public static extern IntPtr GetDlgItem(IntPtr h,int id);
 [DllImport("user32.dll")] public static extern uint GetDlgItemInt(IntPtr h,int id,out bool ok,bool signed);
 [DllImport("user32.dll",CharSet=CharSet.Ansi)] public static extern bool SetWindowText(IntPtr h,string t);
 [DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h,int m,IntPtr w,IntPtr l);
 [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h,uint m,IntPtr w,IntPtr l);
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h,IntPtr hdc,uint flags);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h,out RECT rect);
 [DllImport("user32.dll",CharSet=CharSet.Ansi)] public static extern int GetWindowText(IntPtr h,StringBuilder t,int max);
 [DllImport("user32.dll",CharSet=CharSet.Ansi)] public static extern IntPtr FindWindowEx(IntPtr parent,IntPtr after,string name,string title);
 [DllImport("user32.dll")] public static extern IntPtr GetWindow(IntPtr h,uint cmd);
 [DllImport("user32.dll",CharSet=CharSet.Ansi)] public static extern int GetClassName(IntPtr h,StringBuilder b,int max);
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
 Write-Host "EXTERNAL HANDLES: PARENT=$($w.ToInt64()) INPUT1=$($one.ToInt64()) INPUT2=$($two.ToInt64())"
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
  $cur=[NativeWin]::GetWindow($w,5)
  while($cur -ne [IntPtr]::Zero){
    $buf=New-Object System.Text.StringBuilder 1000
    $cl=New-Object System.Text.StringBuilder 128
    [void][NativeWin]::ReadText($cur,0x000D,[IntPtr]$buf.Capacity,$buf)
    [void][NativeWin]::GetClassName($cur,$cl,$cl.Capacity)
    $strings+= "$($cl.ToString()):$($buf.ToString())"
    $cur=[NativeWin]::GetWindow($cur,2)
  }
  return ($strings -join " | ")
 }
 function ControlText([int] $id){
  $handle=[NativeWin]::GetDlgItem($w,$id)
  if($handle -eq [IntPtr]::Zero){throw "Missing control $id"}
  $buf=New-Object System.Text.StringBuilder 1000
  [void][NativeWin]::ReadText($handle,0x000D,[IntPtr]$buf.Capacity,$buf)
  return $buf.ToString()
 }
 $tests=@(
   @{id="01-add"; first="10";second="5"; button=101;expected="15"},
   @{id="02-subtract";first="20";second="8";button=102;expected="12"},
   @{id="03-multiply";first="6";second="4";button=103;expected="24"},
   @{id="04-divide";first="15";second="2";button=104;expected="7.5"},
   @{id="05-zero-divisor";first="10";second="0";button=104;expected="Cannot divide by zero."},
   @{id="06-invalid-input";first="abc";second="3";button=101;expected="Invalid input."},
   @{id="07-negative-subtract";first="10";second="25";button=102;expected="-15"},
   @{id="08-negative-add";first="-10";second="5";button=101;expected="-5"},
   @{id="09-fraction";first="1";second="3";button=104;expected="0.3333"},
   @{id="10-negative-fraction";first="-1";second="2";button=104;expected="-0.5"},
   @{id="11-empty";first="";second="4";button=101;expected="Please enter both numbers."},
   @{id="12-zero-result";first="5";second="5";button=102;expected="0"},
   @{id="13-out-of-range";first="2147483648";second="1";button=101;expected="Out of range:"}
 )
 $results=@()
 Snapshot "00-start"
 foreach($case in $tests){
  # Clear from the application's own GUI thread before each new test.
  $cleared=[NativeWin]::PostMessage($w,273,[IntPtr]105,[IntPtr]::Zero)
  if(-not $cleared){ throw "Could not clear previous inputs" }
  Start-Sleep -Milliseconds 200
  # Actual WM_CHAR editing, instead of remote SetWindowText.
  foreach($ch in $case.first.ToCharArray()) {
    [void][NativeWin]::PostMessage($one,0x0102,[IntPtr][int]$ch,[IntPtr]1)
  }
  foreach($ch in $case.second.ToCharArray()) {
    [void][NativeWin]::PostMessage($two,0x0102,[IntPtr][int]$ch,[IntPtr]1)
  }
  Start-Sleep -Milliseconds 350
  $inputText1=New-Object System.Text.StringBuilder 500
  $inputText2=New-Object System.Text.StringBuilder 500
  [void][NativeWin]::ReadText($one,0x000D,[IntPtr]$inputText1.Capacity,$inputText1)
  [void][NativeWin]::ReadText($two,0x000D,[IntPtr]$inputText2.Capacity,$inputText2)
  Write-Host "TEST $($case.id) INPUT1=($($inputText1.ToString())) INPUT2=($($inputText2.ToString()))"
  Snapshot "$($case.id)-before"
  $button=[NativeWin]::GetDlgItem($w,$case.button)
  if($button -eq [IntPtr]::Zero){ throw "Operation button missing: $($case.button)" }
  # Queue normal WM_COMMAND for the GUI thread instead of nested cross-process SendMessage
  $posted=[NativeWin]::PostMessage($w,273,[IntPtr]$case.button,$button)
  if(-not $posted){ throw "PostMessage failed for $($case.id)" }
  Start-Sleep -Milliseconds 450
  $after1=New-Object System.Text.StringBuilder 500
  $after2=New-Object System.Text.StringBuilder 500
  [void][NativeWin]::ReadText($one,0x000D,[IntPtr]$after1.Capacity,$after1)
  [void][NativeWin]::ReadText($two,0x000D,[IntPtr]$after2.Capacity,$after2)
  Write-Host "AFTER INPUT1=($($after1.ToString())) INPUT2=($($after2.ToString()))"
  Snapshot $case.id
  $text=ResultAndStatus
  Write-Host "OBSERVED=$text EXPECTED=$($case.expected)"
  $expectedError=$case.id -in @('05-zero-divisor','06-invalid-input','11-empty','13-out-of-range')
  $observedResult=ControlText 303
  $observedStatus=ControlText 304
  $inputsMatch=((ControlText 301) -ceq $case.first) -and ((ControlText 302) -ceq $case.second)
  if($expectedError){
    $match=($observedResult -ceq '') -and $observedStatus.StartsWith($case.expected)
  } else {
    $match=($observedResult -ceq $case.expected)
  }
  $match=$match -and $inputsMatch
  $results += [PSCustomObject]@{Case=$case.id;Input1=$case.first;Input2=$case.second;Expected=$case.expected;Observed=$text;Pass=$match}
 }
 [void][NativeWin]::PostMessage($w,273,[IntPtr]105,[IntPtr]::Zero)
 Start-Sleep -Milliseconds 250
 Snapshot "14-clear"
 $clearOK=((ControlText 301) -ceq '') -and ((ControlText 302) -ceq '') -and ((ControlText 303) -ceq '') -and ((ControlText 304) -ceq 'Ready. Enter two whole numbers.')
 $results += [PSCustomObject]@{Case='14-clear';Input1='';Input2='';Expected='Empty inputs/result; Ready. Enter two whole numbers.';Observed=(ResultAndStatus);Pass=$clearOK}
 [void][NativeWin]::PostMessage($w,273,[IntPtr]106,[IntPtr]::Zero)
 $exitOK=$proc.WaitForExit(5000)
 if($exitOK){$exitOK=$proc.ExitCode -eq 0}
 $results += [PSCustomObject]@{Case='15-exit';Input1='';Input2='';Expected='Process exits with code 0';Observed="Exited=$exitOK";Pass=$exitOK}
 $results | Export-Csv -NoTypeInformation -Path (Join-Path $evidence "verified_test_results.csv")
 if(($results | Where-Object {-not $_.Pass}).Count -gt 0){throw "Calculator returned incorrect values in one or more GUI tests"}
 Write-Host "SUCCESS: GUI launched and all 15 tests passed"

} finally {
 if(-not $proc.HasExited){$proc.CloseMainWindow() | Out-Null;Start-Sleep -Milliseconds 500}
 if(-not $proc.HasExited){Stop-Process -Id $proc.Id -Force}
}
