import sys, pygame, random

class Breakout():

    def instructions(self):
        pygame.init()            

        SIZE = WIDTH, HEIGHT = (1024, 720)
        FPS = 30
        screen = pygame.display.set_mode(SIZE, pygame.RESIZABLE)
        clock = pygame.time.Clock()


        def blit_text(surface, text, pos, font, color=pygame.Color('black')):
            words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
            space = font.size(' ')[0]  # The width of a space.
            max_width, max_height = surface.get_size()
            x, y = pos
            for line in words:
                for word in line:
                    word_surface = font.render(word, 0, color)
                    word_width, word_height = word_surface.get_size()
                    if x + word_width >= max_width:
                        x = pos[0]  # Reset the x.
                        y += word_height  # Start on new row.
                    surface.blit(word_surface, (x, y))
                    x += word_width + space
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.


        text = "Controls:\n 1.Use left and right arrows to move the paddle\n 2.Press F to play the game in full-screen mode\n 3. Press P to pause the music\n 4.Press R to resume the music play\n 4. Press esc to exit from the game.\n 5.Bonus life is given when the score is greater than 200 and lives=1"
        font = pygame.font.SysFont('Times New Roman', 40)

        while True:

            dt = clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.main()

            screen.fill(pygame.Color('white'))
            blit_text(screen, text, (20, 20), font)
            pygame.display.update()
   
    def main(self):
          
        xspeed_init = 6
        yspeed_init = 6
        max_lives = 3
        bat_speed = 30
        score = 0 
        bgcolour = 0x2F, 0x4F, 0x4F         
        size = width, height = 640, 480
  

        # main part 
        screen = pygame.display.set_mode(size)


        bat = pygame.image.load("paddle.png").convert()
        batrect = bat.get_rect()

        ball = pygame.image.load("ball.png").convert()
        ball.set_colorkey((255, 255, 255))
        ballrect = ball.get_rect()
       
        pong = pygame.mixer.Sound('gamesound.wav')
        pong.set_volume(10)        
        
        wall = Wall()
        wall.build_wall(width)

        # Initialise ready for game loop
        batrect = batrect.move((width / 2) - (batrect.right / 2), height - 20)
        ballrect = ballrect.move(width / 2, height / 2)       
        xspeed = xspeed_init
        yspeed = yspeed_init
        lives = max_lives
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1,30)       
        pygame.mouse.set_visible(0)       # turn off mouse pointer

        while 1:

            # 60 frames per second
            clock.tick(50)

            # process key presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
        	            sys.exit()
                    if event.key == pygame.K_LEFT:                        
                        batrect = batrect.move(-bat_speed, 0)     
                        if (batrect.left < 0):                           
                            batrect.left = 0      
                    if event.key == pygame.K_RIGHT:                    
                        batrect = batrect.move(bat_speed, 0)
                        if (batrect.right > width):                            
                            batrect.right = width
                    if event.key == pygame.K_f:
                        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                    if event.key == pygame.K_p:
                        pygame.mixer.pause()
                    if event.key == pygame.K_r:
                        pygame.mixer.unpause()



            # check if bat has hit ball    
            if ballrect.bottom >= batrect.top and \
               ballrect.bottom <= batrect.bottom and \
               ballrect.right >= batrect.left and \
               ballrect.left <= batrect.right:
                yspeed = -yspeed                
                pong.play(0)                
                offset = ballrect.center[0] - batrect.center[0]                          
                                    
                if offset > 0:
                    if offset > 30:  
                        xspeed = 7
                    elif offset > 23:                 
                        xspeed = 6
                    elif offset > 17:
                        xspeed = 5 
                else:  
                    if offset < -30:                             
                        xspeed = -7
                    elif offset < -23:
                        xspeed = -6
                    elif xspeed < -17:
                        xspeed = -5     
                      
            # move bat/ball
            ballrect = ballrect.move(xspeed, yspeed)
            if ballrect.left < 0 or ballrect.right > width:
                xspeed = -xspeed                
                pong.play(0)            
            if ballrect.top < 0:
                yspeed = -yspeed                
                pong.play(0)               

            # check if ball has gone past bat - lose a life
            if ballrect.top > height:
                lives -= 1
                # start a new ball
                xspeed = xspeed_init
                rand = random.random()              
                if random.random() > 0.5:
                    xspeed = -xspeed 
                yspeed = yspeed_init            
                ballrect.center = width * random.random(), height / 3                                
                if lives == 0:                    
                    msg = pygame.font.Font(None,70).render("Game Over", True, (0,255,255), bgcolour)
                    lives-=1
                    msgrect = msg.get_rect()
                    msgrect = msgrect.move(width / 2 - (msgrect.center[0]), height / 3)
                    screen.blit(msg, msgrect)
                    pygame.display.flip()
                    
                    while 1:
                        restart = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                    	            sys.exit()
                                if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):                                    
                                    restart = True      
                        if restart:                   
                            screen.fill(bgcolour)
                            wall.build_wall(width)
                            lives = max_lives
                            score = 0
                            break
            
            if xspeed < 0 and ballrect.left < 0:
                xspeed = -xspeed                                
                pong.play(0)

            if xspeed > 0 and ballrect.right > width:
                xspeed = -xspeed                               
                pong.play(0)
           
            # check if ball has hit wall
            # if yes then delete brick and change ball direction
            index = ballrect.collidelist(wall.brickrect)       
            if index != -1: 
                if ballrect.center[0] > wall.brickrect[index].right or \
                   ballrect.center[0] < wall.brickrect[index].left:
                    xspeed = -xspeed
                else:
                    yspeed = -yspeed                
                pong.play(0)              
                wall.brickrect[index:index + 1] = []
                score += 10
                # if score is greater than 200 and lives remaining is 1 then increment by 1
                if score>=200 and lives==1:
                    lives+=1
                          
            screen.fill(bgcolour)
            scoretext = pygame.font.Font(None,40).render("Score: "+str(score), True, (0,255,255), bgcolour)
            livestext = pygame.font.Font(None,40).render("Lives: "+str(lives), True, (0,255,255), bgcolour)
            scoretextrect = scoretext.get_rect()
            livestextrect = livestext.get_rect(topleft=(0, 0))
            scoretextrect = scoretextrect.move(width - scoretextrect.right, 0)
            # livestextrect = livestextrect.move(width - livestextrect.left, 0)
            screen.blit(scoretext, scoretextrect)
            screen.blit(livestext, livestextrect)

            for i in range(0, len(wall.brickrect)):
                screen.blit(wall.brick, wall.brickrect[i])    

            # if wall completely gone then rebuild it
            if wall.brickrect == []:              
                wall.build_wall(width)                
                xspeed = xspeed_init
                yspeed = yspeed_init                
                ballrect.center = width / 2, height / 3
         
            screen.blit(ball, ballrect)
            screen.blit(bat, batrect)
            pygame.display.flip()

class Wall():

    def __init__(self):
        self.brick = pygame.image.load("brick.png").convert()
        brickrect = self.brick.get_rect()
        self.bricklength = brickrect.right - brickrect.left       
        self.brickheight = brickrect.bottom - brickrect.top             

    def build_wall(self, width):        
        xpos = 0
        ypos = 60
        adj = 0
        self.brickrect = []
        for i in range (0, 52):           
            if xpos > width:
                if adj == 0:
                    adj = self.bricklength / 2
                else:
                    adj = 0
                xpos = -adj
                ypos += self.brickheight
                
            self.brickrect.append(self.brick.get_rect())    
            self.brickrect[i] = self.brickrect[i].move(xpos, ypos)
            xpos = xpos + self.bricklength

if __name__ == '__main__':
    br = Breakout()
    br.instructions()
    # br.main()


