import turtle as t
from time import sleep


class TableGame(object):
    def __init__(self):
        # 创建背景
        self.gameWindow = t.Screen()
        self.score_left = 0  # 左边得分
        self.score_right = 0  # 右边得分
        self.pen = t.Turtle()  # 创建计分笔对象
        self.pen.ht()  # 计分笔对象隐藏初始箭头

    def create_window(self):
        self.gameWindow.title("乒乓球！")
        self.gameWindow.bgcolor('green')
        self.gameWindow.setup(800, 600)
        # self.gameWindow.tracer(0)  # 禁止自动刷新，在__ball_move方法里面刷新，使屏幕更加的流畅
        self.gameWindow.listen()  # 添加监听

    @staticmethod
    def __player_move_up(player):
        """
        球拍上移
        :param player: 球拍对象，这里指的是笔对象
        :return:
        """
        y = player.ycor()  # 获取y轴坐标
        y += 50  # 坐标上移3
        if y > 270:
            y = 270
        print(y)
        player.sety(y)  # 设置移动后的y坐标

    @staticmethod
    def __player_move_down(player):
        """
        球拍下移
        :param player: 球拍对象，这里指的是笔对象
        :return:
        """
        y = player.ycor()  # 获取y轴坐标
        y -= 50  # 坐标上移3
        if y < -270:
            y = -270
        print(y)
        player.sety(y)  # 设置移动后的y坐标

    def create_player(self, pos=(-350, 0), key_up='w', key_down='s'):
        # 创建球拍player（本质是创建画笔）
        player = t.Turtle()
        player.ht()  # 隐藏画笔（hideturtle）
        player.up()  # 抬起笔，防止运动时笔画轨迹出现
        player.speed(0)  # 加速完成
        player.color("yellow")
        player.shape("square")
        player.shapesize(5, 1)  # 设置长宽比
        player.goto(pos)
        player.st()  # 展示画笔（showturtle）
        # 让球拍上下动起来
        self.gameWindow.onkey(fun=lambda: self.__player_move_up(player=player), key=key_up)  # 按w键上移
        self.gameWindow.onkey(fun=lambda: self.__player_move_down(player=player), key=key_down)  # 按s键下移
        return player

    def __ball_move(self, ball=None, speed_x=5, speed_y=5, player1=None, player2=None):
        """
        移动小球的方法
        :param ball:球对象
        :param speed_x: 小球在水平方向上的移动速度
        :param speed_y: 小球在垂直方向上的移动速度
        :return:
        """
        while True:
            self.gameWindow.update()  # 刷新屏幕
            ball.setx(ball.xcor() + speed_x)
            ball.sety(ball.ycor() + speed_y)
            if ball.xcor() >= 390:
                ball.goto(0, 0)
                self.score_right += 1
                self.__count_score()
                print("\a")
                sleep(0.2)
                print("球右边出界！左边分数%d" % self.score_right)
                # speed_x *= -1  # 左界限
            elif ball.xcor() <= -390:
                ball.goto(0, 0)
                self.score_left += 1
                self.__count_score()
                print("\a")
                sleep(0.2)
                print("球左边出界！右边分数%d" % self.score_left)
                # speed_x *= -1  # 右界限
            elif ball.ycor() >= 290 or ball.ycor() <= -290:
                speed_y *= -1  # 上下界限
                print("\a")
            # 球拍接球
            elif ball.xcor() >= 340 and ball.ycor() >= player2.ycor() - 50 and ball.ycor() <= player2.ycor() + 50:
                speed_x *= -1
                ball.setx(339)
                print("\a")
            elif ball.xcor() <= -340 and ball.ycor() >= player1.ycor() - 50 and ball.ycor() <= player1.ycor() + 50:
                speed_x *= -1
                ball.setx(-339)
                print("\a")

    def create_ball(self, player1, player2):
        # 创建桌球（本质是创建画笔）
        ball = t.Turtle()
        ball.up()  # 抬起笔，防止运动时笔画轨迹出现
        ball.speed(0)  # 加速完成
        ball.color("white")
        ball.shape("circle")
        ball.shapesize(1, 1)  # 设置长宽比
        ball.goto(0, 0)
        self.__ball_move(ball=ball, player1=player1, player2=player2)  # 让球动起来

    def __count_score(self):
        """
        计分笔对象计分
        :return:
        """
        self.pen.up()
        self.pen.goto(0, 250)
        self.pen.color("white")
        self.pen.clear()
        self.pen.write("%d : %d" % (self.score_right, self.score_left), align="center", font=("Arial", 20, "normal"))

    def game_start(self):
        tg = TableGame()  # 创建游戏对象
        tg.create_window()  # 创建窗口背景
        tg.__count_score()  # 显示计分板
        p1 = tg.create_player(pos=(-350, 0), key_down='s', key_up='w')  # 创建左边球拍对象
        p2 = tg.create_player(pos=(350, 0), key_down='Down', key_up='Up')  # 创建右边球拍对象
        tg.create_ball(player1=p1, player2=p2)  # 创建球
        self.gameWindow.mainloop()  # 游戏循环


if __name__ == '__main__':
    tg = TableGame()
    tg.game_start()
