---
title: Dotnet build troubleshooting notes
tags:
  - dotnet
categories:
  - Troubleshooting
date: 2021-09-28 13:43:42
author: shenxianpeng
---

## Problem 1

Unable to find package NETStandard.Library

### Solution

https://stackoverflow.com/questions/63633435/unable-to-find-package-netstandard-library

## Problem 2

C:\Program Files (x86)\MSBuild\12.0\bin\Microsoft.Common.CurrentVersion.targets(2151,5): warning MSB3283: Cannot find wrapper assembly for type library "EnvDTE100". Verify that (1) the COM component is registered correctly and (2) your target platform is the same as the bitness of the COM component. For example, if the COM component is 32-bit, your target platform must not be 64-bit.

### Solution

https://developercommunity.visualstudio.com/t/cannot-find-wrapper-assembly-for-type-library-envd/15434#T-N16833

"C:\dotnet\Developer\dotfuscator\Build\Obfuscator.proj" (default target) (1) ->
"C:\dotnet\Developer\dotfuscator\Developer_Dotfuscator\Developer_Dotfuscator.dotfuproj" (clean;rebuild target) (2) ->
  C:\dotnet\Developer\dotfuscator\Developer_Dotfuscator\Developer_Dotfuscator.dotfuproj(32,3): error MSB4019: The impor
ted project "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\MSBuild\PreEmptive\Dotfuscator\4.0\PreEmp
tive.Dotfuscator.Targets" was not found. Confirm that the expression in the Import declaration "C:\Program Files (x86)\
Microsoft Visual Studio\2019\Professional\MSBuild\PreEmptive\Dotfuscator\4.0\PreEmptive.Dotfuscator.Targets" is correct
, and that the file exists on disk.

"C:\dotnet\Plus\BuildPlus\PlushBuild.proj" (default target) (1) ->
"C:\dotnet\Plus\src\VSPackage\VSPackage.csproj" (clean;rebuild target) (9) ->
  C:\dotnet\Plus\src\VSPackage\VSPackage.csproj(322,11): error MSB4226: The imported project "C:\Program Files (x8
6)\Microsoft Visual Studio\2019\Professional\MSBuild\Microsoft\VisualStudio\v16.0\VSSDK\Microsoft.VsSDK.targets" was not fo
und. Also, tried to find "VSSDK\Microsoft.VsSDK.targets" in the fallback search path(s) for $(VSToolsPath) - "C:\Program Fi
les (x86)\MSBuild\Microsoft\VisualStudio\v16.0" . These search paths are defined in "C:\Program Files (x86)\Microsoft Visua
l Studio\2019\Professional\MSBuild\Current\Bin\MSBuild.exe.Config". Confirm that the path in the <Import> declaration is co
rrect, and that the file exists on disk in one of the search paths.
