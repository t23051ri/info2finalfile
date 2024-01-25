import pyxel
import random

class Player:
    def __init__(self, game):
        self.game = game
        self.init_position()

    def init_position(self):
        # プレイヤーの初期位置を設定
        self.x = self.game.width / 2
        self.y = self.game.height
        self.bullets = []

    def update(self):
        # プレイヤーの位置をマウスのX座標に
        self.x = pyxel.mouse_x

        # スペースキーで弾を発射し、敵との衝突判定を処理
        if pyxel.btnr(pyxel.KEY_SPACE) and len(self.bullets) < 20 and not self.game.gameover:
            self.bullets.append([self.x + 7, self.game.height - 25])
            pyxel.play(0, 0)

        for bullet in self.bullets:
            bullet[1] -= 2
            if bullet[1] < 0:
                self.bullets.remove(bullet)

            for enemy in self.game.enemies:
                if self.game.collision_bullet_enemy(bullet[0], bullet[1], enemy.x, enemy.y) and enemy in self.game.enemies:
                    self.game.enemies.remove(enemy)
                    self.game.score += 1
                    pyxel.play(1, 1)

class Enemy:
    def __init__(self, game, x):
        self.game = game
        self.x = x
        self.y = 0

    def update(self):
        # 敵の位置を更新し、画面外に出た場合の処理を行う
        self.y += 1

        if self.y > self.game.height and not self.game.gameover:
            self.game.score -= 1
            self.game.enemies.remove(self)
            pyxel.play(2, 1)

        # プレイヤーとの衝突判定を処理
        if pyxel.frame_count % 60 == 0:
            if self.game.is_enemy_collision(self.x, self.y):
                if self.game.lives > 0:
                    self.game.lives -= 1
                    self.game.color = 9
                    print("Collision")
                    pyxel.play(2, 1)
                else:
                    if self.game.score > self.game.best_score:
                        self.game.best_score = self.game.score
                    self.game.gameover = True
                    self.game.enemies.remove(self)
                    print("game over")
                    pyxel.play(2, 1)

class SpaceInvaderGame:
    def __init__(self, width, height):
        # ゲームの初期化
        pyxel.init(width, height, title="Space Invader")
        self.width = width
        self.height = height
        self.player = Player(self)
        self.enemies = [Enemy(self, random.randint(0, self.width - 20)) for _ in range(10)]
        self.lives = 5
        self.gameover = False
        self.score = 0
        self.color = 11
        self.best_score = 0

        # 背景の星の初期化
        self.stars = [(random.randint(0, self.width), random.randint(0, self.height), random.uniform(1, 2.5)) for _ in range(100)]

        # 音声の初期化
        pyxel.sound(0).set("a3e1", "p", "6", "s", 3)
        pyxel.sound(1).set("e1c1g1c2", "t", "6666", "s", 3)
        pyxel.sound(2).set("c2", "n", "7766543", "s", 3)

        pyxel.play(0, 0, loop=True)
        pyxel.play(1, 1, loop=True)
        pyxel.play(2, 2, loop=True)

    def is_enemy_collision(self, x, y):
        # プレイヤーと敵の衝突判定
        if x >= self.player.x and x <= self.player.x + 20 and y >= self.height - 30 and y <= self.height - 5:
            return True
        return False

    def collision_bullet_enemy(self, bullet_x, bullet_y, enemy_x, enemy_y):
        # 弾と敵の衝突判定
        if bullet_x >= enemy_x and bullet_x <= enemy_x + 8 and bullet_y >= enemy_y and bullet_y <= enemy_y + 8:
            return True
        return False

    def cheat_code(self):
        # チートコードの処理
        if pyxel.btnp(pyxel.KEY_S) and pyxel.btnp(pyxel.KEY_U) and pyxel.btnp(pyxel.KEY_P):
            self.score += 10
        if pyxel.btnp(pyxel.KEY_L) and pyxel.btnp(pyxel.KEY_U) and pyxel.btnp(pyxel.KEY_P):
            self.lives += 10

    def restart_game(self):
        # ゲームのリスタート
        self.player.init_position()
        self.enemies = [Enemy(self, random.randint(0, self.width - 20)) for _ in range(10)]
        self.lives = 5
        self.gameover = False
        self.score = 0
        self.color = 11

    def update(self):
        # ゲームの更新
        self.cheat_code()

        if self.lives == 0:
            self.gameover = True

        self.color = 11

        if pyxel.btnp(pyxel.KEY_Q) and not self.gameover:
            pyxel.quit()

        self.player.update()

        for enemy in self.enemies:
            enemy.update()

        if self.score < 5:
            if pyxel.frame_count % 60 == 0:
                self.enemies.append(Enemy(self, random.randint(0, self.width - 20)))
        elif 5 <= self.score < 15:
            if pyxel.frame_count % 30 == 0:
                self.enemies.append(Enemy(self, random.randint(0, self.width - 20)))
        elif self.score >= 15:
            if pyxel.frame_count % 15 == 0:
                self.enemies.append(Enemy(self, random.randint(0, self.width - 20)))

        if pyxel.btnr(pyxel.KEY_R) and self.gameover:
            self.restart_game()

    def draw(self):
        # ゲームの描画
        pyxel.cls(0)
        for x, y, speed in self.stars:
            y += speed
            if y >= self.height:
                y -= self.height
            pyxel.pset(x, y, 7)

        pyxel.text(self.width - 50, 10, f"score : {str(self.score)}", 2)
        for bullet in self.player.bullets:
            pyxel.rect(bullet[0], bullet[1], 1, 5, 7)

        for enemy in self.enemies:
            pyxel.rect(enemy.x, enemy.y, 8, 8, 8)
        pyxel.text(10, 10, f"remaining lives : {str(self.lives)}", 2)

        pyxel.rect(self.player.x, self.height - 20, 15, 15, self.color)

        if self.gameover:
            pyxel.text(self.width / 2 - 18, self.height / 2, "GAME OVER", 2)
            pyxel.text(self.width / 2 - 34, self.height - 10, "PRESS R TO PLAY AGAIN", 2)

game = SpaceInvaderGame(256, 138)
pyxel.run(game.update, game.draw)