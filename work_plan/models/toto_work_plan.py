from odoo import models, fields, api


class WorkPlan(models.Model):
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _name = 'toto.work.plan'
    _rec_name = 'date'

    date = fields.Datetime('日期', default=fields.Datetime.now)
    # class_id = fields.Many2one('toto.work.class.type', '班别', ondelete="restrict")
    class_type_id = fields.Many2one('hr.department', '班别', ondelete="restrict",
                                    domain=lambda self: [('id', 'in', self.env.user.employee_ids.mapped('department_id').ids)])
    work_type = fields.Selection([('day', '早班'), ('middle', '中班'), ('night', '夜班')], string="班次")
    vacation = fields.Char('休假', default='无')
    staffing = fields.Integer('出勤人数')
    bad_content = fields.Text('不良内容')
    employee_ids = fields.Many2many('hr.employee', string='作业员', ondelete="restrict",
                                    domain="[('department_id', '=', class_type_id)]")
    detail_countermeasure = fields.Html('具体对策')
    item_ids = fields.One2many('toto.work.plan.item', 'plan_id', '人员安排', ondelete="cascade")
    plan_type = fields.Selection([
        ('shaping', '成形系'),
        ('power', '动力系'),
        ('dissolve', '溶着系'),
        ('process', '加工系'),
    ])


class WorkPlanItem(models.Model):
    _name = 'toto.work.plan.item'

    sequence = fields.Integer(string="Sequence", default=10)
    plan_id = fields.Many2one('toto.work.plan', '计划')
    device_id = fields.Many2one('toto.work.device', '设备', ondelete="restrict")
    employee_id = fields.Many2one('hr.employee', '作业员', ondelete="restrict")
    # domain="[('department_id', '=', parent.class_type_id)]"
    work_subject = fields.Char('作业项目')
    predetermined_quantity = fields.Integer('预定数量', default=None)
    actual_quantity = fields.Integer('实际数量', default=None)
    note = fields.Text('备注')
    state = fields.Selection([
        ('progress', '进行中'),
        ('done', '完成'),
        ('cancel', '终止'),
    ], string='状态', copy=False, default='progress', readonly=True, required=True)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
    name = fields.Char(string="名称")

    def action_finish(self):
        self.ensure_one()
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        self.state = 'cancel'
