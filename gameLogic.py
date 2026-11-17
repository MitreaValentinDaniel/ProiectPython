import pygame
import librosa
import numpy as np

# Inițializăm pygame și mixerul audio
pygame.init()
pygame.mixer.init()

leftKey = pygame.K_f
rightKey = pygame.K_j
upKey = pygame.K_h
downKey = pygame.K_g
score = -0


class GameLogic:
    leftArrow = pygame.image
    rightArrow = pygame.image
    upArrow = pygame.image
    downArrow = pygame.image
    arrowPosX = 700
    distanceBetweenArrows = 110
    arrowsPosY = 100

    arrowHeight = 64
    arrowWidth = 64

    arrowEntityVector = []

    leftVectorArrows = []
    rightVectorArrows = []
    upVectorArrows = []
    downVectorArrows = []

    def __init__(self):

        print("Game Logic Assets initialised")
        self.leftArrow = pygame.image.load("assets/leftArrow.png")
        self.rightArrow = pygame.image.load("assets/rightArrow.png")
        self.upArrow = pygame.image.load("assets/upArrow.png")
        self.downArrow = pygame.image.load("assets/downArrow.png")

        self.PressedLeftArrow = pygame.image.load("assets/PressedleftArrow.png")
        self.PressedRightArrow = pygame.image.load("assets/PressedrightArrow.png")
        self.PressedUpArrow = pygame.image.load("assets/PressedupArrow.png")
        self.PressedDownArrow = pygame.image.load("assets/PresseddownArrow.png")

        self.font = pygame.font.SysFont(None, 24)

        # --- ANALIZĂ SPECTRALĂ ȘI DE AMPLITUDINE (RMS & ONSETS) ---
        audio_path = "assets/song.mp3"
        print("Serulează analiza spectrală și de amplitudine a melodiei...")
        y, sr = librosa.load(audio_path)

        # 1. Calculăm energia RMS (amplitudinea melodiei în timp)
        rms = librosa.feature.rms(y=y)[0]
        mean_rms = np.mean(rms)  # Pragul mediu de amplitudine

        # 2. Detectăm momentele de atac (onsets)
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr) * 1000  # în milisecunde

        # 3. Generăm săgeți doar pe momentele unde amplitudinea depășește un prag semnificativ
        arrow_types = ["left", "down", "up", "right"]
        self.songChart = []

        for i, t_ms in enumerate(onset_times):
            # Aflăm cadrul corespunzător timpului din melodie
            frame_idx = librosa.time_to_frames(t_ms / 1000.0, sr=sr)

            if frame_idx < len(rms):
                amplitude = rms[frame_idx]

                # Generăm săgeată doar dacă amplitudinea este suficient de puternică (evităm zgomotul de fundal)
                if amplitude > mean_rms * 0.7:
                    # Distribuim tipul de săgeată în funcție de nivelul amplitudinii sau ciclic
                    a_type = arrow_types[i % len(arrow_types)]
                    self.songChart.append((int(t_ms), a_type))

        self.chartIndex = 0
        print(f"S-au generat {len(self.songChart)} săgeți bazate pe amplitudinea și ritmul melodiei!")

        # Pornim melodia și reținem timpul de start pentru sincronizare precisă
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        self.music_start_ticks = pygame.time.get_ticks()

        pass

    def update(self, screen):
        global score
        keys = pygame.key.get_pressed()

        screen.blit(self.leftArrow, (self.arrowPosX, self.arrowsPosY))
        screen.blit(self.downArrow, (self.arrowPosX + self.distanceBetweenArrows, self.arrowsPosY))
        screen.blit(self.upArrow, (self.arrowPosX + self.distanceBetweenArrows * 2, self.arrowsPosY))
        screen.blit(self.rightArrow, (self.arrowPosX + self.distanceBetweenArrows * 3, self.arrowsPosY))

        hit_tolerance = 30

        # --- GENERARE AUTOMATĂ DUPĂ TIMPUL MELODIEI (SINCRONIZAT CU GET_TICKS) ---
        currentSongTime = pygame.time.get_ticks() - self.music_start_ticks

        if self.chartIndex < len(self.songChart):
            targetTime, arrowType = self.songChart[self.chartIndex]
            travelTimeOffset = 1200  # Timpul necesar săgeții să urce pe ecran

            if currentSongTime + travelTimeOffset >= targetTime:
                if arrowType == "left":
                    self.arrowEntityVector.append(
                        ArrowEntity(self.arrowPosX, screen.get_height() - self.arrowHeight, self.leftArrow, "left"))
                elif arrowType == "down":
                    self.arrowEntityVector.append(
                        ArrowEntity(self.arrowPosX + self.distanceBetweenArrows, screen.get_height() - self.arrowHeight,
                                    self.downArrow, "down"))
                elif arrowType == "up":
                    self.arrowEntityVector.append(ArrowEntity(self.arrowPosX + self.distanceBetweenArrows * 2,
                                                              screen.get_height() - self.arrowHeight, self.upArrow,
                                                              "up"))
                elif arrowType == "right":
                    self.arrowEntityVector.append(ArrowEntity(self.arrowPosX + self.distanceBetweenArrows * 3,
                                                              screen.get_height() - self.arrowHeight, self.rightArrow,
                                                              "right"))

                self.chartIndex += 1
        # ---------------------------------------------

        if keys[leftKey]:
            screen.blit(self.PressedLeftArrow, (self.arrowPosX, self.arrowsPosY))
            for arrow in self.arrowEntityVector[:]:
                if arrow.posX == self.arrowPosX and abs(arrow.posY - self.arrowsPosY) <= hit_tolerance:
                    score += 100
                    print(f"HIT LEFT! Score: {score}")
                    self.arrowEntityVector.remove(arrow)
                    break

        if keys[rightKey]:
            screen.blit(self.PressedRightArrow, (self.arrowPosX + self.distanceBetweenArrows * 3, self.arrowsPosY))
            for arrow in self.arrowEntityVector[:]:
                if arrow.posX == self.arrowPosX + self.distanceBetweenArrows * 3 and abs(
                        arrow.posY - self.arrowsPosY) <= hit_tolerance:
                    score += 100
                    print(f"HIT RIGHT! Score: {score}")
                    self.arrowEntityVector.remove(arrow)
                    break

        if keys[upKey]:
            screen.blit(self.PressedUpArrow, (700 + self.distanceBetweenArrows * 2, self.arrowsPosY))
            for arrow in self.arrowEntityVector[:]:
                if arrow.posX == self.arrowPosX + self.distanceBetweenArrows * 2 and abs(
                        arrow.posY - self.arrowsPosY) <= hit_tolerance:
                    score += 100
                    print(f"HIT UP! Score: {score}")
                    self.arrowEntityVector.remove(arrow)
                    break

        if keys[downKey]:
            screen.blit(self.PressedDownArrow, (700 + self.distanceBetweenArrows * 1, self.arrowsPosY))
            for arrow in self.arrowEntityVector[:]:
                if arrow.posX == self.arrowPosX + self.distanceBetweenArrows and abs(
                        arrow.posY - self.arrowsPosY) <= hit_tolerance:
                    score += 100
                    print(f"HIT DOWN! Score: {score}")
                    self.arrowEntityVector.remove(arrow)
                    break

        # Test manual cu tastele F, G, H, J
        # if keys[pygame.K_f]:
        #     self.arrowEntityVector.append(
        #         ArrowEntity(self.arrowPosX, screen.get_height() - self.arrowHeight, self.leftArrow, "left"))
        # if keys[pygame.K_g]:
        #     self.arrowEntityVector.append(
        #         ArrowEntity(self.arrowPosX + self.distanceBetweenArrows, screen.get_height() - self.arrowHeight,
        #                     self.downArrow, "down"))
        # if keys[pygame.K_h]:
        #     self.arrowEntityVector.append(
        #         ArrowEntity(self.arrowPosX + self.distanceBetweenArrows * 2, screen.get_height() - self.arrowHeight,
        #                     self.upArrow, "up"))
        # if keys[pygame.K_j]:
        #     self.arrowEntityVector.append(
        #         ArrowEntity(self.arrowPosX + self.distanceBetweenArrows * 3, screen.get_height() - self.arrowHeight,
        #                     self.rightArrow, "right"))

        for arrow in self.arrowEntityVector[:]:
            arrow.update(screen, score)
            if arrow.posY < -50:
                self.arrowEntityVector.remove(arrow)

        # Draw the score smaller and right above the arrows
        scoreSurface = self.font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(scoreSurface, (self.arrowPosX, 50))


class ArrowEntity:
    posX = 0
    posY = 0
    speed = 6
    image = pygame.image
    arrowType = ""

    def __init__(self, posX, posY, image, arrowType=""):
        self.posX = posX
        self.posY = posY
        self.image = image
        self.arrowType = arrowType
        pass

    def update(self, screen, score):
        self.posY -= self.speed

        screen.blit(self.image, (self.posX, self.posY))