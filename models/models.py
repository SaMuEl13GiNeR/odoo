#-*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import string
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
import math



def name_generator():
    letters = list(string.ascii_lowercase)
    first = list(string.ascii_uppercase)
    vocals = ['a', 'e', 'i', 'o', 'u', 'y', '']
    name = random.choice(first)
    for i in range(0, random.randint(3, 5)):
        name = name + random.choice(letters) + random.choice(vocals)
    return name



class pirates(models.Model):
    _name = 'pirates.pirates'
    _description = 'pirates.pirates'

    name = fields.Char()
    avatar  = fields.Image(related="pirates_type.avatar")
    avatar_min = fields.Image(related="avatar", max_width=50, max_height=50)
    pirates_type = fields.Many2one("pirates.pirates_type", string='Tipo', ondelete='restrict')
    tripulacion = fields.Many2one("pirates.player", string='Tripulacion', ondelete='restrict')
    ganancias_generadas = fields.Integer(default=0)


    @api.model
    def procude_ganancias(self): #ORM CRON
        for b in self.search([]):
            b.ganancias_generadas = b.ganancias_generadas + b.pirates_type.ganancias
            
    def procude_ganancias2(self):
        for b in self:
            # produce_ganancias()
            b.ganancias_generadas = b.ganancias_generadas + b.pirates_type.ganancias





class barco(models.Model):
    _name = 'pirates.barco'
    _description = 'pirates.barco'

    name = fields.Char()
    barco_type = fields.Many2one("pirates.barco_type", string='Tipo', ondelete='restrict')
    tripulacion = fields.Many2one("pirates.player", string='Tripulacion', ondelete='restrict')
    canyones = fields.Integer()
    avatar  = fields.Image(related="barco_type.avatar")
    avatar_min = fields.Image(related="barco_type.avatar", max_width=50, max_height=50)



class player(models.Model):
    _name = 'pirates.player'
    _description = 'pirates.player'

    name = fields.Char()
    password = fields.Char()
    avatar = fields.Image(max_width=200, max_height=200)
    avatar_min = fields.Image(related="avatar", max_width=50, max_height=50)

    name_tripulacion = fields.Char()
    pirates = fields.One2many('pirates.pirates', 'tripulacion', string='Pirates')
    pirates2 = fields.One2many(related="pirates")
    barco = fields.One2many('pirates.barco', 'tripulacion', string='Barco')
    barco2 = fields.One2many(related="barco")

    total_dmg = fields.Integer(compute="_total_dmg")
    total_ganancias = fields.Integer(compute="_total_ganancias", default=0)
    ganancias_actuales = fields.Integer(default=0)
    gastos = fields.Integer()
    tamano_tripulacion = fields.Integer(default=0)
    pirates_type_disponibles = fields.Many2many('pirates.pirates_type', compute="_get_available_pirates")
    required_money = fields.Integer(compute="_required_money")

    progress_ganancias = fields.Float(compute="_get_progress", default=0)

    @api.depends('pirates', 'barco')
    def _total_dmg(self):
        for player in self: 
            total = 0
            for pirate in player.pirates:
                total += pirate.pirates_type.dmg
            for barco in player.barco:
                total += barco.barco_type.dmg * barco.barco_type.ataques * barco.canyones
            player.total_dmg = total


    @api.depends('pirates')
    def _total_ganancias(self):
        for player in self: 
            total = 0
            for pirate in player.pirates:
                total += pirate.ganancias_generadas
            player.total_ganancias = total
            player.ganancias_actuales = total - player.gastos

            

    def ampliar_tripulacion(self):  # ORM
        for c in self:
            if (c.required_money <= c.ganancias_actuales):
                c.tamano_tripulacion += 1
                c.gastos = c.gastos + c.required_money

           
    @api.depends('tamano_tripulacion')
    def _get_available_pirates(self):  # ORM
        for c in self:
            c.pirates_type_disponibles = self.env['pirates.pirates_type'].search([('tamano_tripulacion', '<=', c.tamano_tripulacion)])

    
    @api.depends('tamano_tripulacion')
    def _required_money(self):  # ORM
        for c in self:
            c.required_money = 10 ** c.tamano_tripulacion


    @api.depends('total_ganancias', 'ganancias_actuales')
    def _get_progress(self):
        for player in self: 
            player.progress_ganancias = player.ganancias_actuales * 100 / player.total_ganancias



    @api.constrains('name')
    def check_name_length(self):
        for player in self:
            if len(player.name) < 3:
                raise ValidationError("Your name is too small: %s" % player.name)


class pirates_type(models.Model):
    _name = 'pirates.pirates_type'
    _description = 'pirates.pirates_type'

    name = fields.Char()


    dmg = fields.Integer()
    hp = fields.Integer()
    ganancias = fields.Integer()
    ataques = fields.Integer()
    tamano_tripulacion= fields.Integer()

    avatar = fields.Image(max_width=200, max_height=200)
    avatar_min = fields.Image(related="avatar", max_width=50, max_height=50)


    def reclute(self):  # ORM
        for s in self:
            player = self.env['pirates.player'].browse(self.env.context['ctx_player'])
            print('parent.id de pirates_type', player)
            player.gastos = player.gastos + s.ganancias
            player.pirates.create({
                "name": name_generator(),
                "pirates_type": s.id,
                "tripulacion": player.id,
            })


class barco_type(models.Model):
    _name = 'pirates.barco_type'
    _description = 'pirates.barco_type'

    name = fields.Char()

    dmg = fields.Integer()
    hp = fields.Integer()
    ataques = fields.Integer()

    avatar = fields.Image(max_width=200, max_height=200)
    avatar_min = fields.Image(related="avatar", max_width=50, max_height=50)




class battle(models.Model):
    _name = 'pirates.battle'
    _description = 'Battles'

    name = fields.Char()
    
    date_start = fields.Datetime()
    date_end = fields.Datetime()

    player1 = fields.Many2one('pirates.player')
    player2 = fields.Many2one('pirates.player')

    pirates1 = fields.Many2one('pirates.pirates')
    pirates2 = fields.Many2one('pirates.pirates')


    @api.onchange('player1')
    def onchange_player1(self):
        self.name = self.player1.name
        return {
            'domain': {
                'pirates1': [('id', 'in', self.player1.pirates.ids)],
                'player2': [('id', '!=', self.player1.id)],
            }
        }

    @api.onchange('player2')
    def onchange_player2(self):
        return {
            'domain': {
                'pirates2': [('id', 'in', self.player2.pirates.ids)],
                'player1': [('id', '!=', self.player2.id)],
            }
        }




                


            

           

