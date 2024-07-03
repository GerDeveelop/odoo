


from odoo import models, fields, api


class GeneroPelicula(models.Model):
    _name='genero.peliculas'


    genero_pelicula = fields.Char(string='Genero de la pelicula')
    