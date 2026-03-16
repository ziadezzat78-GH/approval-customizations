{
    'name': 'Approval Customizations',
    'version': '1.0',
    'depends': ['base',
                'approvals',
                'hr'],
    'data':[
        'security/ir.model.access.csv',
        'security/groups.xml',
        'views/approval_request_view.xml',
        'data /approval_category_claim.xml',

    ],
    'installable': True,
    'application': False,
}
