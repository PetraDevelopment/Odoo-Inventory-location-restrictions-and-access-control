from odoo import models, api

class UserGroups(models.Model):
    _inherit = 'res.groups'

    @api.model
    def create_user_groups(self):
        users = self.env['res.users'].search([('id', '!=', 2)])
        for user in users:
            if user.selected_locations:
            # Check if the group already exists
                existing_group = self.env['res.groups'].search([('name', '=', f"Special group for {user.name}")], limit=1)
                
                if existing_group:
                    access_rules = self.env['ir.rule'].search([('groups', '=', existing_group.id)])
                    for access_rule in access_rules:
                        selected_location_ids = user.selected_locations
                        selected_location_info = ['/'.join((location.location_id.name, location.name)) for location in selected_location_ids]
                        access_rule.write({'domain_force': [('location_id', 'in', selected_location_info)]})
                else:
                    groups_data = [
                        {'name': f"Special group for {user.name}"}
                    ]
                    self.create(groups_data)
                    group_test_1 = self.env['res.groups'].search([('name', '=', f"Special group for {user.name}")], limit=1)

                    if group_test_1:
                        user_name = self.env['res.users'].search([('name', '=', user.name)], limit=1)
                        if user_name:
                            user_name.write({'groups_id': [(4, group_test_1.id)]})
                    product_template_model_id = self.env['ir.model'].search([('model', '=', 'stock.quant')], limit=1).id
                    group = self.env['res.groups'].search([('name', '=', f"Special group for {user.name}")], limit=1)
                    if group:
                        user_name = self.env['res.users'].search([('name', '=', user.name)], limit=1)
                        # Access the selected_locations field of the user object
                        selected_location_ids = user_name.selected_locations
                        selected_location_info = ['/'.join((location.location_id.name, location.name)) for location in selected_location_ids]
                        # Create an access rule for each group
                        access_rule = self.env['ir.rule'].create({
                            'name': f"Access to Product Template for {user.name}",
                            'model_id': product_template_model_id,
                            'perm_read': True,
                            'perm_write': True,
                            'perm_create': True,
                            'perm_unlink': True,
                            'active': True,
                            'groups': [(4, group.id)],
                            'domain_force':[('location_id', 'in', selected_location_info)]
                        })

    @api.model
    def create_user_to_groups(self):
        users = self.env['res.users'].search([('id', '!=', 2)])
        for user in users:
            # Create groups Test 1 and Test 2
            group_test_1 = self.env['res.groups'].search([('name', '=', f"Special group for {user.name}")], limit=1)

            if group_test_1:
                user_name = self.env['res.users'].search([('name', '=', user.name)], limit=1)
                if user_name:
                    user_name.write({'groups_id': [(4, group_test_1.id)]})
    @api.model
    def assign_access_rights(self):
        # Retrieve the model ID for product.template
        
        users = self.env['res.users'].search([('id', '!=', 2)])
        for user in users:
            product_template_model_id = self.env['ir.model'].search([('model', '=', 'stock.quant')], limit=1).id
            group = self.env['res.groups'].search([('name', '=', f"Special group for {user.name}")], limit=1)
            if group:
                user_name = self.env['res.users'].search([('name', '=', user.name)], limit=1)
                # Access the selected_locations field of the user object
                selected_location_ids = user_name.selected_locations
                selected_location_info = ['/'.join((location.location_id.name, location.name)) for location in selected_location_ids]
                # Create an access rule for each group
                access_rule = self.env['ir.rule'].create({
                    'name': f"Access to Product Template for {user.name}",
                    'model_id': product_template_model_id,
                    'perm_read': True,
                    'perm_write': True,
                    'perm_create': True,
                    'perm_unlink': True,
                    'active': True,
                    'groups': [(4, group.id)],
                    'domain_force':[('location_id', 'in', selected_location_info)]
                })
    @api.model
    def run(self):
        # Call methods from user_groups.py to automate user groups setup
        self.env['res.groups'].create_user_groups()
        self.env['res.groups'].create_user_to_groups()
        self.env['res.groups'].assign_access_rights()
