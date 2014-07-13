from couchpotato.core.logger import CPLog
from .main import Norbits

log = CPLog(__name__)

def autoload():
  return Norbits()

config = [{
  'name': 'norbits',
  'groups': [
    {
      'tab': 'searcher',
      'list': 'torrent_providers',
      'name': 'Norbits',
      'description': '<a href="https://norbits.net">Norbits</a>',
      'wizard': True,
      'icon': 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAF/SURBVDhPY/j0+dv/yIKO/y6xFf/d4qv+uydU48UgNSC1ID0gvQwghkNUGVGaYRikFqQHpJfBKabiv31kKQZ2iikHK3aNq8IpD3IJg0ts5f/mKcv+1/QthOP6iYv/x5f0/LcOK/rvkVj9v2kypnxscdd/2/CS/wyVPfP/4wIxRV1gDbhALFCeobRjDpgTmNn0P6miH4j7/ofmtP7/8/fv/7U7jvwvaJmJJt//PyS7BSy2eP1ehAHaHun/HaPLwdjAJ+v/0xevIQY0zwDLS1pEgcVBWNYm9v+L1+/+r9x6EGGAgU82PJRNA/OACt6CDciHGvDo2av/z1+9A+MnL96AxRonLaHMgLr+RYQNwOWFl2/e/1+5hQQvoAcyCCxev+c/Q1XPAjAH3YDPX7/+37b/1H+YBdhAbHH3f4ZgYJS0TV8BTl0wAxyjy/6Xdc79n1Y1EZzi0BNSw8Ql/6OAyRickEDRhqwZ2RCQZtxJuQKSlCnLTJ3/GT59oSA7f/n6HwDsB57Xl/E1hQAAAABJRU5ErkJggg==',
      'options': [
          {
              'name': 'enabled',
              'type': 'enabler',
              'default': False,
          },
          {
              'name': 'username',
              'default': '',
          },
          {
              'name': 'passkey',
              'default': '',
              'type': 'password',
          },
          {
              'name': 'seed_ratio',
              'label': 'Seed ratio',
              'type': 'float',
              'default': 1,
              'description': 'Will not be (re)moved until this seed ratio is met.',
          },
          {
              'name': 'seed_time',
              'label': 'Seed time',
              'type': 'int',
              'default': 40,
              'description': 'Will not be (re)moved until this seed time (in hours) is met.',
          },
          {
              'name': 'extra_score',
              'advanced': True,
              'label': 'Extra score',
              'type': 'int',
              'default': 20,
              'description': 'Starting score for each release found via this provider',
          }
      ],
    },
  ],
}]
