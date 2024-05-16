from odoo import api, fields,models

class LocationUsers(models.Model):
    _inherit="stock.location"

    own_users=fields.Many2many('res.users',string='Own Users',domain="[('Access_All_Locations', '=', True), ('id', '!=', 2)]",    widget='many2many_tags',create=False)
    selected_users = fields.Char(string='Accepted Users', compute='_compute_selected_user_names', store=True)
    user_id = fields.Many2one(
        'res.users',
        string='User'
    )

    @api.depends('own_users')
    def _compute_selected_user_names(self):
        default_user = self.env['res.users'].browse(2)
        default_user_name = default_user.name if default_user else ""
        for record in self:
            own_users_names = ", ".join(record.own_users.mapped('name'))
            record.selected_users = ", ".join(filter(None, [default_user_name, own_users_names]))

    def write(self, vals):
        # Call the super method to perform the write operation
        res = super(LocationUsers, self).write(vals)
       
        # Call methods from UserGroups model
        self.env['res.groups'].create_user_groups()

        return res        