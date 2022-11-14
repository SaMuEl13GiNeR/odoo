#-*- coding: utf-8 -*-

from odoo import models, fields, api


class pirates(models.Model):
    _name = 'pirates.pirates'
    _description = 'pirates.pirates'

    name = fields.Char()
    avatar  = fields.Image(related="pirates_type.avatar")
    avatar_min = fields.Image(related="avatar", max_width=50, max_height=50)
    pirates_type = fields.Many2one("pirates.pirates_type", string='Tipo', ondelete='restrict')
    tripulacion = fields.Many2one("pirates.player", string='Tripulacion', ondelete='restrict')


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
    barco = fields.One2many('pirates.barco', 'tripulacion', string='Barco')

    total_dmg = fields.Integer(compute="_total_dmg")

    @api.depends('pirates', 'barco')
    def _total_dmg(self):
        for player in self: 
            total = 0
            for pirate in player.pirates:
                total += pirate.pirates_type.dmg
            for barco in player.barco:
                total += barco.barco_type.dmg * barco.barco_type.ataques * barco.canyones
            player.total_dmg = total


    
class pirates_type(models.Model):
    _name = 'pirates.pirates_type'
    _description = 'pirates.pirates_type'

    name = fields.Char()


    dmg = fields.Integer()
    hp = fields.Integer()
    ganancias = fields.Integer()
    ataques = fields.Integer()

    avatar = fields.Image(max_width=200, max_height=200)
    avatar_min = fields.Image(related="avatar", max_width=50, max_height=50)


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
