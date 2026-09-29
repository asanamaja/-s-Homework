#!/usr/bin/env python3
"""Build the link catalog (Markdown + HTML) for the descriptive exam notes."""

ITEMS = [
    {
        "id": "Q01",
        "title": "쿨링 레인지 (Cooling range)",
        "links": [
            ("https://gallery-k.tistory.com/157", "글 중간의 ‘3-1 쿨링레인지’. 입구수온−출구수온, 표준 37℃→32℃=5℃, 레인지는 클수록 같은 유량에서 열량이 크다는 문장이 핵심."),
            ("https://m.blog.naver.com/hvackkw/222686660881", "냉각탑 흐름 그림 아래 ‘쿨링렌지’ 정의와 Q=G×Cp×Range 식. 사진·그림으로 37℃와 32℃가 어디에 붙는지 확인."),
            ("https://www.coolingtower.info/87", "표준설계조건 표. 입구 37℃, 출구 32℃, 습구 27℃, 13 L/min = 1 CRT. 레인지 5℃가 표준이라는 근거."),
        ],
    },
    {
        "id": "Q02",
        "title": "쿨링 어프로치 (Cooling approach)",
        "links": [
            ("https://gallery-k.tistory.com/157", "같은 글 ‘3-2 쿨링어프로치’. 출구수온−입구공기 습구온도, 32−27=5℃, 작을수록 좋다는 문장."),
            ("https://m.blog.naver.com/wonyl2017/222015421316", "습구온도 설명과 어프로치 3~5℃ 설계 문단. 어프로치를 줄이려면 탑이 커진다는 문장이 암기 함정을 막아 줌."),
            ("https://www.engineeringtoolbox.com/cooling-towers-d_159.html", "영문 정의 Range / Approach 그림. Approach는 출구수온이 습구온도에 얼마나 가까운지."),
        ],
    },
    {
        "id": "Q03",
        "title": "냉각탑 능력 계산 (13 L/min, 37/32/27℃)",
        "links": [
            ("https://www.coolingtower.info/87", "1 CRT 정의와 ‘3900 kcal/h로 나누면 조건이 다를 때 오산’이라는 경고. 이 문제 조건은 표준이라 변환계수 1."),
            ("https://m.blog.naver.com/hvackkw/222686660881", "Q=13×60×1×5=3900 kcal/h 계산 예시. kcal 버전."),
            ("https://eom119.tistory.com/43", "냉각탑 단원 하단 냉각톤·레인지·어프로치 정리. 1 냉각톤=3900 kcal/h."),
        ],
    },
    {
        "id": "Q04",
        "title": "냉각탑 설치 주의 3가지",
        "links": [
            ("https://gallery-k.tistory.com/157", "글 하단 설치위치. 통풍, 비산, 소음·진동."),
            ("https://en.wikipedia.org/wiki/Cooling_tower", "Drift(비산)와 Plume(백연) 절. 설치 시 물방울이 왜 문제인지 사진과 함께."),
        ],
    },
    {
        "id": "Q05",
        "title": "백연현상 (White plume)",
        "links": [
            ("https://en.wikipedia.org/wiki/Cooling_tower", "Plume 절. 배기의 수증기가 찬 공기에서 응축되어 흰 구름처럼 보이는 현상. 연소 연기가 아님."),
            ("https://eom119.tistory.com/43", "냉각탑이 증발잠열로 식힌다는 앞부분. 백연은 그 수증기가 밖으로 나와 다시 응축된 것."),
        ],
    },
    {
        "id": "Q06",
        "title": "캐리오버 (Carry over, drift)",
        "links": [
            ("https://en.wikipedia.org/wiki/Cooling_tower", "Drift eliminator 설명. 물방울이 송풍기에 실려 탑 밖으로 나가는 현상. 백연(응축된 증기)과 구분."),
            ("https://www.coolingtower.info/87", "비산과 용량 용어가 섞인 기술글. 캐리오버는 액적 손실이라는 점만 가져가면 됨."),
        ],
    },
    {
        "id": "Q07",
        "title": "왕복동 압축기 용량제어 3가지",
        "links": [
            ("https://en.wikipedia.org/wiki/Reciprocating_compressor", "Capacity control 절. 회전수, 클리어런스, 흡입밸브 언로더, 바이패스의 이름."),
            ("https://www.hvacrj.co.kr/news/articleView.html?idxno=10565", "냉동 자동제어 연재. 언로더·압력스위치가 용량과 어떻게 연결되는지."),
        ],
    },
    {
        "id": "Q08",
        "title": "스머징, 도달거리, 강하거리, 등마찰손실법",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "6번 해설. 스머징·도달거리 0.25 m/s·강하거리·등마찰손실법 문장이 기출 문장 그대로."),
            ("https://shopdrawing.tistory.com/176", "등마찰손실(등압)로 덕트 치수를 정한다는 배치 설명과 풍속 표."),
        ],
    },
    {
        "id": "Q09",
        "title": "이중효용 흡수식 vs 단효용",
        "links": [
            ("http://m.moa-ba.com/gnu/bbs/board.php?bo_table=qna&wr_id=39712", "연료 ‘65% 절감’이 아니라 ‘소비량이 단효용의 65%’라는 교정. ASHRAE의 35~45% 절감 문장."),
            ("https://earnings-surprise.tistory.com/65", "단효용 COP 약 0.7, 이중효용은 고온재생기 증기로 저온재생기를 가열. COP 약 50% 향상 문장."),
            ("https://www.hadaworks.com/blog-insight/absorption-chiller-guide", "증발기→흡수기→재생기→응축기 그림 설명. 이중효용은 재생기가 둘."),
            ("https://onhao09.tistory.com/169", "냉매/흡수제 짝 NH3-H2O, H2O-LiBr."),
        ],
    },
    {
        "id": "Q10",
        "title": "R-22와 NH3 특성 비교표",
        "links": [
            ("https://www.hvacrj.co.kr/news/articleView.html?idxno=10136", "윤활유 용해·분리, 수분, 독성 비교의 바탕이 되는 냉매 분류 글."),
            ("https://en.wikipedia.org/wiki/List_of_refrigerants", "R-22, R-717 행. ODP·GWP·안전분류. R-22는 HCFC, 암모니아는 B2L."),
            ("https://www.engineeringtoolbox.com/ammonia-d_1413.html", "암모니아 물성. 물에 잘 녹고 동을 부식시킨다는 실무 주의."),
        ],
    },
    {
        "id": "Q11",
        "title": "NH3 특징 5가지, CO2(R-744) 특징 5가지",
        "links": [
            ("https://www.engineeringtoolbox.com/ammonia-d_1413.html", "암모니아 독성·가연·구리 부식·물에 대한 용해도."),
            ("https://en.wikipedia.org/wiki/Carbon_dioxide", "임계온도 31.0℃, 임계압력 7.38 MPa 절. 포화압력이 높다는 문장의 근거."),
            ("https://en.wikipedia.org/wiki/List_of_refrigerants", "R-744 행. ODP 0, GWP 1. 기출은 ODP 0만 묻는다. GWP를 0으로 쓰면 안 됨."),
        ],
    },
    {
        "id": "Q12",
        "title": "브라인 구비조건 5가지",
        "links": [
            ("https://www.hvacrj.co.kr/news/articleView.html?idxno=10136", "냉매·냉동기유·브라인 연재 1편. 브라인이 간접 냉각의 2차 유체라는 위치."),
            ("https://www.engineeringtoolbox.com/brine-d_1414.html", "염수 농도-동결점 표. ‘사용 온도에서 액체일 것’이 동결점이 낮아야 한다는 뜻."),
        ],
    },
    {
        "id": "Q13",
        "title": "서징 (surging, 맥동)",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "10번. 정의 한 줄과, 산고 상승부·공기조·밸브 위치라는 발생 조건 3가지."),
            ("https://en.wikipedia.org/wiki/Surge_(fluid)", "펌프·압축기 서지가 유량과 압력이 주기적으로 뒤집히는 현상임을 보여주는 설명."),
        ],
    },
    {
        "id": "Q14",
        "title": "캐비테이션 (공동현상)",
        "links": [
            ("https://www.youtube.com/watch?v=U-uUYCFDTrc", "영상 전체. 좁은 목에서 압력이 증기압 아래로 떨어져 기포가 생기고, 압력이 회복되면 기포가 붕괴하는 장면."),
            ("https://en.wikipedia.org/wiki/Cavitation", "정의와 펌프 손상 사진. NPSH 개념."),
            ("https://www.moducbt.com/exam/solution/2181", "9번. 기출 정의와 원인 2가지(흡입양정, 임펠러 끝 고속)."),
        ],
    },
    {
        "id": "Q15",
        "title": "수격현상 (Water hammer)",
        "links": [
            ("https://www.youtube.com/watch?v=xoLmVFAFjn4", "밸브 급폐쇄 실험. 운동에너지가 압력파가 되는 장면과, 천천히 닫기·에어챔버 대응."),
            ("https://www.youtube.com/watch?v=6ydsAIHWVNM", "체크밸브가 역류와 함께 닫히며 수격이 나는 비교 영상."),
            ("https://en.wikipedia.org/wiki/Water_hammer", "Joukowsky 식 Δp=ρcΔv. 에어챔버는 압력파를 흡수하는 압축성 체적."),
        ],
    },
    {
        "id": "Q16",
        "title": "플래시가스, 액압축, 안전두, 펌프다운, 펌프아웃",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "3번·4번. 다섯 용어의 기출 정의와 플래시가스 원인 3·방지 3."),
            ("https://en.wikipedia.org/wiki/Vapor-compression_refrigeration", "사이클 그림. 플래시가스는 팽창 전 액관에서 미리 증발한 기체."),
            ("https://en.wikipedia.org/wiki/Thermal_expansion_valve", "팽창밸브 앞 액이 포화에 가까우면 왜 플래시가 나는지."),
        ],
    },
    {
        "id": "Q17",
        "title": "액압축 원인·방지·영향, 운전 주의, 겨울철 크랭크케이스",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "액압축 방지로 액가스 열교환기·액분리기를 적는 해설."),
            ("https://assets.danfoss.com/documents/50825/AX266348279899en-000101.pdf", "감온통을 액가스 열교환기 뒤에 달면 안 된다는 그림. 과열을 증발기 출구에서 재야 하는 이유."),
        ],
    },
    {
        "id": "Q18",
        "title": "부속기 설치 위치 (여과기, 액분리기, 유분리기, 수액기, 건조기, 균압관)",
        "links": [
            ("https://en.wikipedia.org/wiki/Vapor-compression_refrigeration", "기본 네 요소 그림 위에, 선박에서 보던 부속을 어디 사이에 끼우는지 대조."),
            ("https://eom119.tistory.com/43", "응축기 뒤에 수액기가 오는 흐름."),
        ],
    },
    {
        "id": "Q19",
        "title": "온도식 팽창밸브 감온통·외부균압관 위치",
        "links": [
            ("https://assets.danfoss.com/documents/50825/AX266348279899en-000101.pdf", "Bulb location 그림. 수평 흡입관, 4시·8시 방향, 바닥 금지. 외부균압관은 감온통 직후."),
            ("https://www.contractingbusiness.com/refrigeration/article/20866607/txv-installation-troubleshooting", "같은 내용을 사진과 문장으로. 균압관을 감온통보다 앞에 달면 안 되는 이유."),
        ],
    },
    {
        "id": "Q20",
        "title": "TEV, SV, HPS, OPS, DPS 명칭",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "8번 정답. OPS는 Oil Protection Switch(유압보호스위치), DPS는 Dual Pressure Switch. Valve가 아님."),
            ("https://www.hvacrj.co.kr/news/articleView.html?idxno=10565", "고압차단·유압보호 스위치가 압축기를 어떻게 세우는지."),
        ],
    },
    {
        "id": "Q21",
        "title": "벨로스형 증기 감압밸브 주위 배관",
        "links": [
            ("https://en.wikipedia.org/wiki/Pressure_regulator", "감압밸브는 하류 압력을 일정하게 유지. 고장으로 열리면 2차측이 과압이 되므로 안전밸브는 2차측."),
        ],
    },
    {
        "id": "Q22",
        "title": "EPR, SPR, CRP(CPR), WRV",
        "links": [
            ("https://www.moducbt.com/question/218124", "기출 문장. EPR은 증발기 출구·입구압으로 열림, SPR은 압축기 입구·출구압으로 닫힘, CRP는 응축기-수액기."),
            ("https://gallery-k.tistory.com/150", "EPR 개폐 그림. 압력이 낮으면 닫고 높으면 여는 이유(증발온도 유지)."),
            ("https://www.hvacrj.co.kr/news/articleView.html?idxno=10565", "증발압력조정밸브·흡입압력조정밸브 구조 설명."),
            ("https://engineer.inup.co.kr/post/read.jsp?id=168847", "CRP(냉매측)와 절수밸브 WRV(냉각수측)를 혼동하지 말라는 강사 정정."),
        ],
    },
    {
        "id": "Q23",
        "title": "극간풍 계산 3법·방지 3법, 환기횟수법·크랙법",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "극간풍 문항. 환기횟수, 틈새길이(크랙), 창면적. 방지는 이중문·회전문·에어커튼."),
            ("https://www.gigumi.com/343", "연돌효과. 겨울에 하부로 찬 공기가 들어오는 이유. 회전문이 왜 극간풍 대책인지."),
        ],
    },
    {
        "id": "Q24",
        "title": "증기 인젝터",
        "links": [
            ("https://en.wikipedia.org/wiki/Injector", "노즐-혼합-디퓨저 그림. 속도에너지가 압력에너지로 바뀌어 보일러 압력 위로 급수하는 구조."),
        ],
    },
    {
        "id": "Q25",
        "title": "냉매 표준 비점과 고비점·저비점의 장단점",
        "links": [
            ("https://en.wikipedia.org/wiki/List_of_refrigerants", "Normal boiling point 열. R-22 약 −41℃, NH3 약 −33℃, CO2 약 −78℃(또는 승화)."),
            ("https://www.kmecnews.co.kr/news/articleView.html?idxno=38837", "번호만 봐도 계열이 보인다는 설명. 비점 문제와 함께 읽으면 번호 문제가 붙음."),
        ],
    },
    {
        "id": "Q26",
        "title": "냉매 번호 체계와 R-40, R-717, R-744, R-12, R-764, R-718, R-500, R-114",
        "links": [
            ("https://www.kmecnews.co.kr/news/articleView.html?idxno=38837", "RXYZ 규칙, 400 비공비, 500 공비, 그림 1. 메탄계는 백의 자리가 0이라 두 자리로 씀."),
            ("https://onhao09.tistory.com/11", "400 비공비, 500 공비, 600 유기, 700 무기+분자량 요약."),
            ("https://en.wikipedia.org/wiki/List_of_refrigerants", "번호 대조표. R-717=17+700, R-744=44+700, R-718=18+700, R-764=64+700."),
        ],
    },
    {
        "id": "Q27",
        "title": "흡수식 냉매-흡수제, 흡수제 구비조건 O/X",
        "links": [
            ("https://ilvjesus.tistory.com/509117", "2015-2회 실기 문장. NH3-물, 물-LiBr. 증기압 높을 것 X, 변화 작을 것 O, 점도·부식 X."),
            ("https://www.comcbt.com/cbt/problem/7543/27/", "필기. ‘증발압력이 높을 것’이 가장 거리가 먼 것. 변화는 적을 것, 재생열은 많이 들지 않을 것."),
            ("https://onhao09.tistory.com/169", "두 짝이 쓰이는 온도 범위. 물-LiBr는 냉방, 암모니아-물은 더 낮은 온도."),
        ],
    },
    {
        "id": "Q28",
        "title": "송풍기 동력식, R-500·501·502, 임펠러 형상, 시로코 번호",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "31번. Q는 m³/s, Ps는 정압 kPa, ηs는 정압효율. R-500번은 공비."),
            ("https://www.engineeringtoolbox.com/fans-efficiency-power-consumption-d_197.html", "P=q×p/η. 단위를 SI로 맞추면 kW가 되는 이유."),
            ("https://en.wikipedia.org/wiki/Centrifugal_fan", "시로코(전향 다익), 후향 터보, 방사 플레이트, 익형, 축류 프로펠러 그림."),
        ],
    },
    {
        "id": "Q29",
        "title": "덕트 소음 방지, 흡음장치, 풍속·종횡비 문장 고치기",
        "links": [
            ("https://www.comcbt.com/cbt/problem/7530/10/", "저속/고속 경계는 15 m/s. 20 m/s가 아님."),
            ("https://shopdrawing.tistory.com/176", "용도별 풍속 표. 주택 주덕트 권장 3.5~4.5, 최대 약 4~6. 공공건물 주덕트 권장 5~6.5, 최대 약 10. 기출 교정값 6 m/s·8 m/s의 출처."),
            ("https://m.blog.naver.com/leesgab/223144435477", "기계설비 기준. 장단비 4:1 이내, 풍속 15 m/s 이하가 저압 덕트."),
        ],
    },
    {
        "id": "Q30",
        "title": "가스 머플러, 셔터, 전면적",
        "links": [
            ("https://www.unilab.eu/articles/technical-articles/thermodynamic-engineering-articles/oil-management-refrigerant-lines/", "토출 배관의 맥동·소음 문단. 머플러가 줄이려는 현상이 여기 나옴."),
        ],
    },
    {
        "id": "Q31",
        "title": "응축온도·증발온도·과열·과냉각이 사이클에 미치는 영향",
        "links": [
            ("https://eom119.tistory.com/23", "증발온도·응축온도 표. 이 두 열은 정리본과 일치."),
            ("https://gallery-k.tistory.com/66", "p-h 그림은 유용. 다만 ‘과열 시 냉동효과 감소’ 문장은 대표 조건 계산과 반대이므로 그 문장만 따르지 말 것. 학습본의 CoolProp 수치를 기준으로."),
        ],
    },
    {
        "id": "Q32",
        "title": "p-h 선도 빈칸 (등엔트로피, 단열압축, 포화액, 등엔탈피)",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "42번. 등엔트로피선-단열압축-포화액선-등엔탈피선 순서."),
            ("https://en.wikipedia.org/wiki/Vapor-compression_refrigeration", "Pressure-enthalpy diagram. 압축은 등엔트로피, 팽창은 등엔탈피."),
        ],
    },
    {
        "id": "Q33",
        "title": "유인유닛 vs 팬코일, 전공기 3방식",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "18~20번. 유인유닛은 1차 공기 노즐, 팬코일은 실내 송풍기. 전공기의 단일·이중·멀티존 장점."),
        ],
    },
    {
        "id": "Q34",
        "title": "겨울철 응축압력 저하",
        "links": [
            ("https://engineer.inup.co.kr/post/read.jsp?id=168847", "응축압력조절밸브와 절수밸브를 구분하는 문단. 겨울 대책의 밸브 이름."),
            ("https://www.moducbt.com/question/218124", "CRP는 응축기와 수액기 사이, 겨울철 응축압력 저하 방지."),
            ("https://eom119.tistory.com/23", "응축온도가 낮아지면 냉동효과는 커지지만, 압력차가 너무 줄면 팽창밸브 유량이 준다는 앞뒤 관계."),
        ],
    },
    {
        "id": "Q35",
        "title": "연돌효과, 종국유속, 콜드드래프트, ADPI, CLTD, 리프트피팅, 공동현상, 역환수",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "7번 보기 1~8과 정답. 종국유속은 (5) 배수수직관. 정리본의 (2)는 오타."),
            ("https://www.gigumi.com/343", "연돌효과 정의와 겨울·고층에서 커지는 이유. 회전문."),
        ],
    },
    {
        "id": "Q36",
        "title": "핫가스 제상",
        "links": [
            ("https://www.moducbt.com/exam/solution/2181", "29번. 팽창밸브 닫기 → 핫가스 밸브 열기 → 감압 → 압축기 회수 → 원위치."),
            ("https://engineer.inup.co.kr/post/read.jsp?id=168847", "증발기 2대일 때 밸브 순서에 대한 강사 보충. 장치마다 전자밸브 순서가 다를 수 있다는 주의."),
        ],
    },
    {
        "id": "Q37",
        "title": "이중 입상관 (Double suction riser)",
        "links": [
            ("https://www.achrnews.com/articles/83920-refrigeration-piping-the-use-of-double-risers", "그림이 있는 설명. 저부하는 트랩이 굵은 관을 막고 가는 관만 흐름, 전부하는 둘 다 흐름."),
            ("https://www.unilab.eu/articles/technical-articles/thermodynamic-engineering-articles/oil-management-refrigerant-lines/", "Figure 3 이중 라이저와 오일 트랩 문단."),
            ("https://anvilfield.com/field-guides/hvac/refrigerant-oil-return-long-line-sets/", "저부하에서 트랩이 굵은 관을 밀봉하는 순서를 단계로 적은 글."),
        ],
    },
    {
        "id": "Q38",
        "title": "동 도금 (Copper plating)",
        "links": [
            ("https://anvilfield.com/field-guides/hvac/refrigerant-oil-return-long-line-sets/", "수분+냉동기유(특히 POE)가 산을 만든다는 문단. 산이 동을 녹이는 앞단계."),
            ("https://www.hvacrj.co.kr/news/articleView.html?idxno=10136", "프레온과 수분이 공존하면 안 되는 이유. 건조기의 목적과 연결."),
        ],
    },
    {
        "id": "Q39",
        "title": "펌프 손실수두 3가지",
        "links": [
            ("https://en.wikipedia.org/wiki/Hydraulic_head", "전양정=위치수두+압력수두+속도수두+손실. 손실을 빼면 실양정만으로 펌프를 고르게 됨."),
        ],
    },
    {
        "id": "Q40",
        "title": "열원 설비, 에너지 절약",
        "links": [
            ("https://www.hadaworks.com/blog-insight/absorption-chiller-guide", "압축식 대신 흡수식을 열원으로 두는 경우. 열원 4종의 하나."),
        ],
    },
    {
        "id": "Q41",
        "title": "응축기 냉각수 배관 (출구를 높게, 밸브 위치, 체크밸브, 유니언)",
        "links": [
            ("https://www.moducbt.com/question/43082", "기출 해설 4문항. 기포 배출, 자동밸브는 입구, 시수에는 체크밸브, 유니언은 정비."),
        ],
    },
    {
        "id": "Q42",
        "title": "종횡비 6:1, 저온공조, 냉매 강제순환, 중간냉각기",
        "links": [
            ("https://m.blog.naver.com/leesgab/223144435477", "장단비 4:1이 설계 기준. 6:1 문제는 그보다 넓은 시공 상한을 묻는 것. 둘을 섞지 말 것."),
            ("https://www.moducbt.com/exam/solution/2181", "41번 중간냉각기 기능 3가지가 정리본과 동일."),
        ],
    },
]


