from odoo import models, fields, api
import openerp.addons.decimal_precision as dp
from odoo import exceptions
import datetime

class Requisition(models.Model):

    _name = 'purchase.requisition'
    _description = 'Requisition For Purchase Orders'
    name = fields.Char('Requisition Number')
    reference = fields.Char('Reference')
    dest_warehouse = fields.Many2one('stock.warehouse','Warehouse', required = True)
    delivery_date = fields.Datetime('Delivery Date', states={'draft': [('readonly', False)], 'done': [('readonly', True)]}, required =True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Appoved'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default='draft')
    requisition_line = fields.One2many('purchase.requisition.line', 'requisition_id', string='Order Lines', states={'draft': [('readonly', False)], 'done': [('readonly', True)]}, copy=True, auto_join=True, required = True)
    po_id = fields.Char('PO Number')
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states={'draft': [('readonly', False)], 'done': [('readonly', True)]}, track_visibility='always', help="You can find a vendor by its Name, TIN, Email or Internal Reference.")

    @api.model
    def create(self, vals):
        record = super(Requisition, self).create(vals)
        if vals.get('requisition_line'):
            requisition_number = "REQ0" + str(record.id)
            record.name = requisition_number
        else:
            raise exceptions.ValidationError('You have to input at least one Product')

        return record

    def action_approve(self):
        req_env = self.env['purchase.requisition']

        for item in self:
            po_data = {}

            po_data['origin'] = item.reference
            po_data['partner_id'] = int(item.partner_id.id)
            po_data['picking_type_id'] = int(item.dest_warehouse.in_type_id)
            po_data['origin'] = item.name

            product_line_list = list()

            for line_item in item.requisition_line:
                product_line_list.append([0,False,
                                          {
                                              'product_id': int(line_item.product_id),
                                              'name': line_item.product_id.product_tmpl_id.display_name,
                                              'price_unit': float(line_item.price_unit),
                                              'product_qty': float(line_item.product_uom_qty),
                                              'product_uom': int(line_item.product_uom),
                                              'state': 'draft',
                                              'account_analytic_id': False,
                                              'date_planned': item.delivery_date
                                          }
                ])

            po_data['order_line'] = product_line_list
            po_env = self.env['purchase.order']
            save_the_data = po_env.create(po_data)


            req_update_query = "UPDATE purchase_requisition SET state = 'approve', po_id = '{1}'  WHERE id = {0}".format(item.id, str(save_the_data.name))
            self.env.cr.execute(req_update_query)
            self.env.cr.commit()

            line_update_query = "UPDATE purchase_requisition_line SET state = 'approve' WHERE requisition_id = {0}".format(item.id)
            self.env.cr.execute(line_update_query)
            self.env.cr.commit()

        return True



class RequisitionLine(models.Model):

    _name = 'purchase.requisition.line'
    _description = 'Product Line For Requisiton'

    requisition_id = fields.Many2one('purchase.requisition', string = 'Requisition Number', ondelete='cascade', index=True, copy=False, required=True, readonly=True)
    product_id = fields.Many2one('product.product', string = 'Product', required = True)
    product_uom_qty = fields.Float(string='Ordered Quantity', digits=dp.get_precision('Product Unit of Measure'), required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string = 'Unit Of Measure', required = True)
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Appoved'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3,
        default='draft')

    def unlink(self):
        for line in self:
            if line.requisition_id.state == "approve":
                raise exceptions.UserError(('Cannot delete a Requisition Line which is in state \'%s\'.') % (line.state,))
        return super(RequisitionLine, self).unlink()