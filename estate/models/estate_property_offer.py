from odoo import api, models, fields
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer'

    price = fields.Float()
    status = fields.Selection(selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')], copy=False)
    parter_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date()#compute='_compute_deadline')#, inverse='_inverse_deadline')

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)
    
    # def _inverse_deadline(self):
        # for record in self:
            # record.validity = abs(record.create_date - record.date_deadline)