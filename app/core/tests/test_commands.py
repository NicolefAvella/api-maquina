from unittest.mock import patch # simular bd esta disponible y no esta disponible al probar test

from django.core.management import call_command
from django.db.utils import OperationalError  # simular error disponibilidad bd
from django.test import TestCase


class CommandsTestCase(TestCase):

    def test_wait_for_db_ready(self):
        """Test esperando por db cuando db esta disponible"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:  # simulamos comportamiento cuando bd esta disponible
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=None)   # para no esperar 1 segundo cuando para error, se ignora
    def test_wait_for_db(self, ts):
        """Test esperando por db"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]  # prueba bd 5 veces y la6 sera exitosa
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
