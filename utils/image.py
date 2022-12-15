import base64
from io import BytesIO
from pydoc import doc

from PIL import Image, ImageDraw, ImageFont

from models.benefit import Benefit, DiseaseType
from models.user import Doctor, Patient


def base64_to_img(base64_str):
    image = base64.b64decode(base64_str.replace(" ", "+"))
    image = BytesIO(image)
    image = Image.open(image, formats=["PNG"])
    image = image.resize((int(image.width / 4), int(image.height / 4)))
    return image


async def create_image_document(benefit: Benefit, patient: Patient, doctor: Doctor):
    sig_pos = [(790, 965), (770, 1090), (480, 1175)]
    datas = [
        [(380, 210), "V" if benefit.type == DiseaseType.cancer else ""],  # 암 체크
        [(460, 210), "V" if benefit.type == DiseaseType.other else ""],  # 기타 체크
        [(290, 280), f"{patient.healthInsuranceNumber}"],  # 건강보험증 번호
        [(660, 280), f"{patient.name}"],  # 가입자 이름
        [(375, 340), f"{patient.name}"],  # 수신자 이름
        [(300, 365), f"020627"],  # 주민번호 앞자기
        [(430, 365), f"*******"],  # 주민번호 뒷자리
        [(655, 330), "V"],  # 문자메세지 체크
        [(280, 400), f"{patient.id}@dogcoolcodefair.com"],  # 이메일
        [(740, 400), f"{patient.phoneNumber}"],  # 전화번호
        [(280, 425), f"서울특별시 서초구 강남대로 273, 10층"],  # 주소
        [(270, 475), f"신경과"],  # 진단과
        [
            (740, 475),
            f"{benefit.date.year}    {benefit.date.month}    {benefit.date.day}",
        ],  # 진단일 (띄어쓰기 4번)
        [(370, 505), f"{benefit.disease.name}"],  # 질환명
        [(700, 505), f"{benefit.disease.id}"],  # 질병코드
        [(320, 595), "V" if benefit.type == DiseaseType.cancer else ""],  # 암 체크
        [(615, 595), "V" if benefit.type == DiseaseType.other else ""],  # 기타 체크
        [
            (175, 630),
            "V"
            if (benefit.methodIndex == 1 and benefit.type == DiseaseType.cancer)
            else "",
        ],  # 암 - 1
        [
            (175, 690),
            "V"
            if (benefit.methodIndex == 2 and benefit.type == DiseaseType.cancer)
            else "",
        ],  # 암 - 2
        [
            (175, 720),
            "V"
            if (benefit.methodIndex == 3 and benefit.type == DiseaseType.cancer)
            else "",
        ],  # 암 - 3
        [
            (175, 750),
            "V"
            if (benefit.methodIndex == 4 and benefit.type == DiseaseType.cancer)
            else "",
        ],  # 암 - 4
        [
            (175, 780),
            "V"
            if (benefit.methodIndex == 5 and benefit.type == DiseaseType.cancer)
            else "",
        ],  # 암 - 5
        [
            (175, 810),
            "V"
            if (benefit.methodIndex == 6 and benefit.type == DiseaseType.cancer)
            else "",
        ],  # 암 - 6
        [
            (175, 840),
            "V"
            if (benefit.methodIndex == 7 and benefit.type == DiseaseType.cancer)
            else "",
        ],  # 암 - 7
        [
            (550, 650),
            "V"
            if (benefit.methodIndex == 1 and benefit.type == DiseaseType.other)
            else "",
        ],  # 기타 - 1
        [
            (550, 710),
            "V"
            if (benefit.methodIndex == 2 and benefit.type == DiseaseType.other)
            else "",
        ],  # 기타 - 2
        [
            (550, 755),
            "V"
            if (benefit.methodIndex == 3 and benefit.type == DiseaseType.other)
            else "",
        ],  # 기타 - 3
        [
            (550, 785),
            "V"
            if (benefit.methodIndex == 4 and benefit.type == DiseaseType.other)
            else "",
        ],  # 기타 - 4
        [
            (550, 815),
            "V"
            if (benefit.methodIndex == 5 and benefit.type == DiseaseType.other)
            else "",
        ],  # 기타 - 5
        [
            (410, 920),
            f"{benefit.date.year}      {benefit.date.month}      {benefit.date.day}",
        ],  # 진단일 (띄어쓰기 6번)
        [(410, 950), f"{doctor.hospital}"],  # 병원명
        [(460, 980), f"{doctor.name}"],  # 의사명
        [(620, 980), f"{doctor.doctorNumber}"],  # 면허번호
        # [(790, 980), "의사서명파일"], #의사서명파일
        [
            (410, 1065),
            f"{benefit.date.year}      {benefit.date.month}      {benefit.date.day}",
        ],  # 신청일 (띄어쓰기 6번)
        [(650, 1095), f"{patient.name}"],  # 신청자 이름
        # [(770, 1100), "신청자서명파일"], #신청자서명파일
        [
            (500, 1165),
            f"{benefit.date.year}      {benefit.date.month}      {benefit.date.day}",
        ],  # 신청일 (띄어쓰기 6번)
        [(380, 1190), f"{doctor.name}"],  # 신청자 이름 (의사명)
        # [(480, 1190), "의사서명파일"], #의사서명파일
        [(740, 1190), f"{doctor.phoneNumber}"],  # 의사 전화번호
        [(815, 1220), "담당의"],  # 수신자와의 관계
    ]
    target_image = Image.open("./static/base.png")
    font = "./static/NanumGothic.ttf"
    selectedFont = ImageFont.truetype(font, 20)
    draw = ImageDraw.Draw(target_image)
    for data in datas:
        draw.text(data[0], data[1], fill="black", font=selectedFont, align="right")
    [
        target_image.paste(
            base64_to_img(benefit.signature), pos, base64_to_img(benefit.signature)
        )
        for pos in sig_pos
    ]
    return target_image


