from django.test import TestCase
from django.core.mail import send_mail

class EmailTest(TestCase):
    def test_enviar_correo(self):
        # Datos de prueba
        subject = 'Correo de Prueba'
        message = 'Este es un correo de prueba enviado desde la consola de Python.'
        from_email = 'yhuancas@unsa.edu.pe'
        recipient_list = ['yhuancas@unsa.edu.pe']


        # Intenta enviar el correo
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            # Si la autenticación falla, se lanzará una excepción
            self.fail(f'Error al enviar el correo: {str(e)}')

        # Si el correo se envía con éxito, la prueba pasa
        self.assertTrue(True)