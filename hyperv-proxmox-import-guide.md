# Hyper-V Proxmox VM 불러오기 절차

이 문서는 Proxmox VM zip 파일을 아래 위치에 압축 해제한 상태를 기준으로 합니다.

```text
바탕화면\a
```

현재 `a` 폴더 안에 아래 폴더들이 있는 상태입니다.

```text
a
├─ Snapshots
├─ Virtual Hard Disks
└─ Virtual Machines
```

목표는 **압축 해제한 원본 `.vhdx` / `.avhdx` 체크포인트 체인은 건드리지 않고**, `a` 폴더 안에 새 작업 폴더를 만들어 `run.vhdx` 파일에만 변경분이 쌓이게 하는 것입니다.

## 주의사항

- `바탕화면\a` 안의 `.vhdx`, `.avhdx` 파일을 개별 삭제하지 마세요.
- 원본 `.avhdx`를 VM에 직접 붙여서 부팅하지 마세요.
- 이 복구용 VM에서는 Hyper-V 검사점을 켜지 마세요.
- `run.vhdx`는 VM을 켜면 커질 수 있습니다. 다만 원본 체크포인트 체인 파일이 아니라 `a\proxmox-work\run.vhdx`만 커지게 하는 방식입니다.

## 1. 관리자 PowerShell 열기

시작 메뉴에서 PowerShell을 검색한 뒤 **관리자 권한으로 실행**합니다.

## 2. 경로 변수 설정

아래 명령어는 현재 Windows 사용자의 바탕화면 경로를 자동으로 잡습니다. 바탕화면이 OneDrive로 연결된 경우에도 보통 자동으로 맞습니다.

```powershell
$Original = Join-Path ([Environment]::GetFolderPath("Desktop")) "a"
$Work = Join-Path $Original "proxmox-work"
$RunDisk = Join-Path $Work "run.vhdx"

$Original
$Work
$RunDisk
```

출력된 `$Original` 경로가 `Snapshots`, `Virtual Hard Disks`, `Virtual Machines`가 들어있는 `a` 폴더인지 확인합니다.

## 3. 최신 `.avhdx` 찾기

먼저 최신 `.avhdx` 목록을 확인합니다.

```powershell
Get-ChildItem $Original -Recurse -File |
Where-Object { $_.Extension -eq ".avhdx" } |
Sort-Object LastWriteTime -Descending |
Select-Object -First 20 LastWriteTime, @{Name="GB";Expression={[math]::Round($_.Length / 1GB, 2)}}, FullName
```

가장 최신 `.avhdx`를 부모 디스크로 저장합니다.

```powershell
$Parent = Get-ChildItem $Original -Recurse -File |
Where-Object { $_.Extension -eq ".avhdx" } |
Sort-Object LastWriteTime -Descending |
Select-Object -First 1

$Parent.FullName
```

출력이 비어 있으면 여기서 멈추고, 압축 해제한 VM에 체크포인트 파일이 실제로 있는지 다시 확인해야 합니다.

### 압축 해제로 날짜가 바뀐 경우 수동 지정

zip을 풀면서 모든 파일의 수정 시간이 압축 해제 시점으로 바뀌면, 위의 "최신 파일" 자동 선택이 틀릴 수 있습니다. 이 경우 파일 탐색기에서 실제로 사용할 `.avhdx` 경로를 확인한 뒤 직접 `$Parent`에 넣습니다.

예시:

```powershell
$ParentPath = "C:\Users\사용자이름\Desktop\a\Snapshots\실제사용할파일.avhdx"
$Parent = Get-Item $ParentPath
$Parent.FullName
```

바탕화면 경로를 자동으로 조합하려면 아래처럼 쓸 수도 있습니다.

```powershell
$ParentPath = Join-Path $Original "Snapshots\실제사용할파일.avhdx"
$Parent = Get-Item $ParentPath
$Parent.FullName
```

이후 단계의 `New-VHD -ParentPath $Parent.FullName` 명령은 그대로 사용합니다.

## 4. 새 변경 디스크 만들기

작업용 폴더를 만듭니다.

```powershell
New-Item -ItemType Directory -Path $Work -Force
```

최신 `.avhdx`를 부모로 하는 새 differencing disk를 만듭니다.

```powershell
New-VHD -Path $RunDisk -ParentPath $Parent.FullName -Differencing
```

이후 구조는 아래처럼 전부 `a` 폴더 안에서 처리됩니다.

```text
바탕화면\a\Snapshots              = 원본 체크포인트 보존
바탕화면\a\Virtual Hard Disks     = 원본 디스크 보존
바탕화면\a\Virtual Machines       = 원본 구성 파일 보존
바탕화면\a\proxmox-work\run.vhdx  = 새 변경분 저장
```

