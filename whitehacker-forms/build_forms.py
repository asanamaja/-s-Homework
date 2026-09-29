#!/usr/bin/env python3
"""국립한국해양대학교 화이트해커 동아리 사업단 제출용 한글 서식 생성기.

산출물:
  화이트해커_행사계획서.hwp / .hwpx
  화이트해커_행사결과보고서.hwp / .hwpx
  화이트해커_서식_작성안내.hwp / .hwpx

한글 2010 이후 .hwp, 한글 2014 이후 .hwpx 로 연다.
"""

from __future__ import annotations

from pathlib import Path

from hwpx import HwpxDocument

FONT = "함초롬돋움"
NAVY = "#0C3C6E"
LIGHT = "#E7F2FA"
SUM_BG = "#F4F8FB"
GOLD = "#C4A35A"
INK = "#1F2933"
HINT_C = "#5C6770"

OUT = Path(__file__).resolve().parent


def mm(value: float) -> int:
    return int(round(value / 25.4 * 7200))


class Form:
    def __init__(self, header: str) -> None:
        self.doc = HwpxDocument.new()
        self.doc.page.setup(
            paper_size="A4",
            margin_left_mm=14,
            margin_right_mm=14,
            margin_top_mm=16,
            margin_bottom_mm=14,
            header_margin_mm=8,
            footer_margin_mm=8,
        )
        self.W = mm(182)
        er = self.doc.styles.ensure_run
        self.S = {
            "sec": er(font=FONT, size=11, bold=True, color="#FFFFFF"),
            "label": er(font=FONT, size=9.5, bold=True, color=NAVY),
            "body": er(font=FONT, size=9.5, bold=False, color=INK),
            "small": er(font=FONT, size=8.5, bold=False, color=INK),
            "hint": er(font=FONT, size=8.5, bold=False, color=HINT_C),
            "th": er(font=FONT, size=9, bold=True, color="#FFFFFF"),
            "sum": er(font=FONT, size=9.5, bold=True, color=NAVY),
            "white": er(font=FONT, size=10.5, bold=True, color="#FFFFFF"),
            "white_sub": er(font=FONT, size=10, bold=False, color="#D6E6F2"),
            "white_lg": er(font=FONT, size=18, bold=True, color="#FFFFFF"),
            "guide_h": er(font=FONT, size=13, bold=True, color=NAVY),
            "guide": er(font=FONT, size=10.5, bold=False, color=INK),
        }
        first = list(self.doc.paragraphs)
        if first:
            self.doc.styles.apply_paragraph_format(
                paragraphs=[first[0]],
                spacing_before_pt=0,
                spacing_after_pt=0,
                line_spacing_percent=50,
            )
        self.doc.page.set_header(text=header)
        self.doc.page.set_page_number(
            target="footer",
            align="CENTER",
            prefix="사업단 제출용   ·   ",
            suffix=" 쪽",
        )

    def spacer(self, after: float = 3) -> None:
        paragraph = self.doc.add_paragraph("", char_pr_id_ref=self.S["hint"])
        self.doc.styles.apply_paragraph_format(
            paragraphs=[paragraph],
            spacing_before_pt=0,
            spacing_after_pt=after,
            line_spacing_percent=70,
        )

    def paragraph(self, text: str, style: str = "guide", *, after: float = 3, before: float = 1, align: str = "LEFT") -> None:
        paragraph = self.doc.add_paragraph(text, char_pr_id_ref=self.S[style])
        self.doc.styles.apply_paragraph_format(
            paragraphs=[paragraph],
            alignment=align,
            spacing_before_pt=before,
            spacing_after_pt=after,
            line_spacing_percent=150,
        )

    def _valign(self, cell, align: str) -> None:
        for element in cell.element.iter():
            if element.tag.endswith("subList"):
                element.set("vertAlign", align)

    def put(
        self,
        table,
        row: int,
        col: int,
        text: str,
        style: str = "body",
        fill: str | None = None,
        align: str = "LEFT",
        valign: str = "CENTER",
    ) -> None:
        cell = table.cell(row, col)
        cell.set_text(text or "", split_paragraphs=True)
        style_id = str(self.S[style])
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.element.set("charPrIDRef", style_id)
        if fill:
            table.set_cell_shading(row, col, fill)
        if cell.paragraphs:
            self.doc.styles.apply_paragraph_format(
                paragraphs=list(cell.paragraphs),
                alignment=align,
                line_spacing_percent=130,
            )
        self._valign(cell, valign)

    def grid(self, rows: int, cols: int, row_mm: float, weights: list[float] | None = None):
        table = self.doc.add_table(rows, cols, width=self.W, height=mm(row_mm * rows))
        if weights:
            table.set_column_widths(weights)
        return table

    def fill(self, table, matrix, merges: list[tuple[int, int, int, int]] | None = None) -> None:
        if merges:
            for start_row, start_col, end_row, end_col in merges:
                table.merge_cells(start_row, start_col, end_row, end_col)
        for row_index, row in enumerate(matrix):
            for col_index, item in enumerate(row):
                if not item:
                    continue
                self.put(
                    table,
                    row_index,
                    col_index,
                    item.get("text", ""),
                    item.get("style", "body"),
                    item.get("fill"),
                    item.get("align", "LEFT"),
                    item.get("valign", "CENTER"),
                )

    def banner(self, eyebrow: str, title: str, subtitle: str) -> None:
        table = self.doc.add_table(1, 1, width=self.W, height=mm(30))
        cell = table.cell(0, 0)
        cell.set_text(eyebrow)
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.element.set("charPrIDRef", str(self.S["white_sub"]))
        cell.add_paragraph(title, char_pr_id_ref=self.S["white_lg"])
        cell.add_paragraph(subtitle, char_pr_id_ref=self.S["white"])
        table.set_cell_shading(0, 0, NAVY)
        self.doc.styles.apply_paragraph_format(
            paragraphs=list(cell.paragraphs),
            alignment="CENTER",
            line_spacing_percent=150,
        )
        self._valign(cell, "CENTER")
        self.spacer(1)
        gold = self.doc.add_table(1, 1, width=self.W, height=mm(1.8))
        self.put(gold, 0, 0, " ", "body", GOLD, "CENTER", "CENTER")
        self.spacer(3)

    def section(self, title: str) -> None:
        self.spacer(1)
        table = self.doc.add_table(1, 1, width=self.W, height=mm(7.4))
        self.put(table, 0, 0, "  " + title, "sec", NAVY, "LEFT", "CENTER")
        self.spacer(2)

    def note(self, text: str) -> None:
        self.paragraph(text, "hint", after=2, before=0)

    def box(self, text: str, height_mm: float = 28, fill: str | None = None) -> None:
        table = self.grid(1, 1, height_mm)
        self.put(table, 0, 0, text, "body", fill, "LEFT", "TOP")
        self.spacer(2)

    def kv(self, rows: list[list[tuple[str, str]]], row_mm: float = 8.4) -> None:
        matrix = []
        merges = []
        for index, row in enumerate(rows):
            if len(row) == 1:
                label, value = row[0]
                matrix.append([L(label), V(value), None, None])
                merges.append((index, 1, index, 3))
            else:
                (label_a, value_a), (label_b, value_b) = row
                matrix.append([L(label_a), V(value_a), L(label_b), V(value_b)])
        table = self.grid(len(rows), 4, row_mm, [18, 32, 18, 32])
        self.fill(table, matrix, merges)
        self.spacer(2)

    def table(
        self,
        headers: list[str],
        body: list[list[str]],
        weights: list[float],
        row_mm: float = 8.2,
        *,
        header_mm: float = 8.2,
        sum_last: bool = False,
        body_align: list[str] | None = None,
    ) -> None:
        rows = [header_cells(headers)]
        for offset, values in enumerate(body):
            last = sum_last and offset == len(body) - 1
            style = "sum" if last else "small"
            fill = SUM_BG if last else None
            aligned = []
            for col, value in enumerate(values):
                align = "CENTER" if last and col == 0 else (body_align[col] if body_align else "CENTER")
                if body_align is None and col == 0 and not last:
                    align = "CENTER"
                aligned.append({"text": value, "style": style, "fill": fill, "align": align, "valign": "CENTER"})
            rows.append(aligned)
        table = self.grid(len(rows), len(headers), row_mm, weights)
        # Give the header the same row height as the body. header_mm is accepted
        # so callers can document a taller header without a second code path.
        _ = header_mm
        self.fill(table, rows)
        self.spacer(2)

    def save(self, stem: str) -> None:
        self.doc.validate()
        hwpx_path = OUT / f"{stem}.hwpx"
        hwp_path = OUT / f"{stem}.hwp"
        self.doc.save_to_path(hwpx_path)
        self.doc.save_to_path(hwp_path)
        for path in (hwpx_path, hwp_path):
            opened = HwpxDocument.open(path)
            text = opened.text.plain()
            if stem.startswith("화이트해커_행사계획서") and "행사 계획서" not in text:
                raise RuntimeError(f"계획서 본문 확인 실패: {path.name}")
            if stem.startswith("화이트해커_행사결과") and "행사 결과보고서" not in text:
                raise RuntimeError(f"보고서 본문 확인 실패: {path.name}")
            if "작성안내" in stem and "참고한 공개 자료" not in text:
                raise RuntimeError(f"안내문 본문 확인 실패: {path.name}")
        print(f"saved {hwpx_path.name} ({hwpx_path.stat().st_size} bytes), {hwp_path.name} ({hwp_path.stat().st_size} bytes)")


