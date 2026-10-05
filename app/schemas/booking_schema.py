class BookingDTO:
    @staticmethod
    def validate_create(data):
        errors = {}

        if not data:
            return {"payload": "Se requiere un cuerpo JSON válido."}

        activity_id = data.get('activity_id')
        if not activity_id or not isinstance(activity_id, int):
            errors['activity_id'] = "El identificador de la actividad (activity_id) es obligatorio y debe ser un entero."

        return errors