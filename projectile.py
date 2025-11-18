import pygame

class Projectile(pygame.sprite.Sprite):
	def __init__(self, player):
		super().__init__()
		self.velocity = 7
		self.player = player
		self.image = pygame.image.load('assets/projectile.png')
		self.image = pygame.transform.scale(self.image, (40, 40))
		self.rect = self.image.get_rect()
		self.rect.x = player.rect.x + 120
		self.rect.y = player.rect.y + 80
		self.origin_image = self.image
		self.angle = 0
	
	def remove(self):
		self.player.all_projectile.remove(self)
	
	def rotate(self):
		self.angle -= -2 
		self.image = pygame.transform.rotate(self.origin_image, self.angle)
		self.rect = self.image.get_rect(center=self.rect.center)
	
	def move(self):
		self.rect.x += self.velocity
		self.rotate()

		for monster in  self.player.game.check_collision(self, self.player.game.all_monsters) :
			self.remove()
			monster.damage(self.player.attack)
		
		if self.rect.x > 1080:
			self.remove()