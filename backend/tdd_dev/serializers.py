from rest_framework import serializers
from .models import Question

class QuestionOptionSerializer(serializers.Serializer):
    text = serializers.CharField()

class QuestionSerializer(serializers.Serializer):
    number = serializers.CharField()
    question_text = serializers.CharField()
    question_type = serializers.ChoiceField(choices=[qt[0] for qt in Question.QUESTION_TYPES])
    options = QuestionOptionSerializer(many=True, required=False)
    condition_question = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    condition_answer = serializers.CharField(required=False, allow_blank=True, allow_null=True)

class SurveyBuildSerializer(serializers.Serializer):
    title = serializers.CharField()
    questions = QuestionSerializer(many=True)

    def validate_questions(self, value):
        if not value:
            raise serializers.ValidationError("At least one valid question is required.")
        return value