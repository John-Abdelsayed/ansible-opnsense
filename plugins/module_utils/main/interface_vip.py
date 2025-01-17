from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Vip(BaseModule):
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }
    API_KEY_PATH = 'vip.vip'
    API_MOD = 'interfaces'
    API_CONT = 'vip_settings'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'address', 'mode', 'cidr', 'expand', 'bind', 'gateway', 'password', 'vhid',
        'advertising_base', 'advertising_skew', 'description', 'interface',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'address': 'subnet',
        'cidr': 'subnet_bits',
        'expand': 'noexpand',
        'bind': 'nobind',
        'advertising_base': 'advbase',
        'advertising_skew': 'advskew',
        'description': 'descr',
    }
    FIELDS_DIFF_EXCLUDE = ['password']
    FIELDS_BOOL_INVERT = ['expand', 'bind']
    FIELDS_TYPING = {
        'bool': ['expand', 'bind'],
        'select': ['mode', 'interface', 'vhid', 'advertising_base', 'advertising_skew'],
        'int': ['vhid', 'advertising_base', 'advertising_skew'],
    }
    INT_VALIDATIONS = {
        'vhid': {'min': 1, 'max': 255},
        'advertising_base': {'min': 1, 'max': 254},
        'advertising_skew': {'min': 0, 'max': 254},
    }
    EXIST_ATTR = 'vip'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.vip = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()

    def update(self) -> None:
        self.b.update(enable_switch=False)
