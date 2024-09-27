
import logging

from odoo import models, fields, api
from odoo.exceptions import UserError

#se crea una variable para el loggin.geLogger el cual nos ayuda a leer acciones de algun objeto
logger = logging.getLogger(__name__) 

class Peliculas(models.Model):
    _name = 'peliculas'
    _inherit = ['image.mixin']

    #variable global, el primer campo es el id registrado en la base de datos, el 2 campo es lo que se muestra al cliente.
    MOVI_CLASSIFICATION=[('G','General'),  # publico general
        ('PG','PG'), # se recomienda la compañia de un adulto
        ('PG-13','PG-13'),  # mayor de 13
        ('R','R'),  # se recomienda un adulto responsable
        ('RC-17','RC-17'), # mayores de 18 años
        ] 
    name = fields.Char(string='Nombre de pelicula')

    clasificacion = fields.Selection(MOVI_CLASSIFICATION, string='Clasificacion')
    description_clasification = fields.Char(string='Descripción de clasificación')

    fecha_estreno = fields.Date(string='Fecha estreno')
    puntuacion = fields.Integer(string='Puntuacion', related='puntuacion2')
    puntuacion2 = fields.Integer(string='Puntuacion2') #para dar relacion a puntuacion
    active = fields.Boolean(string='Activo',
                            default=True) # active es una caracteristica especial para la base de datos -> oculta los campos para archivarlos con un checkbox
    director_id = fields.Many2one(
        comodel_name='res.partner',
        string='Director',
    )
    
    director_categories = fields.Many2one(
        comodel_name='res.partner.category',
        string='Director categorias',
        #funcion lambda para buscar categoria dentro de res.partner.category
        default=lambda self: self.env['res.partner.category'].search([('name','=','Director')])
    )
    generos_ids = fields.Many2many(
        comodel_name='genero.peliculas',
        string='Genero',
    )
    
    vista_general = fields.Text(string='Descripcion')
    link_triler = fields.Char(string='Trailer')
    es_libro = fields.Boolean(string='Version libro')
    libro = fields.Binary('Libro')
    #para ver reflejado el nombre del libro se crea un campo "filename" -> libro_filename = tipo char
    libro_filename = fields.Char(string="Nombre del libro")

    #state para los estados del statusbar 
    state = fields.Selection(selection=[
        ('borrador', 'Borrador'),
        ('aprobado', 'Aprobado'),
        ('cancelado', 'Cancelado'),
    ], default='borrador', string="Estados", copy="False")
    fecha_aprobado = fields.Datetime(string="Fecha aprobado", copy="False")

     # @api.depend('helpdesk.ticket')
    # def _compute_tickets_ids(self):
    #     for rec in self:
    #         rec.helpdesk.ticket()

    def borrador_presupuesto(self):
        logger.info('++++++++ funciona!') #usamos logger.info para poder leer la accion si funciona
        self.state = 'borrador'
        
    def aprobar_presupuesto(self):
        self.state = 'aprobado'
    
    def cancelar_presupuesto(self):
        self.state = 'cancelado'
    
    def unlink(self):
        logger.info("se disparo la uncion unlink")
        if self.state != "cancelado":
            raise UserError("no se puede eliminar el registro porque no esta en estado cancelado")
        super(Peliculas, self).unlink()
    #se ve el resgitro de las variables que tienen o no algun dato ingresado
    @api.model
    def create(self, variables):
        logger.info('++++ se disparo la funcion create, indica variables: {0}'.format(variables))
        return super(Peliculas, self).create(variables)
    
    #funcion de la  varible sobreescrita (editar)
    def write(self, variables):
        logger.info('+++ variables: {0}'.format(variables))
        if 'clasificacion' in variables:
            if self.state != 'borrador':
                raise UserError('La clasificacion no se puede editar debes descartar cambios y pasarlo a borrador')
        super(Peliculas, self).write(variables)
    
    #copia para un registro creado
    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + '(copia)'
        return super(Peliculas, self).copy(default)
    
    @api.onchange('MOVI_CLASSIFICATION')
    def _onchange_clasificacion(self):
        if self.MOVI_CLASSIFICATION:
            if self.MOVI_CLASSIFICATION == 'G':
                self.description_clasification = 'Publico general'
            if self.MOVI_CLASSIFICATION == 'PG':
                self.description_clasification = 'Se recomienda compañia de un adulto'
            if self.MOVI_CLASSIFICATION == 'PG-13':
                self.description_clasification = 'Mayor de 13 años'
            if self.MOVI_CLASSIFICATION == 'R':
                self.description_clasification = 'Se recomienda adulto responsable'
            if self.MOVI_CLASSIFICATION == 'RC-17':
                self.description_clasification = 'mayor de 18 años'
        else:
            self.description_clasification = False

    

            

