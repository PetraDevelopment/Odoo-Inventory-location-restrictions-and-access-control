from odoo import fields, models, api

class CustomPicking(models.Model):
    _inherit = "stock.picking"

    @api.depends('picking_type_id.code')
    def _compute_is_incoming(self):
        for record in self:
            if record.picking_type_id.code == 'incoming':
                first_locations = self.env['stock.location'].search([('id','=',14)], limit=1)
                location_id = first_locations.id
                record.location_id=location_id
            else:
                location_id = None
                record.location_id=location_id

    @api.onchange('picking_type_id', 'partner_id')
    def _onchange_picking_type(self):
        pass

    @api.onchange('location_id', 'location_dest_id', 'picking_type_id')
    def _onchange_locations(self):
        pass

    @api.onchange('code')
    def _onchange_picking_code(self):
        pass


    location_id = fields.Many2one(
        'stock.location', "Source Location",
        compute=_compute_is_incoming,
        default=None,
        check_company=True, readonly=False, required=True,
        store=True, precompute=True,
        domain=lambda self: self._compute_location_domain(),
        states={'done': [('readonly', True)]},
    )

    # location_id = fields.Many2one(
    #     'stock.location', "Source Location",
    #     compute=_compute_is_incoming, store=True, precompute=True, readonly=False,
    #     check_company=True, required=True,
    #     states={'done': [('readonly', True)]},
    #     domain=lambda self: self._compute_location_domain(),
    #     # default=_default_location_id,
    # )


    def _compute_location_domain(self):
        if self.env.user.id == 2:
            return []
        else:
            selected_location_ids = self.env.user.selected_locations.ids
            domain = [
                ('id', 'in', selected_location_ids)
            ]
            return domain






    @api.depends('picking_type_id.code')
    def _compute_is_incomings(self):
        for record in self:
            if record.picking_type_id.code == 'outgoing':
                first_locations = self.env['stock.location'].search([('id','=',5)], limit=1)
                location_dest_id = first_locations.id
                record.location_dest_id=location_dest_id
            else:
                location_dest_id = None
                record.location_dest_id=location_dest_id
    
    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        default=None,
        compute=_compute_is_incomings,
        domain=lambda self: self._compute_location_domain(),
        store=True,precompute=True,
        check_company=True, readonly=False, required=True,
        states={'done': [('readonly', True)]},
    )

    # location_dest_id = fields.Many2one(
    #     'stock.location', "Destination Location",
    #     compute=_compute_is_incomings, store=True, precompute=True, readonly=False,
    #     check_company=True, required=True,
    #     domain=lambda self: self._compute_location_domain(),
    #     states={'done': [('readonly', True)]},
    #     # default=None,
    # )


    def _compute_location_domain(self):
        if self.env.user.id == 2:
            return []
        else:
            selected_location_ids = self.env.user.selected_locations.ids
            domain = [
                ('id', 'in', selected_location_ids)
            ]
            return domain