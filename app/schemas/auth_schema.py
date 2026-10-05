import re

class AuthDTO:
    @staticmethod
    def validate_register(data):
        """Valida el payload para el registro de usuarios."""
        errors = {}

        if not data:
            return {"payload": "Se requiere un cuerpo JSON válido."}

        # Validar username
        username = data.get('username')
        if not username or not isinstance(username, str) or not username.strip():
            errors['username'] = "El nombre de usuario es obligatorio y no puede estar vacío."

        # Validar email
        email = data.get('email')
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not email or not isinstance(email, str) or not re.match(email_regex, email.strip()):
            errors['email'] = "Proporcione un correo electrónico válido."

        # Validar contraseña
        password = data.get('password')
        if not password or not isinstance(password, str) or len(password) < 6:
            errors['password'] = "La contraseña es obligatoria y debe tener al menos 6 caracteres."

        return errors

    @staticmethod
    def validate_login(data):
        """Valida el payload para el inicio de sesión."""
        errors = {}

        if not data:
            return {"payload": "Se requiere un cuerpo JSON válido."}

        email = data.get('email')
        if not email or not isinstance(email, str) or not email.strip():
            errors['email'] = "El correo electrónico es obligatorio."

        password = data.get('password')
        if not password or not isinstance(password, str) or not password.strip():
            errors['password'] = "La contraseña es obligatoria."

        return errors