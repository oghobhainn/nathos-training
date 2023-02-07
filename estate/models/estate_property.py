from odoo import api, models, fields
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
    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    tags_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offer')
    total_area = fields.Integer(compute='_compute_area')
    best_offer = fields.Integer(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        #self.total_area = self.living_area + self.garden_area 
        for line in self:
            line.total_area = line.living_area + line.garden_area
            
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:#why not just using self
            if prop.offer_ids:
                prop.best_offer = max(prop.offer_ids.mapped("price"))
            else:
                prop.best_offer = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'North'

    def action_sold(self):
        for record in self:
            record.state = 'Sold'