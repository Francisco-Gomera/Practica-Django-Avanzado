from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer para el modelo User.
    
    Incluye validación personalizada del campo email.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name']
        read_only_fields = ['pk']
        
    def validate_email(self, value):
        """Valida que el email contenga el símbolo '@'.
        
        Args:
            value: Valor del email a validar
            
        Returns:
            str: El email validado
            
        Raises:
            ValidationError: Si el email no contiene '@'
        """
        if "@" not in value:
            raise serializers.ValidationError("Email debe contener el símbolo '@'.")
        return value