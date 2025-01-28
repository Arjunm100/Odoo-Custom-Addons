# -*- coding: utf-8 -*-

"""This module provides a transient model for handling the import of order lines
into a sale order. It supports reading and processing Excel files while ensuring
that all required fields are validated and handled correctly"""

from io import BytesIO
import base64
from odoo import fields, models
import openpyxl
import odoo.exceptions as oe

class OrderLineImport(models.TransientModel):
    """This model allows users to upload an Excel file containing order line details,
    which are then processed and added to the selected sale order. It includes
    methods for validating the uploaded file, reading its content, and creating
    order lines based on the data provided."""
    _name = 'order.line.import'
    _description = 'Import Order lines'

    order_id = fields.Many2one(comodel_name='sale.order')
    file = fields.Binary('File')

    def action_import_lines(self):
        """ This method decodes the uploaded file, validates its format, checks for the
        presence of required fields, and processes the data to create order lines in
        the specified sale order."""
        try:
            workbook = openpyxl.load_workbook(
                filename=BytesIO(base64.b64decode(self.file)), read_only=True
            )
            workbook = workbook.active

        except:
            raise oe.ValidationError(
                "Failed to read the file.\n"
                "Please ensure the following:\n"
                "- The file is not corrupted or open in another program.\n"
                "- The file has a valid Excel format (.xlsx).\n"
            )
        required_fields = ['product_id', 'product_uom_qty', 'price_unit', 'product_uom', 'name']
        available_field = [field for field in [(val.value.lower().
                                               replace(" ", "_") if not isinstance(val.value,int)
                                                else val.value) for val in workbook[1]] if
                           field in required_fields]
        try:
            product_index = available_field.index('product_id') if len(available_field) == len(required_fields) else 0
            quantity_index = available_field.index('product_uom_qty') if len(available_field) == len(required_fields) else 1
            price_index = available_field.index('price_unit') if len(available_field) == len(required_fields) else 2
            unit_index = available_field.index('product_uom') if len(available_field) == len(required_fields) else 3
            name_index = available_field.index('name') if len(available_field) == len(required_fields) else 4

            for record in workbook.iter_rows(min_row=2, max_row=None,
                                       min_col=None, max_col=None, values_only=True):
                product = (self.env['product.product'].
                                  search([('name', '=', record[product_index])]))
                product = (product[0] if product
                        else (self.env['product.product'].
                                 create({'name': record[product_index]})))
                quantity = (record[quantity_index] if isinstance(record[quantity_index], int)
                            else 0)
                price = record[price_index] if isinstance(record[price_index], int) else 0
                name = record[name_index] if record[name_index] else ''
                uom = self.env['uom.uom'].search([('name', '=', record[unit_index])])
                uom = uom[0] if uom else product.uom_id

                self.order_id.order_line = [
                    fields.Command.create({
                        'product_id': product.id,
                        'product_uom_qty': quantity,
                        'price_unit': price,
                        'product_uom': uom.id,
                        'name': name
                    })
                ]
        except:
            raise oe.MissingError("Failed to export file")

