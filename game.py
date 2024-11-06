import pygame
import random
import time

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption("横向躲避障碍物")

# 定义颜色
black = (0, 0, 0)
white = (255, 255, 255)

# 加载并缩放图片
try:
    player_image = pygame.image.load('car.jpg')  # 汽车图片
    player_image = pygame.transform.scale(player_image, (50, 50))  # 缩放到50x50像素
    obstacle_image = pygame.image.load('th.jpg')  # 障碍物图片
    obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))  # 缩放到50x50像素
    background_image = pygame.image.load('background.jpg')  # 背景图片
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # 缩放到屏幕尺寸
except pygame.error as e:
    print(f"无法加载图片：{e}")
    exit()

# 玩家汽车设置
player_x = 0  # 玩家始终在屏幕最左侧
player_y = screen_height / 2  # 初始位置在屏幕中间

# 障碍物设置
obstacle_speed = 5
obstacles = []  # 障碍物列表
game_start_time = time.time()  # 记录游戏开始时间

# 游戏状态
running = True
game_over = False
crashes = 0
max_crashes = 3

# 加载字体
font = pygame.font.Font(None, 36)

# 生成新的障碍物
def generate_obstacle():
    obstacles.append([screen_width, random.randrange(0, screen_height - 50)])

# 游戏主循环
while running:
    current_time = time.time()
    dt = current_time - game_start_time  # 计算游戏运行时间

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and game_over:
                running = False
            elif event.key == pygame.K_c and game_over:
                game_over = False
                crashes = 0
                obstacles.clear()
                generate_obstacle()  # 重新生成障碍物
                player_x = 0
                player_y = screen_height / 2
                game_start_time = current_time  # 重置游戏开始时间

    if not game_over:
        # 玩家移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= 5
        if keys[pygame.K_DOWN] and player_y < screen_height - 50:
            player_y += 5

        # 根据游戏时间增加障碍物生成速度和移动速度
        obstacle_speed = 5 + int(dt / 5)  # 每过5秒，速度增加1
        generate_obstacle_chance = 50 - int(dt / 10)  # 每过5秒，生成障碍物的几率增加1
        if generate_obstacle_chance > 0 and random.randint(0, generate_obstacle_chance) == 1:  # 每隔一段时间生成一个新的障碍物
            generate_obstacle()

        # 障碍物移动
        for i in range(len(obstacles) - 1, -1, -1):
            obstacle = obstacles[i]
            obstacle[0] -= obstacle_speed
            if obstacle[0] < -50:  # 移除屏幕外的障碍物
                obstacles.pop(i)
            else:
                obstacles[i][0] = obstacle[0]  # 更新障碍物位置

        # 检查碰撞
        collision = False
        for obstacle in obstacles:
            if player_x < obstacle[0] + 50 and player_x + 50 > obstacle[0] and player_y < obstacle[1] + 50 and player_y + 50 > obstacle[1]:
                crashes += 1
                collision = True
                obstacles.remove(obstacle)  # 移除发生碰撞的障碍物
                break

        if collision:
            if crashes >= max_crashes:
                game_over = True
            else:
                generate_obstacle()  # 生成新的障碍物

        # 绘制背景
        screen.blit(background_image, (0, 0))

        # 绘制障碍物
        for obstacle in obstacles:
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

        # 绘制玩家
        screen.blit(player_image, (player_x, player_y))

    else:
        # 游戏结束界面
        screen.fill(white)
        text = font.render("Game over! Press C to start over or Q to exit", True, black)
        text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(text, text_rect)

    # 更新屏幕
    pygame.display.flip()

    # 控制游戏刷新速度
    pygame.time.Clock().tick(60)

# 退出游戏
pygame.quit()
