from odoo import models, fields
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Properties in sale."

    name = fields.Char(required=True)
    description = fields.Char(help=None)
    postcode = fields.Char(help=None)
    date_availability = fields.Date(default=lambda self: fields.Datetime.now() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(help=None)
    facades = fields.Integer(help=None)
    garage = fields.Boolean(help=None)
    garden = fields.Boolean(help=None)
    garden_area = fields.Integer(help=None)    
    garden_orientation = fields.Selection(
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West','West')])
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(
        selection=[('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold','Sold'), ('Canceled', 'Canceled')], default='New')