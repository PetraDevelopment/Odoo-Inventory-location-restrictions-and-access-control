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
            ('company_id', '=', False),
            ('company_id', '=', self.company_id.id)
        ]
        return domain