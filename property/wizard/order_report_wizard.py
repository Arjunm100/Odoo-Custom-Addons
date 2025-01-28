# -*- coding: utf-8 -*-

"""Module used to manage data for generating rent or lease order reports"""
from openpyxl.xml.functions import tostring

from odoo import fields, models
from odoo.exceptions import ValidationError
import io
import json
import xlsxwriter
import base64
from odoo.tools import date_utils


class OrderReportWizard(models.TransientModel):
    """This model provides a wizard for generating Rent and Lease order reports based on various filters such as date
    range, state, tenant, property, owner,and rent/lease type. The generated report can be exported as a PDF. """
    _name = 'order.report.wizard'
    _description = 'Rent and Lease order report'

    from_date = fields.Date(string='Start Date')
    to_date = fields.Date(string='To Date', default=fields.Datetime.today())
    state = fields.Selection(string='State', selection=[
        ('draft', 'Draft'), ('confirmed', 'Confirmed'), ('close', 'Close'),
        ('return', 'Return'), ('expired', 'Expired')])
    tenant_id = fields.Many2one(string='Tenant', comodel_name='res.partner')
    rent_lease = fields.Selection(string='Rent or Lease?', selection=[
        ('rent', 'Rent'), ('lease', 'Lease')])
    property_id = fields.Many2one(comodel_name='property.management', string='Property')
    owner_id = fields.Many2one(comodel_name='res.partner', string='Owner')

    def action_generate_pdf_report(self):
        """Generates a Rent and Lease order report based on the filters provided in the wizard.

        - Constructs a SQL query dynamically based on the provided filters.
        - Executes the query to fetch the data.
        - If data is found, it generates and returns a PDF report.
        - If no data is found, raises a ValidationError."""
        if self.to_date and self.from_date and self.to_date < self.from_date:
            raise ValidationError("The end date cannot be earlier than the start date."
                                  " Please select a valid date range.")
        report = self.fetch_query_data()

        if not report:
            raise ValidationError("No data found to generate the PDF report. Please ensure the filters are set"
                                  " correctly, and relevant records are available.")
        data = {'date': self.read()[0], 'report': report}
        return self.env.ref('property.action_report_rent_lease').report_action(docids=None, data=data)

    def action_generate_xlsx_report(self):
        """Trigger the functionalities required to generate xlsx report"""
        if self.to_date and self.from_date and self.to_date < self.from_date:
            raise ValidationError("The end date cannot be earlier than the start date."
                                  " Please select a valid date range.")

        data = self.fetch_query_data()
        if not data:
            raise ValidationError("No data found to generate the XLSX report. Please ensure the filters are set"
                                  " correctly, and relevant records are available.")
        for rec in data:
            rec['start_date'] = fields.Datetime.to_string(rec['start_date'])
            rec['end_date'] = fields.Datetime.to_string(rec['end_date'])
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'order.report.wizard',
                     'options': json.dumps(data),
                     'output_format': 'xlsx',
                     'report_name': 'Property Order Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """Method used to generate xlsx file"""
        company = self.env.company
        address_list = [field for field in
                        [company.street, company.street2, company.city, company.state_id.name, company.country_id.name]
                        if field]
        address = "\n".join(address_list)
        file = io.BytesIO(base64.b64decode(company.logo))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px','bold': True, 'align': 'center','border': 1,'border_color': 'black'})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px','border': 1,'border_color': 'black'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center','border': 1,'border_color': 'black'})
        txt2 = workbook.add_format({'font_size': '10px', 'align': 'center', 'border': 1,
                                    'border_color': 'black','align':'vcenter'})
        sheet.merge_range('B2:I3', 'Property Orders Report', head)
        sheet.merge_range('A5:B5', 'Date', cell_format)
        sheet.merge_range('C5:E5', fields.Datetime.to_string(fields.Datetime.today()), txt)
        sheet.merge_range('K2:M2', self.env.company.name, txt)
        sheet.merge_range('O2:P6','')
        sheet.insert_image("O2", "example.jpg", {'image_data': file,'x_scale': 0.20,'y_scale': 0.19})
        sheet.merge_range('K3:M7',address,txt2)
        sheet.merge_range('A9:B9', 'Property Name', cell_format)
        sheet.merge_range('C9:D9', 'Owner Name', cell_format)
        sheet.merge_range('E9:F9', 'Order Type', cell_format)
        sheet.merge_range('G9:H9', 'Tenant Name', cell_format)
        sheet.merge_range('I9:J9', 'Start Date', cell_format)
        sheet.merge_range('K9:L9', 'End Date', cell_format)
        sheet.merge_range('M9:N9', 'Amount', cell_format)
        sheet.merge_range('O9:P9', 'State', cell_format)
        for record in data:
            index = data.index(record) + 10
            sheet.merge_range(f"A{index}:B{index}", record['property_name'], txt)
            sheet.merge_range(f"C{index}:D{index}", record['owner_name'], txt)
            sheet.merge_range(f"E{index}:F{index}", record['rent_lease'], txt)
            sheet.merge_range(f"G{index}:H{index}", record['tenant_name'], txt)
            sheet.merge_range(f"I{index}:J{index}", record['start_date'], txt)
            sheet.merge_range(f"K{index}:L{index}", record['end_date'], txt)
            sheet.merge_range(f"M{index}:N{index}", record['amount'], txt)
            sheet.merge_range(f"O{index}:P{index}", record['stages'], txt)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


    def fetch_query_data(self):
        """Method used to generate SQL query based on different conditions and fetch the value from database"""
        selection = ("""property.name AS property_name,owner.name AS owner_name,orders.rent_lease,tenant.name AS 
                        tenant_name,orders.start_date,orders.end_date,orderline.amount,orders.stages""")
        table_from = """property_orderline AS orderline INNER JOIN property_management AS property 
                                ON orderline.property_id = property.id INNER JOIN res_partner AS owner 
                                ON owner.id = property.owner_id INNER JOIN property_rent_lease AS orders
                                ON orderline.rent_lease_id = orders.id INNER JOIN res_partner AS tenant 
                                ON orders.tenant_id = tenant.id"""
        conditions = [f"orders.company_id = {self.env.company.id}"]

        if self.owner_id:
            conditions.append(f" AND property.owner_id = {self.owner_id.id}")
        if self.property_id:
            conditions.append(f" AND orderline.property_id = {self.property_id.id}")
        if self.to_date:
            conditions.append(f" AND orders.start_date < '{self.to_date}'")
        if self.from_date:
            conditions.append(f" AND orders.start_date > '{self.from_date}'")
        if self.tenant_id:
            conditions.append(f" AND orders.tenant_id = {self.tenant_id.id}")
        if self.state:
            conditions.append(f" AND orders.stages = '{self.state}'")
        if self.rent_lease:
            conditions.append(f" AND orders.rent_lease = '{self.rent_lease}'")
        query = f"SELECT {selection} FROM {table_from}"
        if conditions:
            query += " WHERE " + " ".join(conditions)
        self.env.cr.execute(query)
        data = self.env.cr.dictfetchall()
        selection = self.fields_get(['state','rent_lease'])
        order_selection = {}
        stages_selection = {}
        [order_selection.update({i[0]: i[1]}) for i in selection.get('rent_lease').get('selection')]
        [stages_selection.update({i[0]: i[1]}) for i in selection.get('state').get('selection')]
        for record in data:
            record['stages'] = stages_selection.get(record.get('stages'))
            record['rent_lease'] = order_selection.get(record.get('rent_lease'))
        return data

