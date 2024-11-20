import pygame
import pandas as pd
import numpy as np

# Pygame 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stellar Evolution Simulation")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
STAR_COLORS = [
    (135, 206, 250),  # ZAMS - 푸른빛 (뜨겁고 젊은 별)
    (173, 216, 230),  # MS - 밝은 파랑
    (255, 223, 186),  # TAMS - 노란빛
    (255, 160, 122),  # 수소껍질 연소 - 연주황
    (255, 127, 80),   # SGB - 주황색
    (255, 69, 0),     # RGB - 적색거성 가지
    (255, 20, 147),   # 1차 준설과정 - 핑크빛
    (240, 230, 140),  # 헬륨 섬광 - 옅은 황색
    (255, 215, 0),    # HB - 황금빛
    (255, 140, 0),    # 전점근거성 가지 - 짙은 주황색
    (205, 92, 92),    # 열적제동점근거성 가지 - 진한 붉은색
    (75, 0, 130),     # 후점근 가지 - 자주빛
    (176, 224, 230),  # 행성상 성운 - 옅은 청록색
    (211, 211, 211),  # 백색왜성 전단계 - 회백색
    (255, 255, 255)   # 백색왜성 - 흰색
]


STAR_SIZES = [
    20,  # ZAMS
    25,  # MS
    30,  # TAMS
    35,  # 수소껍질 연소
    40,  # SGB
    70,  # RGB
    65,  # 1차 준설과정
    50,  # 헬륨 섬광
    45,  # HB
    55,  # 전점근거성 가지
    60,  # 열적제동점근거성 가지
    70,  # 후점근거성 가지
    35,  # 행성상 성운
    15,  # 백색왜성 전단계
    5    # 백색왜성
]


# 폰트
font_path="malgun.ttf"
font = pygame.font.Font(font_path, 24)
afont = pygame.font.Font(font_path, 12)

# 슬라이더 설정
slider_x = WIDTH // 2 - 150
slider_y = HEIGHT - 50
slider_width = 300
slider_height = 10
slider_pos = 0
slider_dragging = False

# 진화 단계
evolution_stages = [
    "영년주계열(ZAMS)", "주계열(MS)", "말년주계열(TAMS)", 
    "수소껍질 연소", "준거성 가지(SGB)",
    "적색거성 가지(RGB)", "1차 준설과정",
    "헬륨 섬광", "수평 가지(HB)",
    "전점근거성 가지", "열적제동점근거성 가지",
    "후점근거성 가지", "행성상 성운",
    "백색왜성 전단계", "백색왜성"
]

# 슬라이더 단계 전환 기준 (0.0 ~ 1.0 사이의 비율)
stage_thresholds = [
    0.0,
    0.02, 0.09, 0.10,
    0.12, 0.16,
    0.26, 0.29,
    0.35, 0.45,
    0.53, 0.65,
    0.70, 0.78,
    0.90, 1.1
]

# 데이터 로드
file_path = "HRdiagram.csv"
data = pd.read_csv(file_path)

# NaN 값 제거 또는 대체
data = data.dropna()  # NaN 값 제거
coordinates = data[['x', 'y']].values  # 필요한 좌표만 가져오기

# H-R 다이어그램 크기 설정
HR_X_MIN, HR_X_MAX = np.min(data['x']), np.max(data['x'])
HR_Y_MIN, HR_Y_MAX = np.min(data['y']), np.max(data['y'])
HR_WIDTH, HR_HEIGHT = 300, 400
HR_TOP_LEFT_X = WIDTH - 350
HR_TOP_LEFT_Y = 100

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if slider_x <= event.pos[0] <= slider_x + slider_width and slider_y - 10 <= event.pos[1] <= slider_y + 10:
                slider_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            slider_dragging = False
        elif event.type == pygame.MOUSEMOTION and slider_dragging:
            # 슬라이더를 드래그 중일 때
            slider_pos = event.pos[0] - slider_x
            slider_pos = max(0, min(slider_pos, slider_width))  # 슬라이더 범위 제한

    # 현재 슬라이더 비율 계산 (0.0 ~ 1.0)
    slider_ratio = slider_pos / slider_width

    # H-R 다이어그램의 점 위치 계산
    data_index = int(slider_ratio * (len(data) - 1))
    hr_x, hr_y = coordinates[data_index]
    hr_point_x = int(HR_TOP_LEFT_X + (hr_x - HR_X_MIN) / (HR_X_MAX - HR_X_MIN) * HR_WIDTH)
    hr_point_y = int(HR_TOP_LEFT_Y + (1 - (hr_y - HR_Y_MIN) / (HR_Y_MAX - HR_Y_MIN)) * HR_HEIGHT)

    # 현재 단계 계산
    current_stage_index = 0
    for i in range(len(stage_thresholds) - 1):
        if stage_thresholds[i] <= slider_ratio < stage_thresholds[i + 1]:
            current_stage_index = i
            break
    current_stage = evolution_stages[current_stage_index]
    star_color = STAR_COLORS[current_stage_index]
    star_size = STAR_SIZES[current_stage_index]

    # 화면 업데이트
    screen.fill(BLACK)

    # 왼쪽 상단: 별
    pygame.draw.circle(screen, star_color, (150, HEIGHT // 2), star_size)

    # 오른쪽: H-R 다이어그램
    pygame.draw.rect(screen, WHITE, (HR_TOP_LEFT_X, HR_TOP_LEFT_Y, HR_WIDTH, HR_HEIGHT), 1)
    x_axis_label = afont.render("log(T_e)", True, WHITE)
    y_axis_label = afont.render("log(L/L_sun)", True, WHITE)
    screen.blit(x_axis_label, (HR_TOP_LEFT_X + HR_WIDTH // 2 - x_axis_label.get_width() // 2, HR_TOP_LEFT_Y + HR_HEIGHT + 20))
    screen.blit(y_axis_label, (HR_TOP_LEFT_X - y_axis_label.get_width() - 10, HR_TOP_LEFT_Y + HR_HEIGHT // 2 - y_axis_label.get_height() // 2))

    # 데이터 포인트 그리기
    for x, y in coordinates:
        x_pos = int(HR_TOP_LEFT_X + (x - HR_X_MIN) / (HR_X_MAX - HR_X_MIN) * HR_WIDTH)
        y_pos = int(HR_TOP_LEFT_Y + (1 - (y - HR_Y_MIN) / (HR_Y_MAX - HR_Y_MIN)) * HR_HEIGHT)
        pygame.draw.circle(screen, WHITE, (x_pos, y_pos), 2)

    # 현재 단계 점
    pygame.draw.circle(screen, star_color, (hr_point_x, hr_point_y), 6)

    # 하단: 슬라이더
    pygame.draw.rect(screen, WHITE, (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.circle(screen, WHITE, (slider_x + slider_pos, slider_y + slider_height // 2), 8)

    # 화면 하단: 현재 단계 텍스트
    stage_info = font.render(f"단계: {current_stage}", True, WHITE)
    screen.blit(stage_info, (slider_x, slider_y - 40))

    # 화면 표시
    pygame.display.flip()

pygame.quit()
