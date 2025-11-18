import pygame

from 	player 	import Player
from 	monster import Monster
from 	monster import Mummy
from 	monster import Alien
from 	sounds 	import SoundManager
from 	comet_event import CometFallEvent

class Game:
	def __init__(self):
		self.is_playing = False 
		self.pressed = {}
		self.sound_manager = SoundManager()
		self.all_monsters = pygame.sprite.Group()

		self.player = Player(self)
		self.all_players = pygame.sprite.Group()
		self.all_players.add(self.player)
		self.font = pygame.font.SysFont("monospace", 25, True)
		self.score = 0

		self.comet_event = CometFallEvent(self)

	def start(self):
		self.is_playing = True
		self.spawn_monster(Mummy)
		self.spawn_monster(Mummy)
		self.spawn_monster(Alien)
	
	def game_over(self):
		# retirer les montres, pv player = max_health, jeu en attente
		self.all_monsters 	= pygame.sprite.Group()
		self.comet_event = CometFallEvent(self)
		self.player.health 	= self.player.max_health
		self.is_playing 	= False
		self.comet_event.reset_percent()
		self.score = 0
		self.sound_manager.play('game_over')
	
	def add_score(self, score=10):
		self.score += score
	
	def update(self, screen):
		score_texte = self.font.render(f"Score : {self.score}", 1, (0, 0, 0))
		screen.blit(score_texte, (20, 20))
		
		screen.blit(self.player.image, self.player.rect)

		for projectile in self.player.all_projectile:
			projectile.move()
		
		for monster in self.all_monsters:
			monster.forward()
			monster.update_health_bar(screen)
			monster.update_animation()
		
		for comet in self.comet_event.all_comets:
			comet.fall()
		
		self.all_monsters.draw(screen)

		self.player.all_projectile.draw(screen)
		self.player.update_health_bar(screen)

		self.player.update_animation()

		self.comet_event.all_comets.draw(screen)
		self.comet_event.update_bar(screen)

		if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
			self.player.move_rigt()
		elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
			self.player.move_left()

	def spawn_monster(self, monster_class_name):
		self.all_monsters.add(monster_class_name.__call__(self))
	
	def check_collision(self, sprite, group):
		return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)