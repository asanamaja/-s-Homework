# 앵커 윈드라스 유압회로

사진의 선박 앵커(양묘기) 유압회로를 [MechSimulator Hydraulic Circuit](https://mechsimulator.com/tools/hydraulic-circuit/)에서 바로 돌릴 수 있는 파일입니다.

파일: `anchor-windlass.json`

## 불러오기

1. https://mechsimulator.com/tools/hydraulic-circuit/ 를 연다.
2. 캔버스 위 도구막대에서 **Import** 를 누른다.
3. `anchor-windlass.json` 을 고른다.
4. 이미 회로가 있으면 바꾸겠다는 확인을 누른다.
5. 화면이 잘리면 **Fit** 버튼 또는 `Ctrl+1`.

## 시험 순서

불러온 직후 밸브는 그림의 스프링 위치다. 절환밸브(Changeover)는 **To anchor** 쪽이다.

| 조작 | 결과 |
| --- | --- |
| **Run Circuit** (또는 Space) | 오른쪽 앵커 모터가 돈다. 약 100 bar, 36 L/min, 토크 45 N·m, 약 1070 rpm. |
| `E` | 절환밸브가 윈드라스 쪽, 슬라이드 밸브는 권상, 분배밸브 두 개가 열린다. 모터 1·2·3이 돈다. 압력 약 89 bar, 모터 1은 약 855 rpm. |
| 슬라이드 밸브의 오른쪽 칸만 클릭 | `E` 로 윈드라스에 유량을 준 뒤, 슬라이드만 Retract 로 두면 하강이다. 카운터밸런스(90 bar)를 지나 모터가 반대 방향으로 돈다. `R` 키는 절환밸브까지 앵커 쪽으로 되돌리므로 하강에는 쓰지 않는다. |
| `C` | 슬라이드는 중립. 절환밸브는 스프링으로 **To anchor** 에 돌아간다. |
| 분배밸브 오른쪽 칸 클릭 (Closed) | 모터 2(No.1) 또는 모터 3(No.2)이 빠진다. 모터 1만 남으면 유량을 혼자 받아 회전수가 올라간다. |

밸브를 누르는 위치: 4/3 슬라이드는 왼쪽 Extend, 가운데 Center, 오른쪽 Retract. 4/2 절환밸브는 왼쪽이 윈드라스, 오른쪽이 To anchor.

## 그림과 심볼 대응

이 시뮬레이터에 없는 기호(전동기 M, 감속기 R/G, 사이트 글라스)는 아래처럼 묶었다.

| 그림 | 이 파일 |
| --- | --- |
| Hydraulic motor 1, 2, 3 | 위쪽 Hyd Motor 세 개. 배기량 20 cm³/rev, 부하 25 N·m |
| Lower limit & relief valve | 카운터밸런스 90 bar (하강 제한) + 릴리프 170 bar (모터 회로) |
| No. 1 distribution valve | DCV 3/2, 솔레노이드 + 스프링. 모터 2 투입 |
| No. 2 distribution valve | DCV 3/2, 파일럿 + 스프링. 모터 3 투입 |
| Slide valve | DCV 4/3 레버, 클로즈드 센터. 중립에서 모터 포트가 막힌다 |
| Changrover valve, To anchor | DCV 4/2 레버 + 스프링. 스프링 위치에서 오른쪽 앵커 모터로 주유 |
| Full flow filter | Filter. 펌프 토출측, 체크밸브 다음에 직렬 |
| Thermometer | Temp Gauge. 유량계 출구(절환밸브 입구)에 연결 |
| Hyd. pump, safety valve, nonreturn | Power Unit 200 bar / 36 L/min + 릴리프 150 bar + 체크밸브 |
| M, R/G | Power Unit 에 포함. 전동기와 감속기어 심볼은 없다 |
| Expansion tank | Reservoir 30 L (펌프 탱크 포트) |
| Filling tank, sight glass | Reservoir 80 L. 유면계 심볼은 없다 |
| Filling pump | Hand Pump 40 bar / 2 L/min + 체크밸브. 주펌프가 돌면 대기하고, 주펌프 유량이 0이 되면 보충한다 |

앵커 모터는 절환밸브 오른쪽의 Hyd Motor (32 cm³/rev, 45 N·m)다.

밸브 탱크 포트 옆의 작은 Reservoir 는 배관을 짧게 그리기 위한 반복 탱크 기호다. 오일 온도는 가장 큰 탱크(200 L) 기준으로 계산된다.

## 읽을 때 알아둘 점

- 파일럿 조작은 그림으로만 표시된다. 압력만으로 스풀이 움직이지 않으므로 분배밸브는 클릭하거나 `E`로 연다.
- 이 시뮬레이터는 회로 안의 **가장 낮은 릴리프**로 시스템 전체를 제한한다. 그래서 하강 제한은 릴리프를 낮춰 그리지 않고 카운터밸런스(90 bar)로 두었다. 펌프 안전밸브 150 bar가 상한이다.
- 모터 세 대는 병렬이다. 분배밸브가 열리면 모터 1이 유량의 절반을 받고, 모터 2와 3이 나머지를 나눈다. 같은 축으로 기계적으로 묶인 모델은 아니다.
- 고장 드롭다운(펌프 고장, 필터 막힘, 오일 과열 등)과 온도계로 사진의 필터·온도 감시를 이어서 볼 수 있다.