async def create_image_diagnosis(benefit: Benefit, patient: Patient, doctor: Doctor):
    sig_pos = [(int(840 / 1.5), int(1740 / 1.5))]
    datas = [
        [(390 / 1.5, 530 / 1.5), f"{benefit.disease.name}"],
        [(390 / 1.5, 645 / 1.5), f"{patient.name}"],
        [(945 / 1.5, 645 / 1.5), "020627 - *******"],
        [
            (650 / 1.5, 1460 / 1.5),
            f"{benefit.date.year}      {benefit.date.month}      {benefit.date.day}",
        ],
        [(330 / 1.5, 1550 / 1.5), f"{doctor.hospital}"],
        [(315 / 1.5, 1650 / 1.5), f"{doctor.phoneNumber}"],
        [(450 / 1.5, 1750 / 1.5), f"{doctor.name}"],
        [(630 / 1.5, 1750 / 1.5), f"{doctor.doctorNumber}"],
    ]
    for _ in range(int(len(benefit.memo) / 1.5) + 1):
        datas.append(
            [(390 / 1.5, (870 + 35 * _) / 1.5), benefit.memo[35 * _ : 35 * (_ + 1)]]
        )

    target_image = Image.open("./static/base2.png")
    target_image = target_image.resize(
        (int(target_image.width / 1.5), int(target_image.height / 1.5))
    )
    font = "./static/NanumGothic.ttf"
    selectedFont = ImageFont.truetype(font, 20)
    draw = ImageDraw.Draw(target_image)
    for data in datas:
        draw.text(data[0], data[1], fill="black", font=selectedFont, align="right")
    [
        target_image.paste(
            base64_to_img(benefit.signature), pos, base64_to_img(benefit.signature)
        )
        for pos in sig_pos
    ]
    return target_image
