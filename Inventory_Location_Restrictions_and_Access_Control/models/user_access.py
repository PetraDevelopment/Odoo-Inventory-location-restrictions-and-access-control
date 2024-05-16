from odoo import api, fields,models

class AccessUsers(models.Model):
    _inherit="res.users"
    Access_All_Locations=fields.Boolean(string="Access All Location")
    selected_locations = fields.Many2many(
        'stock.location',
        string='Selected Locations',
        compute='_compute_selected_locations',
        store=True
    )
    location_ids = fields.One2many(
        'stock.location',  # Target model name
        'user_id',          # Related field name in the target model (stock.location)
        string='Locations'
    )
    @api.depends('location_ids.own_users')
    def _compute_selected_locations(self):
        for user in self:
            selected_locations = self.env['stock.location'].search([('own_users', 'in', user.ids)])
            user.selected_locations = selected_locations.mapped('name')