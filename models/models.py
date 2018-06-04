# -*- coding: utf-8 -*-

from odoo import models, fields, api

class eschool_res_company(models.Model):
    _inherit='res.company'
    email_suffix = fields.Char('Default Email Suffix for New Contacts',default='dsblsc.com')
class eschoolCampus(models.Model):
    _inherits={'res.company':'company_id'}
    _name='eschool.campus'
    parent_campus=fields.Many2one('eschool.campus','Mother Branch')
    campus_code=fields.Char('Campus Code')
    medium_ids=fields.Many2many('eschool.medium','res_company_eschool_medium_rel','campus_ids','medium_ids')
    shift_ids=fields.Many2many('eschool.shift','eschool_campus_eschool_shift_rel','campus_ids','shift_ids')
    standard_ids=fields.Many2many("eschool.standard","eschool_campus_eschool_standard_rel",'standard_ids','campus_ids')
    company_id = fields.Many2one(
        'res.company', 'id', required=True, ondelete="cascade")
class eschoolShift(models.Model):
    ''' Defining a medium(ENGLISH, HINDI, GUJARATI) related to standard'''
    _name = "eschool.shift"
    _description = "Shift"
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    description = fields.Text('Description')
    campus_ids=fields.Many2many('eschool.campus','eschool_campus_eschool_shift_rel','shift_ids','campus_ids')
class eschoolMedium(models.Model):
    ''' Defining a medium(ENGLISH, HINDI, GUJARATI) related to standard'''
    _name = "eschool.medium"
    _description = "Standard Medium"
    _order = "name"
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    description = fields.Text('Description')
    course_ids=fields.One2many('op.course','medium_id',"courses")
    standard_ids = fields.Many2many('eschool.standard', 'eschool_medium_eschool_standard_rel', 'medium_ids',
                                  'standard_ids', 'Standard')
class eschoolstandards(models.Model):
    ''' Defining Standard Information '''
    _name = 'eschool.standard'
    _description = 'standard Information'
    _order = "sequence"
    course_ids = fields.One2many('op.course','standard_id', 'Course', required=True)
    sequence = fields.Integer('Sequence', required=True)
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    description = fields.Text('Description')
    campus_ids=fields.Many2many('eschool.campus','eschool_campus_eschool_standard_rel','standard_ids','campus_ids')
    medium_ids=fields.Many2many('eschool.medium','eschool_medium_eschool_standard_rel','standard_ids','medium_ids','Medium')
    _sql_constraints = [
        ('unique_standards_code',
         'unique(code)', 'Code should be unique per standards!')]
    @api.model
    def next_standard(self, sequence):
        '''This method check sequence of standard'''
        stand_ids = self.search([('sequence', '>', sequence)], order='id',
                                limit=1)
        if stand_ids:
            return stand_ids.id
        return False
class opCourse(models.Model):
    _inherit = 'op.course'
    medium_id=fields.Many2one('eschool.medium',required=True)
    name=fields.Char('Name',compute="get_course_code",required=True)
    standard_id = fields.Many2one('eschool.standard','Class', required=True)
    batch_id=fields.Many2one('op.batch','Batch',required=True)
    code=fields.Char('Code',compute='get_course_code',size=30)
    parent_id = fields.Many2one('op.course',"Next Class")
    _sql_constraints = [
        ('unique_course',
         'unique(medium_id,standard_id,batch_id)',
         'Course must be unique per Class/Batch/Medium.'),
    ]
    @api.onchange('medium_id','batch_id','name','standard_id')
    def get_course_code(self):
        for rec in self:
            rec.code='%s %s %s'%(rec.standard_id.code,rec.batch_id.code,rec.medium_id.code)
            rec.name='%s %s %s'%(rec.standard_id.name,rec.batch_id.name,rec.medium_id.name)
class opbatchInherit(models.Model):
    _inherit = 'op.batch'
    current=fields.Boolean("Current", help="Set Batch Active")
    code = fields.Char('Code', required=True)
    course_id=fields.One2many('op.course','batch_id','Courses')
class opAdmissionInherit(models.Model):
    _inherit = 'op.admission'

    @api.onchange('register_id')
    def onchange_register(self):
        self.course_id = self.register_id.course_id
        self.fees = self.register_id.product_id.lst_price
        self.batch_id=self.course_id.batch_id
    @api.onchange('name')
    def generate_email(self):
            self.email = '%s.%s@dsblsc.com' %(self.name,self.application_number)
            self.country_id=20

    @api.onchange('course_id')
    def onchange_course(self):
        # self.batch_id = False
        term_id = False
        if self.course_id and self.course_id.fees_term_id:
            term_id = self.course_id.fees_term_id.id
        self.fees_term_id = term_id
class insertStudentsforAttendance(models.Model):
    _inherit = 'op.attendance.sheet'
    got_student=fields.Boolean('Got Student?')

    @api.multi
    def get_students(self):
        student_in_course= self.env['op.student.course'].search([('course_id','=',self.course_id.id)])
        for student in student_in_course:
            self.env['op.attendance.line'].create({'attendance_id': self.id,'student_id':student.student_id.id,'register_id':self.register_id,'batch_id': self.batch_id.id,'present': True})
        self.got_student=True