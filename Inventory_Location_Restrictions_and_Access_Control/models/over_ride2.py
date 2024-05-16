from odoo import fields, models,api

class StockMove(models.Model):
    _inherit = 'stock.move'

    
    product_id = fields.Many2one(
        'product.product', 
        'Product',
        check_company=True,
        domain=lambda self: self._compute_product_domain(),
        index=True, 
        required=True,
        states={'done': [('readonly', True)]}
    )

    @api.depends('product_id.qty_available')
    def _compute_product_domain(self):
        products_with_quantity = self.env['product.product'].search([('qty_available', '!=', 0)])
        domain = [
            ('id', 'in', products_with_quantity.ids),
            ('type', 'in', ['product', 'consu']),
            '|',
            # ('id', 'in', products_with_quantity.ids),
            ('company_id', '=', False),
            ('company_id', '=', self.company_id.id)
        ]
        # domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", index=True, required=True,
        print("***************************88",domain)
        return domain
class StockMoveLineInherit(models.Model):
    _inherit = 'stock.move.line'

    product_id = fields.Many2one(
        'product.product',
        string='Product',
        ondelete="cascade",
        check_company=True,
        domain=lambda self: self._compute_product_domain(),
        store=True,
        index=True
    )

    @api.depends('product_id.qty_available')
    def _compute_product_domain(self):
        products_with_quantity = self.env['product.product'].search([('qty_available', '!=', 0)])
        domain = [
            ('id', 'in', products_with_quantity.ids),
            ('type', 'in', ['product', 'consu']),
            '|',
            # ('id', 'in', products_with_quantity.ids),
            ('company_id', '=', False),
            ('company_id', '=', self.company_id.id)
        ]
        # domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", index=True, required=True,
        print("***************************88",domain)
        return domain

    # @api.depends('product_id')
    # def _compute_product_domain(self):
    #     for line in self:
    #         products_with_quantity = self.env['product.product'].search([('qty_available', '!=', 0)])
    #         line.product_id = products_with_quantity.filtered(lambda p: p.type != 'service')[:1]

    

# from odoo import fields, models, api


# class OverRideProduct(models.Model):
#     _inherit = "stock.move"

#     product_id = fields.Many2one(
#         'product.product', 'Product',
#         check_company=True,
#         domain=lambda self: [
#             ('id', 'in', self.env.user.selected_locations.mapped(lambda loc: loc.location_route_ids.mapped('product_ids').ids)),
#             ('type', 'in', ['product', 'consu']),
#             '|',
#             ('company_id', '=', False),
#             ('company_id', '=', self.company_id.id)
#         ],
#         states={'done': [('readonly', True)]})