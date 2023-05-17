from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_ids = fields.One2many('res.partner.wmr_contacts', 'partner_id', string='Contact Details', copy=False)

class ContactDetails(models.Model):
    _name = "res.partner.wmr_contacts"
    _description = "Contact Details"

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    telephone = fields.Char(string="Telephone")
    primary = fields.Boolean(string="Primary Contact")
    partner_id = fields.Many2one('res.partner',string='Parent Contact Id', index=True, copy=True,ondelete='set null', track_visibility='onchange', track_sequence=3, store=True)
    