def L(text: str) -> dict:
    return {"text": text, "style": "label", "fill": LIGHT, "align": "CENTER", "valign": "CENTER"}


def V(text: str = "") -> dict:
    return {"text": text, "style": "body", "fill": None, "align": "LEFT", "valign": "CENTER"}


def header_cells(labels: list[str]) -> list[dict]:
    return [{"text": label, "style": "th", "fill": NAVY, "align": "CENTER", "valign": "CENTER"} for label in labels]


def blank_rows(columns: int, count: int, first_numbers: bool = False) -> list[list[str]]:
    rows = []
    for index in range(count):
        row = [""] * columns
        if first_numbers:
            row[0] = str(index + 1)
        rows.append(row)
    return rows


def build_plan() -> None:
    form = Form("국립한국해양대학교  화이트해커 동아리   |   행사 계획서")
    form.banner(
        "국립한국해양대학교",
        "행사 계획서",
        "화이트해커 동아리  ·  사업단 제출용",
    )
    form.kv(
        [
            [("문서번호", "WH-PLAN-20__-__"), ("작성일", "20__년 __월 __일")],
            [("보존", "행사 종료 후 3년 권장"), ("공개", "□ 일반    □ 대외비")],
        ],
        row_mm=7.6,
    )
    form.note("결재란은 사업단이 요구하는 순서에 맞게 칸을 고쳐 씁니다. 서명란이 좁으면 한글에서 행 높이를 늘립니다.")
    form.table(
        ["구분", "실무 담당", "동아리장", "총무", "지도교수", "사업단"],
        [
            ["성명", "", "", "", "", ""],
            ["서명", "", "", "", "", ""],
            ["일자", "", "", "", "", ""],
        ],
        [12, 17, 17, 16, 19, 19],
        row_mm=11,
    )

    form.section("1. 동아리·제출 정보")
    form.kv(
        [
            [("동아리명", "화이트해커 (White Hacker)"), ("소속", "국립한국해양대학교")],
            [("학부·학과", ""), ("동아리 구분", "□ 전공    □ 일반·학술    □ 연합    □ 기타(    )")],
            [("활동 분야", "정보보호, 화이트해커 교육, 허가된 환경에서의 보안 실습")],
            [("지도교수", "소속                    성명                    연락처")],
            [("대표자", "학부                    학번                    성명")],
            [("대표 연락처", ""), ("이메일", "")],
            [("실무 담당", "성명                    연락처")],
            [("제출처", "국립한국해양대학교 ____________________ 사업단")],
        ],
        row_mm=10,
    )

    form.section("2. 행사 개요")
    form.kv(
        [
            [("행사명", "")],
            [("행사 구분", "□ 교내          □ 교외"), ("예산 지원", "□ 요청          □ 자체 개최")],
            [(
                "행사 유형",
                "□ 보안 세미나·특강    □ 교내 CTF    □ 워크숍·실습    □ 보안 인식 캠페인\n"
                "□ 연합·교류    □ 신입 모집    □ 외부 대회 참가·견학    □ 기타(          )",
            )],
            [("행사 일시", "20__년 __월 __일 ( __ ) __:__  ~  20__년 __월 __일 ( __ ) __:__")],
            [("장소", "교내: ____________________    호실·시설명 ____________________\n교외: ____________________")],
            [("참가 대상", "□ 동아리 부원    □ 본교 재학생    □ 타 대학    □ 외부 전문가    □ 기타(    )")],
            [("예상 인원", "부원 ____명    재학생 ____명    외부 ____명    합계 ____명")],
            [("총예산", "____________원"), ("지원 요청액", "____________원")],
        ],
        row_mm=12,
    )

    form.section("3. 목적·필요성·기대 효과")
    form.note("각 칸은 5~8줄. 기대 효과에는 인원, 만족도, 수료 인원처럼 나중에 결과보고서로 대조할 숫자를 적습니다.")
    form.paragraph("가. 추진 목적", "label", after=1, before=1)
    form.box("\n\n\n", 26)
    form.paragraph("나. 필요성", "label", after=1, before=1)
    form.box("\n\n\n", 26)
    form.paragraph("다. 기대 효과", "label", after=1, before=1)
    form.box("정량: \n정성: \n\n", 26)

    form.section("4. 준비 일정")
    form.note("행사 2주 전 제출이 필요한 사업단이 많습니다. 실제 마감은 해당 공고를 따릅니다.")
    prep = blank_rows(5, 6, first_numbers=True)
    form.table(
        ["연번", "일자", "추진 내용", "담당", "완료 기준"],
        prep,
        [8, 16, 40, 16, 20],
        row_mm=8.6,
        body_align=["CENTER", "CENTER", "LEFT", "CENTER", "LEFT"],
    )

    form.section("5. 당일 프로그램")
    program = blank_rows(6, 8)
    form.table(
        ["시간", "프로그램", "주요 내용", "진행·강사", "장소", "준비물"],
        program,
        [14, 18, 28, 16, 14, 14],
        row_mm=8.4,
        body_align=["CENTER", "LEFT", "LEFT", "CENTER", "CENTER", "LEFT"],
    )

    form.section("6. 역할 분담")
    roles = [
        ["총괄", "", "", "", ""],
        ["진행", "", "", "", ""],
        ["기술·실습", "", "", "", ""],
        ["안전", "", "", "", ""],
        ["홍보", "", "", "", ""],
        ["회계·증빙", "", "", "", ""],
        ["기록·사진", "", "", "", ""],
    ]
    form.table(
        ["역할", "성명", "학번", "담당 업무", "연락처"],
        roles,
        [16, 16, 16, 32, 20],
        row_mm=7.8,
        body_align=["CENTER", "CENTER", "CENTER", "LEFT", "CENTER"],
    )

    form.section("7. 홍보·모집")
    promo = [
        ["교내 포스터", "", "", ""],
        ["학부·학과 공지", "", "", ""],
        ["커뮤니티", "", "", ""],
        ["SNS", "", "", ""],
        ["문자·메일", "", "", ""],
    ]
    form.table(
        ["채널", "홍보 내용", "게시 일정", "담당"],
        promo,
        [18, 42, 22, 18],
        row_mm=8,
        body_align=["CENTER", "LEFT", "CENTER", "CENTER"],
    )

    form.section("8. 안전·준법·개인정보")
    form.note("보안 행사임을 사업단이 판단할 수 있게, 해당 항목을 체크하고 예외가 있으면 비고에 적습니다.")
    checks = [
        ["□", "실습은 주최 측이 제공하고 사전에 허가한 환경에서만 진행한다."],
        ["□", "교내 운영 시스템, 타인의 계정, 외부 기관 시스템을 대상으로 하는 침해 행위는 포함하지 않는다."],
        ["□", "개인정보를 수집하면 목적, 항목, 보유 기간을 알리고 동의를 받는다. 수집이 없으면 해당 없음으로 적는다."],
        ["□", "사진·영상 촬영과 게시는 동의한 범위에서만 한다."],
        ["□", "야간, 교외, 차량 이동이 있으면 인솔자와 비상 연락 체계를 둔다."],
        ["□", "예산 항목이 사업단 집행 기준에 맞는지는 지출 전에 확인한다."],
        ["□", "외부 강사, 후원, 공동 주최가 있으면 소속과 역할을 미리 알린다."],
    ]
    form.table(
        ["확인", "준수 사항"],
        checks,
        [10, 90],
        row_mm=11,
        body_align=["CENTER", "LEFT"],
    )
    form.paragraph("예외·추가 안전 계획", "label", after=1, before=0)
    form.box("\n\n", 18)

    form.section("9. 소요 예산")
    form.note(
        "재원에는 사업단, 자부담, 후원, 기타 중 하나를 적습니다. "
        "비목 예: 인쇄·홍보비, 소모품비, 다과·식비, 외부 강사 사례비, 장소 임차료, 상장·기념품, 교통비. "
        "주류, 자산성 물품, 개인 물품은 지원되지 않는 경우가 많으니 공고를 확인합니다."
    )
    budget = blank_rows(7, 8, first_numbers=True)
    budget.append(["합계", "", "", "", "", "", ""])
    form.table(
        ["연번", "비목", "세부 내역", "산출 근거", "금액(원)", "재원", "비고"],
        budget,
        [7, 13, 24, 20, 12, 12, 12],
        row_mm=7.6,
        sum_last=True,
        body_align=["CENTER", "CENTER", "LEFT", "LEFT", "RIGHT", "CENTER", "LEFT"],
    )
    form.kv(
        [[("사업단 요청액", "____________원"), ("자부담·후원", "____________원")]],
        row_mm=8,
    )

    form.section("10. 시설·장비·실습 환경")
    facilities = [
        ["장소", "", "", "", "□ 허가 필요    □ 불필요"],
        ["기자재", "", "", "", ""],
        ["네트워크·실습 환경", "", "", "", "허가된 환경만 기재"],
        ["게시·현수막", "", "", "", ""],
        ["차량·이동", "", "", "", ""],
    ]
    form.table(
        ["구분", "사용 내용", "수량", "사용 일시", "허가·협조"],
        facilities,
        [18, 28, 10, 20, 24],
        row_mm=8.4,
        body_align=["CENTER", "LEFT", "CENTER", "CENTER", "LEFT"],
    )

    form.section("11. 첨부 서류")
    attachments = [
        ["□", "세부 시간표. 위 4~5항으로 갈음할 수 있으면 갈음이라고 적는다."],
        ["□", "예산 산출 내역"],
        ["□", "포스터 또는 홍보물 시안"],
        ["□", "참가 신청서"],
        ["□", "시설 사용 신청"],
        ["□", "외부 강사 프로필. 외부 강사가 있을 때"],
        ["□", "개인정보 수집·이용 동의서. 수집할 때"],
        ["□", "안전 계획. 교외, 야간, 이동이 있을 때"],
        ["□", "기타 (                                        )"],
    ]
    form.table(
        ["첨부", "서류"],
        attachments,
        [10, 90],
        row_mm=7.4,
        body_align=["CENTER", "LEFT"],
    )

    form.section("12. 확인 및 제출")
    form.box(
        "본 동아리는 국립한국해양대학교와 지원 사업단의 행사·예산 기준을 확인했습니다.\n"
        "본 행사는 교육과 방어 역량을 위한 활동이며, 허가되지 않은 시스템이나 타인의 계정을 대상으로 하는 침해 행위가 포함되지 않습니다.\n"
        "개인정보와 초상은 동의한 범위에서만 다루고, 위 기재 내용이 사실과 다름없음을 확인합니다.",
        28,
        "#F8FBFE",
    )
    form.paragraph("20__년 ____월 ____일", "body", align="CENTER", before=2, after=2)
    form.table(
        ["구분", "소속·학부", "학번 또는 직위", "성명", "서명", "일자"],
        [
            ["대표자", "", "", "", "", ""],
            ["총무", "", "", "", "", ""],
            ["지도교수", "", "", "", "", ""],
        ],
        [14, 22, 20, 16, 14, 14],
        row_mm=12,
    )
    form.paragraph("국립한국해양대학교 ____________________ 사업단장  귀하", "guide_h", align="CENTER", before=4, after=2)
    form.save("화이트해커_행사계획서")