def md():
    lines = [
        "# 공조냉동기계기사 서술형 자료 링크",
        "",
        "정리본(2004~2025.3)의 문답에 맞춰, 실제로 열어 본 페이지와 영상만 넣었다.",
        "각 링크 옆 문장은 그 페이지에서 어디를 보면 되는지다.",
        "같은 주소가 여러 문항에 다시 나오면, 그 글이 그 문항들의 공통 그림이기 때문이다.",
        "",
        "학습 본문은 `02-study-guide.html`이다. 링크는 그림과 출처 확인용이고, 암기 문장은 학습본에 모아 두었다.",
        "",
    ]
    for it in ITEMS:
        lines.append(f"## {it['id']}. {it['title']}")
        lines.append("")
        for url, note in it["links"]:
            lines.append(f"- [{url}]({url})")
            lines.append(f"  - {note}")
        lines.append("")
    return "\n".join(lines)


def html():
    parts = ["""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>공조냉동기계기사 서술형 자료 링크</title>
<style>
  body { font-family: "WenQuanYi Micro Hei", "Noto Sans CJK KR", sans-serif; margin: 32px auto; max-width: 980px; line-height: 1.55; color: #1c2430; }
  h1 { font-size: 28px; margin-bottom: 8px; }
  h2 { font-size: 18px; margin-top: 28px; border-top: 2px solid #1f4e79; padding-top: 12px; }
  .note { background: #f4f7fb; padding: 12px 14px; border-radius: 8px; }
  li { margin: 8px 0 14px; }
  a { color: #0b57d0; word-break: break-all; }
  .why { color: #243044; }
</style>
</head>
<body>
<h1>공조냉동기계기사 서술형 자료 링크</h1>
<p class="note">정리본의 문답마다, 열어 본 글·영상만 걸었다. 링크 아래 문장은 그 페이지에서 어느 문단·그림이 핵심인지다. 본문으로 이해하고 외울 내용은 같은 폴더의 학습본(<code>02-study-guide.html</code>, PDF 동일)에 있다.</p>
"""]
    for it in ITEMS:
        parts.append(f"<h2>{it['id']}. {it['title']}</h2>\n<ul>")
        for url, note in it["links"]:
            parts.append(f"<li><a href=\"{url}\">{url}</a><br><span class=\"why\">{note}</span></li>")
        parts.append("</ul>")
    parts.append("</body></html>")
    return "\n".join(parts)


if __name__ == "__main__":
    open("/workspace/hvac-study/01-links.md", "w", encoding="utf-8").write(md())
    open("/workspace/hvac-study/01-links.html", "w", encoding="utf-8").write(html())
    print("links", len(ITEMS))
