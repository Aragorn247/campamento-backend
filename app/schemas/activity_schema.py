class ActivityDTO:
    @staticmethod
    def validate_create(data):
        errors = {}

        if not data:
            return {"payload": "Se requiere un cuerpo JSON válido."}

        name = data.get('name')
        if not name or not isinstance(name, str) or not name.strip():
            errors['name'] = "El nombre de la actividad es obligatorio."

        capacity = data.get('capacity')
        if capacity is None or not isinstance(capacity, int) or capacity <= 0:
            errors['capacity'] = "La capacidad debe ser un número entero mayor que 0."

        price = data.get('price')
        if price is None or not (isinstance(price, (int, float))) or price < 0:
            errors['price'] = "El precio debe ser un número igual o mayor a 0."

        return errors