def build_report() -> None:
    form = Form("국립한국해양대학교  화이트해커 동아리   |   행사 결과보고서")
    form.banner(
        "국립한국해양대학교",
        "행사 결과보고서",
        "화이트해커 동아리  ·  사업단 제출용",
    )
    form.kv(
        [
            [("문서번호", "WH-RPT-20__-__"), ("작성일", "20__년 __월 __일")],
            [("관련 계획서", "WH-PLAN-20__-__"), ("제출 기한", "행사 후 ____일 이내")],
        ],
        row_mm=7.6,
    )
    form.note("많은 대학이 행사 후 7일에서 14일 사이에 결과와 영수증을 받습니다. 마감은 사업단 공고를 따릅니다.")
    form.table(
        ["구분", "실무 담당", "동아리장", "총무", "지도교수", "사업단"],
        [
            ["성명", "", "", "", "", ""],
            ["서명", "", "", "", "", ""],
            ["일자", "", "", "", "", ""],
        ],
        [12, 17, 17, 16, 19, 19],
        row_mm=11,
    )

    form.section("1. 기본 정보")
    form.kv(
        [
            [("동아리명", "화이트해커 (White Hacker)"), ("소속", "국립한국해양대학교")],
            [("학부·학과", ""), ("지도교수", "")],
            [("대표자", "학번                    성명"), ("연락처", "")],
            [("제출처", "국립한국해양대학교 ____________________ 사업단")],
            [("행사명", "")],
            [("행사 유형", "□ 세미나·특강  □ 교내 CTF  □ 워크숍·실습  □ 캠페인  □ 연합  □ 대회 참가  □ 기타")],
        ],
        row_mm=10,
    )

    form.section("2. 계획 대비 실적")
    form.table(
        ["항목", "계획", "실적", "차이·사유"],
        [
            ["일시", "", "", ""],
            ["장소", "", "", ""],
            ["참가 대상", "", "", ""],
            ["참가 인원", "", "", ""],
            ["예산 총액", "", "", ""],
            ["프로그램", "", "", ""],
        ],
        [16, 28, 28, 28],
        row_mm=8.2,
        body_align=["CENTER", "LEFT", "LEFT", "LEFT"],
    )
    form.kv(
        [[("계획 변경", "□ 없음     □ 있음 (일시 · 장소 · 예산 · 내용)")]],
        row_mm=8,
    )
    form.paragraph("변경 내용과 사전 승인 여부", "label", after=1, before=0)
    form.box("\n\n", 18)

    form.section("3. 참가 실적")
    form.table(
        ["구분", "목표", "신청", "실제 참석", "참석률", "비고"],
        [
            ["동아리 부원", "", "", "", "", ""],
            ["본교 재학생(부원 제외)", "", "", "", "", ""],
            ["타 대학·외부", "", "", "", "", ""],
            ["스태프·진행", "", "", "", "", ""],
            ["합계", "", "", "", "", ""],
        ],
        [24, 12, 12, 16, 14, 22],
        row_mm=8,
        sum_last=True,
        body_align=["LEFT", "CENTER", "CENTER", "CENTER", "CENTER", "LEFT"],
    )

    form.section("4. 프로그램 실시 결과")
    done = blank_rows(6, 8)
    form.table(
        ["시간", "프로그램", "계획 내용", "실시 결과", "참석", "비고"],
        done,
        [13, 16, 24, 23, 10, 14],
        row_mm=8.2,
        body_align=["CENTER", "LEFT", "LEFT", "LEFT", "CENTER", "LEFT"],
    )

    form.section("5. 주요 내용")
    form.note("교육으로 다룬 주제, 진행 방식, 참가자가 가져간 결과를 적습니다. 공격 절차나 악용 가능한 세부 내용은 보고서 본문에 넣지 않습니다.")
    form.paragraph("가. 행사 진행 요약", "label", after=1, before=1)
    form.box("\n\n\n", 28)
    form.paragraph("나. 프로그램별 결과", "label", after=1, before=1)
    form.box("\n\n\n", 28)
    form.paragraph("다. 산출물", "label", after=1, before=1)
    form.box("자료집, 발표 자료, 수료 현황, 문제 풀이 통계, 홍보 게시물 등 이름과 수량만 적습니다.\n\n", 22)

    form.section("6. 성과")
    form.table(
        ["지표", "목표", "실적", "비고"],
        [
            ["참석률", "", "", ""],
            ["만족도(5점 만점)", "", "", ""],
            ["설문 응답률", "", "", ""],
            ["수료·완주 인원", "", "", ""],
            ["산출물 수량", "", "", ""],
        ],
        [24, 22, 22, 32],
        row_mm=8,
        body_align=["LEFT", "CENTER", "CENTER", "LEFT"],
    )
    form.note("만족도는 행사 직후 짧은 설문으로 받습니다. 응답 수를 반드시 같이 적습니다.")
    form.table(
        ["항목", "5", "4", "3", "2", "1", "응답 수", "평균"],
        [
            ["내용의 적절성", "", "", "", "", "", "", ""],
            ["난이도의 적절성", "", "", "", "", "", "", ""],
            ["운영·진행", "", "", "", "", "", "", ""],
            ["실습 환경(해당 시)", "", "", "", "", "", "", ""],
            ["재참여 의향", "", "", "", "", "", "", ""],
            ["전체", "", "", "", "", "", "", ""],
        ],
        [24, 8, 8, 8, 8, 8, 14, 12],
        row_mm=7.4,
        sum_last=True,
    )
    form.paragraph("참가자 의견 가운데 다음 행사에 반영할 내용", "label", after=1, before=1)
    form.box("\n\n", 20)

    form.section("7. 예산 집행")
    form.note("금액은 영수증, 카드 전표, 이체 확인증과 원이 맞아야 합니다. 증빙번호는 아래 증빙 목록의 번호와 같게 적습니다.")
    money = blank_rows(7, 8, first_numbers=True)
    money.append(["합계", "", "", "", "", "", ""])
    form.table(
        ["연번", "비목", "예산액", "집행액", "잔액", "차이 사유", "증빙번호"],
        money,
        [7, 14, 13, 13, 12, 25, 16],
        row_mm=7.6,
        sum_last=True,
        body_align=["CENTER", "CENTER", "RIGHT", "RIGHT", "RIGHT", "LEFT", "CENTER"],
    )
    form.kv(
        [
            [("집행률", "________ %"), ("반환·불용액", "____________원")],
            [("사업단 지원 집행", "____________원"), ("자부담·후원 집행", "____________원")],
        ],
        row_mm=8,
    )
    form.paragraph("증빙 목록", "label", after=1, before=1)
    evidence = blank_rows(7, 8, first_numbers=True)
    form.table(
        ["번호", "지출일", "사용처", "적요", "금액(원)", "증빙 종류", "비고"],
        evidence,
        [8, 14, 18, 22, 14, 14, 10],
        row_mm=7.4,
        body_align=["CENTER", "CENTER", "LEFT", "LEFT", "RIGHT", "CENTER", "LEFT"],
    )
    form.note("증빙 종류 예: 카드전표, 현금영수증, 세금계산서, 계좌이체확인, 견적·거래명세서, 현장 사진. 간이영수증만으로는 부족한 사업단이 많습니다.")

    form.section("8. 자체 평가와 다음 계획")
    form.paragraph("가. 잘된 점", "label", after=1, before=0)
    form.box("\n\n", 18)
    form.paragraph("나. 아쉬운 점", "label", after=1, before=0)
    form.box("\n\n", 18)
    form.paragraph("다. 다음에 고칠 점", "label", after=1, before=0)
    form.box("\n\n", 18)
    form.paragraph("라. 이후 동아리·사업 계획", "label", after=1, before=0)
    form.box("\n\n", 18)

    form.section("9. 활동 사진")
    form.note("활동 내용이 보이는 사진으로 붙입니다. 참가자 단체 사진 1장을 포함하고, 게시에 동의하지 않은 얼굴은 가립니다. 칸이 부족하면 표를 복사합니다.")
    photo_table = form.grid(3, 2, 32, [50, 50])
    photo_rows = []
    for left in (1, 3, 5):
        photo_rows.append([
            {"text": f"사진 {left}\n\n\n설명:", "style": "body", "align": "LEFT", "valign": "TOP"},
            {"text": f"사진 {left + 1}\n\n\n설명:", "style": "body", "align": "LEFT", "valign": "TOP"},
        ])
    form.fill(photo_table, photo_rows)
    form.spacer(2)

    form.section("10. 참여자 명단")
    form.note("사업단이 서명부를 따로 요구하면 그 양식을 첨부하고, 이 표에는 인원 집계가 맞게 적습니다. 행이 부족하면 표를 복사합니다.")
    people = blank_rows(7, 15, first_numbers=True)
    form.table(
        ["연번", "학부·학과", "학번", "학년", "성명", "구분", "출석"],
        people,
        [8, 24, 16, 8, 14, 16, 14],
        row_mm=7.2,
    )
    form.note("구분 예: 부원, 재학생, 외부, 스태프. 출석란은 ○ 또는 서명.")

    form.section("11. 지도교수 의견")
    form.box("\n\n\n", 28)
    form.kv(
        [[("지도교수", "소속                    성명"), ("서명·일자", "")]],
        row_mm=10,
    )

    form.section("12. 첨부 및 확인")
    files = [
        ["□", "활동 사진. 단체 사진 포함"],
        ["□", "포스터, 자료집, 발표 자료"],
        ["□", "출석부 또는 참여자 명단"],
        ["□", "만족도 설문 결과"],
        ["□", "영수증·전표 원본 또는 사업단이 정한 사본"],
        ["□", "통장사본. 지원금을 입금받을 때"],
        ["□", "계획 변경 승인 자료. 변경이 있었을 때"],
        ["□", "기타 (                                        )"],
    ]
    form.table(["첨부", "서류"], files, [10, 90], row_mm=7.2, body_align=["CENTER", "LEFT"])
    form.box(
        "위 내용은 행사 계획서와 실제 집행을 대조하여 작성했으며, 금액과 증빙이 서로 맞습니다.\n"
        "허가되지 않은 시스템에 대한 침해 행위는 없었습니다. 사실과 다르게 적은 내용이 있으면 정정하여 다시 제출하겠습니다.",
        24,
        "#F8FBFE",
    )
    form.paragraph("20__년 ____월 ____일", "body", align="CENTER", before=2, after=2)
    form.table(
        ["구분", "소속·학부", "학번 또는 직위", "성명", "서명", "일자"],
        [
            ["대표자", "", "", "", "", ""],
            ["총무", "", "", "", "", ""],
            ["지도교수", "", "", "", "", ""],
        ],
        [14, 22, 20, 16, 14, 14],
        row_mm=12,
    )
    form.paragraph("국립한국해양대학교 ____________________ 사업단장  귀하", "guide_h", align="CENTER", before=4, after=2)
    form.save("화이트해커_행사결과보고서")


