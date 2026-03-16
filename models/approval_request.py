from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    category_code = fields.Char()


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    ziad = fields.Char(related='category_id.category_code')
    # -----------------
    # claim fields
    # ---------------------
    reason = fields.Text(help="Reason for the claim request")
    amount = fields.Integer()

    # -----------------------
    # Recruitment Fields
    # -----------------------
    department_id = fields.Many2one('hr.department')
    position_title = fields.Char(string="Post Title")
    experience_description = fields.Text(string="Experience Description")
    expected_salary = fields.Float(string="Expected Salary")
    recruitment_justification = fields.Text(
        string='Justification',
        help='Why do we need to hire for this position?'
    )

    position_name= fields.Char(string="Position Name")
    num_vacancies = fields.Integer(
        string='Number of Vacancies',
        help='Number of positions to fill'
    )

     # ---------------------------
        # travel  fields
    # ----------------------------------
    destination = fields.Char(store=False)
    date = fields.Date()


    # ---------------------------------
    # equipment fields
    # ---------------------------------

    equipment_type = fields.Selection([('laptop', 'Laptop'),
                                  ('mouse', 'Mouse'),
                                  ('table', 'Table'),
                                  ('computer', 'Computer'),
                                  ('phone', 'Phone')],)
    price=fields.Float()


    @api.constrains('price','category_id')
    def _check_price(self):
        equipment_category = self.env.ref(
            "approval_customizations.approval_category_equipment_request",
            raise_if_not_found=False
        )

        for rec in self:
            if rec.category_id == equipment_category and rec.price > 1500:
                raise ValidationError(
                    'Equipment Request amount cannot exceed 1500!'
                )

    @api.constrains('amount', 'category_id')
    def _check_claim_amount(self):
        """Validation: Claim amount cannot exceed 500"""
        claim_category = self.env.ref(
            "approval_customizations.approval_category_claim_request",
            raise_if_not_found=False
        )
        for record in self:
            if record.category_id == claim_category and record.amount > 500:
                raise ValidationError(
                    'Claim Request amount cannot exceed 500!'
                )


    @api.onchange('category_id')
    def _onchange_category_id(self):
        if self.category_id:
            self._set_approvers_from_group()



    @api.model_create_multi
    def create(self, vals_list):

        records = super(ApprovalRequest, self).create(vals_list)

        for record in records:
            if not record.approver_ids:
                record._set_approvers_from_group()

        return records


    def _set_approvers_from_group(self):
        self.ensure_one()
        if not self.category_id:
            return
        category_name = self.category_id.name
        category_to_group = {
            'Claim Request': 'approval_customizations.group_claim_approvers',
            'Recruitment Request': 'approval_customizations.group_recruitment_approvers',
            'Travel Request': 'approval_customizations.group_travel_approvers',
            'Equipment Request': 'approval_customizations.group_equipment_approvers',
        }
        group_xmlid = category_to_group.get(category_name)
        if group_xmlid:
            try:
                group = self.env.ref(group_xmlid, raise_if_not_found=False)
                if group and group.users:

                    approver_list = []
                    for user in group.users:
                        approver_list.append((0, 0, {
                            'user_id': user.id,
                            'status': 'new',
                        }))
                    self.approver_ids = approver_list
                    _logger.info(f"✅ Set {len(group.users)} approvers for {category_name}")
                else:
                    _logger.warning(f"⚠️ No users in group {group_xmlid}")

            except Exception as e:
                _logger.error(f"❌ Error setting approvers: {e}")




    def action_approve(self):
        """Override approve"""
        result = super(ApprovalRequest, self).action_approve()

        for request in self:
            if request.ziad == 'recruitment':
                request._create_job_position()

        return result

    def _create_job_position(self):
        """Create Job Position"""
        self.ensure_one()

        if not self.position_name:
            raise UserError('Position Name is required!')

        if self.num_vacancies <= 0:
            raise UserError('Number of Vacancies must be > 0!')

        job = self.env['hr.job'].create({
            'name': self.position_name,
            'no_of_recruitment': self.num_vacancies,
        })

        return job




