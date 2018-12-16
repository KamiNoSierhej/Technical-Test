from rest_framework import serializers

from users.helpers import credit_check_call
from users.models import CreditCheck


class CreditCheckDefault:
    def validate_user(self):
        user_with_full_name = (
            self.user.has_profile and
            self.user.profile.first_name and
            self.user.profile.last_name
        )

        if not user_with_full_name:
            raise serializers.ValidationError(
                'Users first or last name missing.'
            )

    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user
        self.validate_user()
        self.credit_check_resonse = credit_check_call(
            self.user.profile.first_name,
            self.user.profile.last_name
        )

    def __call__(self):
        accepted = self.credit_check_resonse.get('accepted')

        if accepted is None:
            raise serializers.ValidationError(
                'Error with message:'
                f' {self.credit_check_resonse.get("Message", "error")}'
                ' occurred.'
            )

        return accepted

    def __repr__(self):
        return self.credit_check_resonse['accepted']


class CreditCheckSerializer(serializers.ModelSerializer):
    accepted = serializers.HiddenField(
        default=CreditCheckDefault()
    )
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def to_representation(self, obj):
        return {
            'user': obj.user_id,
            'accepted': obj.accepted
        }

    class Meta:
        model = CreditCheck
        fields = ('accepted', 'user',)