def build_guide() -> None:
    form = Form("국립한국해양대학교  화이트해커 동아리   |   서식 작성 안내")
    form.banner(
        "국립한국해양대학교",
        "서식 작성 안내",
        "행사 계획서 · 행사 결과보고서",
    )
    form.paragraph(
        "동아리에 큰 행사가 있을 때 사업단에 내기 위한 계획서와 결과보고서입니다. "
        "동아리명과 소속은 화이트해커, 국립한국해양대학교로 넣어 두었습니다. "
        "제출처의 빈칸에는 실제 사업단 이름을 적습니다.",
        after=6,
    )

    form.section("1. 파일")
    form.paragraph("화이트해커_행사계획서.hwp, .hwpx  —  행사 전에 제출", after=2)
    form.paragraph("화이트해커_행사결과보고서.hwp, .hwpx  —  행사 후에 제출", after=2)
    form.paragraph(".hwp 는 한글의 기본 형식입니다. .hwpx 는 한글 2014 이상에서 여는 같은 문서입니다. 사업단이 한쪽만 받으면 그 형식으로 보냅니다.", after=6)

    form.section("2. 참고한 공개 자료")
    form.paragraph(
        "유료 서식 사이트의 파일을 그대로 담지 않았습니다. 대학이 공개한 동아리 행사 서류에 반복되는 항목을 모아, 화이트해커 행사에 맞게 다시 구성했습니다.",
        after=4,
    )
    form.paragraph(
        "가. 포항공과대학교 동아리연합회 행사계획서의 공개된 구성. 교내·교외 구분, 행사 종류, 기간, 시설과 차량, 대표자와 지도교수 확인, 학생처 결재.",
        after=3,
    )
    form.paragraph(
        "나. 가톨릭관동대학교 2024학년도 2학기 동아리 활동 지원 계획. 지원금 사용 계획, 활동 주요 내용, 향후 계획, 활동 사진, 참여자 명단. "
        "https://www.ck.ac.kr/wp-content/uploads/2024/09/20240912_022458.pdf",
        after=3,
    )
    form.paragraph(
        "다. 아주대학교 경영대학원 학생행사 안내와 경영대학 소학회 활동비 안내. 계획서는 행사 2주 전, 결과보고서는 행사 후 1주 안. "
        "영수증, 단체 사진, 명단, 통장사본. 주류·개인 물품·현금성 지출은 지원 불가 사례로 안내.",
        after=3,
    )
    form.paragraph(
        "라. 행사 결과보고서에서 공통으로 요구되는 참여 실적, 예산 대비 집행, 정량 성과. 계획서의 예산표에 집행액과 잔액 칸을 더하는 방식.",
        after=6,
    )

    form.section("3. 이 동아리에 맞게 넣은 것")
    form.paragraph("표지와 머리말에 국립한국해양대학교, 화이트해커를 고정했습니다.", after=2)
    form.paragraph("행사 유형에 보안 세미나, 교내 CTF, 워크숍, 보안 인식 캠페인, 연합 행사, 외부 대회 참가를 넣었습니다.", after=2)
    form.paragraph("실습 환경, 허가 범위, 개인정보, 촬영 동의를 계획서 확인란으로 빼 두었습니다. 사업단이 보안 행사의 범위를 읽을 수 있게 하기 위한 칸입니다.", after=2)
    form.paragraph("결과보고서의 만족도는 내용, 난이도, 운영, 실습 환경, 재참여 의향으로 나눴습니다.", after=2)
    form.paragraph("교내 학생 행사 창구로는 학생처 학생복지과 학생지원팀(051-410-4022)이 있습니다. 시설 협조가 필요할 때 참고하고, 서류를 낼 곳은 사업단 공고를 따릅니다.", after=6)

    form.section("4. 작성 순서")
    form.paragraph("1. 제출처에 사업단 정식 명칭을 적고, 그 사업단에 지정 서식이 있는지 먼저 확인합니다. 지정 서식이 있으면 그 서식이 우선입니다.", after=2)
    form.paragraph("2. 행사명, 일시, 장소, 인원, 예산을 개요에 적고, 같은 숫자를 일정표와 예산표에 맞춥니다.", after=2)
    form.paragraph("3. 기대 효과의 숫자를 결과보고서 성과 칸과 같은 항목으로 적어 둡니다. 나중에 계획 대비 실적을 쓰기 쉽습니다.", after=2)
    form.paragraph("4. 안전 확인란은 해당 없는 문장도 지우지 말고, 해당 없음이라고 적습니다.", after=2)
    form.paragraph("5. 행사 뒤에는 영수증을 지출일 순서로 번호를 매기고, 예산 집행표의 증빙번호와 맞춥니다.", after=2)
    form.paragraph("6. 사진, 출석, 설문, 영수증을 빠뜨리지 않고 대표자와 지도교수 서명을 받습니다.", after=6)

    form.section("5. 자주 빠지는 것")
    form.paragraph("계획 인원과 결과 인원의 기준이 다른 경우. 신청 인원과 실제 참석을 나눠 적습니다.", after=2)
    form.paragraph("예산 합계와 항목 합계가 다른 경우. 합계 칸을 적기 전에 세로로 더해 봅니다.", after=2)
    form.paragraph("영수증 금액과 보고서 금액이 다른 경우. 부가세 포함 금액으로 통일합니다.", after=2)
    form.paragraph("지원받지 않는 항목을 올린 경우. 주류, 자산으로 남는 장비, 개인 물품은 공고에서 먼저 확인합니다.", after=2)
    form.paragraph("얼굴이 나온 사진을 동의 없이 붙이는 경우. 공개용과 제출용을 구분합니다.", after=6)

    form.section("6. 작성 예시")
    form.note("숫자는 예시입니다. 서식 파일에는 들어 있지 않으니, 실제 행사 값으로 바꿉니다. 문제 내용이나 공격 절차는 적지 않습니다.")
    form.kv(
        [
            [("행사명", "2026학년도 화이트해커 교내 보안 세미나 및 CTF")],
            [("일시", "2026년 10월 17일 (금) 13:00 ~ 18:00")],
            [("장소", "본교 ○○관 ○○호. 주최 측이 준비한 실습용 네트워크")],
            [("대상·인원", "본교 재학생 40명 목표. 부원 15명, 일반 재학생 25명")],
            [("목적", "정보보호의 기본을 강의로 다루고, 허가된 실습 환경에서 분석·방어 관점의 문제를 풀어 본다.")],
            [("기대 효과", "참석 40명, 설문 만족도 4.2점 이상, 수료 기준을 채운 인원 30명")],
            [("예산 예", "포스터·문제지 인쇄 8만 원, 다과 12만 원, 상장 3만 원. 합계 23만 원, 사업단 요청")],
        ],
        row_mm=8.6,
    )
    form.paragraph(
        "결과 예시. 실제 참석 32명(목표 대비 80%), 설문 28명 응답, 평균 4.4점, 집행 214,000원, 잔액 16,000원. "
        "아쉬운 점으로 후반 시간 부족을 적고, 다음 행사에서는 강의와 실습 시간을 나눠 잡는다고 적으면 계획과 결과가 연결됩니다.",
        after=6,
    )
    form.paragraph(
        "이 안내와 두 서식은 사업단 공고를 대신하지 않습니다. 공고의 비목, 마감, 제출처가 다르면 공고에 맞춥니다.",
        "label",
        after=4,
        align="LEFT",
    )
    form.save("화이트해커_서식_작성안내")


def main() -> None:
    build_plan()
    build_report()
    build_guide()


if __name__ == "__main__":
    main()