문제가 생기면 VM을 끄고 `run.vhdx`만 지운 뒤 다시 만들면 됩니다.

## 5. 이전 실패 VM 등록 제거

Hyper-V에 실패한 `Proxmox-VE` VM이 이미 있으면, VM 등록만 제거합니다.

```powershell
Stop-VM -Name "Proxmox-VE" -TurnOff -Force -ErrorAction SilentlyContinue
Remove-VMSavedState -VMName "Proxmox-VE" -ErrorAction SilentlyContinue
Remove-VM -Name "Proxmox-VE" -Force -ErrorAction SilentlyContinue
```

이 명령은 압축 해제한 `바탕화면\a` 폴더를 삭제하지 않습니다.

## 6. `run.vhdx`로 새 Hyper-V VM 만들기

PowerShell에서 새 VM을 만듭니다.

```powershell
New-VM `
  -Name "Proxmox-VE" `
  -Generation 2 `
  -MemoryStartupBytes 8GB `
  -VHDPath $RunDisk
```

호스트 메모리가 부족하면 `8GB` 대신 `4GB`처럼 낮춰도 됩니다.

## 7. 첫 부팅 전 검사점과 보안 부팅 끄기

반드시 VM을 시작하기 전에 아래를 실행합니다.

```powershell
Set-VM -Name "Proxmox-VE" -AutomaticCheckpointsEnabled $false
Set-VM -Name "Proxmox-VE" -CheckpointType Disabled
Set-VMFirmware -VMName "Proxmox-VE" -EnableSecureBoot Off
Set-VMProcessor -VMName "Proxmox-VE" -CompatibilityForMigrationEnabled $true
```

Hyper-V 관리자에서도 확인합니다.

- 설정 -> 검사점: 검사점 사용 안 함
- 설정 -> 보안: 보안 부팅 사용 안 함
- 설정 -> 펌웨어: 하드 디스크가 네트워크 부팅보다 위에 있음

## 8. 네트워크 없이 먼저 부팅

먼저 네트워크를 붙이지 않은 상태로 VM을 시작합니다.

```powershell
Start-VM -Name "Proxmox-VE"
```

부팅되면 원본 체크포인트/디스크 파일이 빠르게 커지지 않는지 확인합니다. 정상적으로는 주로 아래 파일이 커집니다.

```text
바탕화면\a\proxmox-work\run.vhdx
```

## 9. 부팅 안정 후 네트워크 연결

NAT 방식이면 Default Switch를 붙입니다.

```powershell
Connect-VMNetworkAdapter -VMName "Proxmox-VE" -SwitchName "Default Switch"
```

공유기/물리 LAN에 직접 붙는 브리지 방식이 필요하면 Hyper-V 관리자에서 External Switch를 만들고 연결합니다.

```powershell
Connect-VMNetworkAdapter -VMName "Proxmox-VE" -SwitchName "External Switch"
```

`External Switch` 부분은 실제 만든 스위치 이름으로 바꿉니다.

## 10. 이번 시도 변경분만 초기화하기

이번 부팅 시도를 버리고 처음 상태로 되돌리고 싶으면, VM을 끄고 `run.vhdx`만 다시 만듭니다.

```powershell
Stop-VM -Name "Proxmox-VE" -TurnOff -Force
Remove-VM -Name "Proxmox-VE" -Force
Remove-Item $RunDisk -Force
New-VHD -Path $RunDisk -ParentPath $Parent.FullName -Differencing
```

그 다음 6번부터 다시 진행합니다.

## 예상 동작

- VM을 켜면 `run.vhdx`는 커질 수 있습니다.
- 원본 `바탕화면\a\Snapshots`, `바탕화면\a\Virtual Hard Disks`, `바탕화면\a\Virtual Machines`는 체크포인트 원본 체인으로 보존합니다.
- 새 변경분은 `바탕화면\a\proxmox-work\run.vhdx`에 저장합니다.
- C드라이브 여유 공간이 부족하면 부팅 전에 먼저 공간을 확보해야 합니다.

## 11. 사용한 PowerShell 변수 정리

작업이 끝난 뒤 현재 PowerShell 창에서 사용한 변수를 지우고 싶으면 아래를 실행합니다.

```powershell
Remove-Variable Original, Work, RunDisk, Parent, ParentPath -ErrorAction SilentlyContinue
```

이 명령은 PowerShell 변수만 지우며, VM 파일이나 디스크 파일은 삭제하지 않습니다.
